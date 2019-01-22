let token = getCookie('token');
let name = localStorage.getItem('profileName');
let email = localStorage.getItem('profileEmail');
let phonenumber = localStorage.getItem('profilePhoneNumber');
let username = getCookie('username');
let isAdmin = getCookie('isAdmin');
let isLoggedIn = getCookie('isLoggedIn');

const user = {
  token: token,
  name: name,
  email: email,
  phonenumber: phonenumber,
  username: username,
  isAdmin: isAdmin,
  isLoggedIn: isLoggedIn
};

if (isLoggedIn === 'False' || isLoggedIn === 'logged out' || token === 'logged out') {
  window.location.replace('signin.html');
}
