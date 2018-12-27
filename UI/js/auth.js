let cookie = document.cookie.split(";");
let token = cookie[0];
let name = cookie[1];
let email = cookie[2];
let username = cookie[3];
let id = cookie[4];
let isAdmin = cookie[5];

if (document.cookie.length == 0){
  window.location.replace("signin.html");
}