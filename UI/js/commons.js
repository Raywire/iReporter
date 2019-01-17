const config = {
  root : 'https://pure-wildwood-82378.herokuapp.com/api/v2/',
  resetlink: 'https://raywire.github.io/iReporter/UI/reset_password.html'
}

function setCookie(cname, cvalue, expirationtime) {
  let date = new Date();
  date.setTime(date.getTime() + (expirationtime * 60 * 1000));
  let expires = "expires=" + date.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/;" + "sameSite=Strict;";
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "logged out";
}

let scrollFunction = () => {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    document.getElementById("toTop").style.display = "block";
  } else {
    document.getElementById("toTop").style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
let topFunction = () => {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

let hideLoader = (timer) => {
  setTimeout(hide, timer);

  function hide() {
    document.getElementById("loader").style.display = "none";
  }
}

let showLoader = () => {
  document.getElementById("loader").style.display = "block";
}

let checkPassword = () => {
  let pass1 = document.getElementById('password').value;
  let confirm_pass1 = document.getElementById('confirm_password').value;

  if (pass1 == confirm_pass1) {
    document.getElementById('password').style.borderColor = "green";
    document.getElementById('confirm_password').style.borderColor = "green";
  } else {
    document.getElementById('password').style.borderColor = "red";
    document.getElementById('confirm_password').style.borderColor = "red";
  }
}