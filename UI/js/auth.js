let token = getCookie('token');
let name = getCookie('name');
let email = getCookie('email');
let username = getCookie('username');
let isAdmin = getCookie('isAdmin');
let isLoggedIn = getCookie('isLoggedIn');

const user = {
  token: token,
  name: name,
  email: email,
  username: username,
  isAdmin: isAdmin,
  isLoggedIn: isLoggedIn
};

if (isLoggedIn === 'False' || isLoggedIn === "logged out" || token === "logged out") {
  window.location.replace("signin.html");
}