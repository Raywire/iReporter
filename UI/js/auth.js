const root = 'https://pure-wildwood-82378.herokuapp.com/api/v2/';

let token = getCookie('token');
let name = getCookie('name');
let email = getCookie('email');
let username = getCookie('username');
let id = getCookie('id');
let isAdmin = getCookie('isAdmin');
let isLoggedIn = getCookie('isLoggedIn');

if (isLoggedIn == 'False' || isLoggedIn == "logged out" || token == "logged out"){
  window.location.replace("signin.html");
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