# Fanfiction Search Engine

This engine builds off of ~100K recommendations users have made via
[/u/FanfictionBot](https://www.reddit.com/user/FanfictionBot) in order to
find the most commonly recommended fanfictions for any given fanfiction.

## Quick Start

### First Run

Install the requirements:

```bash
$ pip install -r requirements.txt
```

Fetch all ~100K comments the bot has made and build an in-memory
index relating each fanfiction to comment and submission it was
a part of.

```bash
$ python related-fics.py --json-mode=write --num-comments=99000
```

This will save the results of the search in a file called `comment_mapping.json`.
Additionally, it will bring up the prompt that lets you search for related
fics.

### Subsequent Runs

You can load the json file you generated into the script so you do not
have to perform the long and tedious task of fetching ~100K comments:

```bash
$ python related-fics.py
Loaded 12320 fics across 19019 submissions.

Enter the ID of the fic you'd like to find related fics for:
3473224
(39, Fic(name='The Mind Arts', url='https://www.fanfiction.net/s/12740667/1/'))
(26, Fic(name='The many Deaths of Harry Potter', url='https://www.fanfiction.net/s/12388283/1/'))
(26, Fic(name='The Arithmancer', url='https://www.fanfiction.net/s/10070079/1/'))
(24, Fic(name='Harry Potter and the Natural 20', url='https://www.fanfiction.net/s/8096183/1/'))
(23, Fic(name='Browncoat, Green Eyes', url='https://www.fanfiction.net/s/2857962/1/'))
(22, Fic(name='A Black Comedy', url='https://www.fanfiction.net/s/3401052/1/'))
(20, Fic(name='The Skitterleap', url='https://www.fanfiction.net/s/5150093/1/'))
(20, Fic(name='Prince of the Dark Kingdom', url='https://www.fanfiction.net/s/3766574/1/'))
(20, Fic(name='Ectomancer', url='https://www.fanfiction.net/s/4563439/1/'))
(19, Fic(name='A Second Chance at Life', url='https://www.fanfiction.net/s/2488754/1/'))
(18, Fic(name='Stages of Hope', url='https://www.fanfiction.net/s/6892925/1/'))
(18, Fic(name='Harry Potter and the Wastelands of Time', url='https://www.fanfiction.net/s/4068153/1/'))
(17, Fic(name='Seventh Horcrux', url='https://www.fanfiction.net/s/10677106/1/'))
(17, Fic(name='Magicks of the Arcane', url='https://www.fanfiction.net/s/8303194/1/'))
(17, Fic(name='Harry Potter and the Sword of the Hero', url='https://www.fanfiction.net/s/3994212/1/'))
```
