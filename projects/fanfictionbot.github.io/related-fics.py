import psaw
import progressbar
import re
from collections import defaultdict, namedtuple
import sys
import argparse
import json

comment_regex = re.compile(r"""\[\*\*\*(?P<name>.+)\*\*\*\].+fanfiction.net\/s\/(?P<id>\d+)""")
FicComment = namedtuple('FicComment', ['name', 'id', 'score', 'permalink'])


def get_comment_mapping(author: str, num_comments: int):
    fic_id_to_submissions, submissions_to_fics = defaultdict(set), defaultdict(set)
    bar = progressbar.ProgressBar(max_value=num_comments)
    api = psaw.PushshiftAPI()
    errors = []
    for i, comment in enumerate(
            api.search_comments(author=author,
                                filter=['score', 'id', 'link_id', 'body', 'permalink'],
                                limit=num_comments)):
        bar.update(i)
        for fic_name, fic_id in re.findall(comment_regex, comment.body):
            try:
                # Validate that all attributes exist (some of these will not for removed/deleted submissions)
                _, _, _, _, _ = comment.score, comment.id, comment.link_id, comment.body, comment.permalink
                f = FicComment(name=fic_name, id=fic_id, score=comment.score, permalink=comment.permalink)
                fic_id_to_submissions[fic_id].add(comment.link_id)
                submissions_to_fics[comment.link_id].add(f)
            except Exception as e:
                errors.append(str(e))
                continue
    bar.finish()

    if len(errors) > 0:
        print("Errors:\n" + "\n".join(errors))
        print(f"{len(errors)} errors.")

    return fic_id_to_submissions, submissions_to_fics


def to_json(mapping):
    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError

    return json.dumps(mapping, default=set_default)


def get_related_fics_engine(author: str, num_comments: int, json_file: str, json_mode: str):
    fic_id_to_submissions, submissions_to_fics = None, None

    if json_mode == "read":
        with open(json_file, "r") as f:
            mapping = json.load(f)
            fic_id_to_submissions = mapping['fic_id_to_submissions']
            submissions_to_fics = mapping['submissions_to_fics']
        print(f"Loaded {len(fic_id_to_submissions)} fics across {len(submissions_to_fics)} submissions.")
    elif json_mode == "write":
        fic_id_to_submissions, submissions_to_fics = get_comment_mapping(author, num_comments)
        with open(json_file, "w") as text_file:
            text_file.write(to_json({
                "fic_id_to_submissions": fic_id_to_submissions,
                "submissions_to_fics": submissions_to_fics,
            }))
        print(f"Saved {len(fic_id_to_submissions)} fics across {len(submissions_to_fics)} submissions.")
    elif json_mode == "ignore":
        fic_id_to_submissions, submissions_to_fics = get_comment_mapping(author, num_comments)
    else:
        raise Exception("json_mode must be one of [read, write, ignore]")

    def get_related_fics(req_id: str) -> list:
        Fic = namedtuple('Fic', ['name', 'url'])
        counter = defaultdict(int)
        for link_id in fic_id_to_submissions[req_id]:
            for fic in submissions_to_fics[link_id]:
                fic = FicComment(*fic)
                if fic.id == req_id or fic.score <= 0:
                    continue
                url = f"https://www.fanfiction.net/s/{fic.id}/1/"
                counter[Fic(fic.name, url)] += fic.score
        return sorted([(score, fic) for fic, score in counter.items()])[::-1]

    return get_related_fics


def prompt_num_comments(author: str):
    print(f"Determining the number of comments that {author} has made.")
    num_comments = sum(api.redditor_subreddit_activity(author)['comment'].values())
    print(f"Enter the number of comments you'd like to index (1-{num_comments}):")
    for request in sys.stdin:
        request = request.rstrip()
        if not request.isnumeric():
            print("Please enter a valid number:")
            continue
        request = int(request)
        if request <= 0 or request > num_comments:
            print("Number out of range. Please enter a valid number:")
            continue
        num_comments = request
        break

    return num_comments


if __name__ == '__main__':
    api = psaw.PushshiftAPI()

    args = argparse.ArgumentParser()
    args.add_argument("--json-path", type=str, help="location of jsond comment mapping", default="comment_mapping.json")
    args.add_argument("--json-mode", type=str, help="whether to [read|write|ignore] the json file", default="read")
    args.add_argument("--author", type=str, help="username that FanfictionBot is operating under",
                      default="FanfictionBot")
    args.add_argument("--num-comments", type=int, help="number of comments; default will determine maximum", default=0)
    args.add_argument("--num-recs", type=int, help="maximum number of recs to give; 0 is unlimited", default=15)
    parsed = args.parse_args()

    num_comments = parsed.num_comments
    if parsed.json_mode != "read" and not num_comments:
        num_comments = prompt_num_comments(parsed.author) if parsed.json_mode != "read" else 0
    get_related_fics = get_related_fics_engine(parsed.author, num_comments, parsed.json_path, parsed.json_mode)

    print("\nEnter the ID of the fic you'd like to find related fics for:")
    for request in sys.stdin:
        request = request.rstrip()
        result = get_related_fics(request)
        display_limit = parsed.num_recs if parsed.num_recs else len(result)
        if len(result) == 0:
            print(f"Could not find fic with id {request}. Please try another ID:")
            continue
        for result in result[:display_limit]:
            print(result)
