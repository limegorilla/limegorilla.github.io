function pop(theurl, w, h, scroll)
{
 var the_atts = "width="+w+", height="+h+", top=20, screenY=20, left=20, screenX=20,  toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars="+scroll+", resizable=yes, copyhistory=no";
 // open window
 window.open(theurl,'pop',the_atts);
}

function submit1() {
    document.passwordform.email.value;
    return false;
}

function disableSubmit(menu) {
  if (menu.options[menu.selectedIndex].id == "disable")
     menu.form.submit.disabled = true;
if (menu.options[menu.selectedIndex].id == "enable")
     menu.form.submit.disabled = false;
}