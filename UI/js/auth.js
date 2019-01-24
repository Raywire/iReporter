let token = getCookie('token');
let name = localStorage.getItem('profileName');
let email = localStorage.getItem('profileEmail');
let phonenumber = localStorage.getItem('profilePhoneNumber');
let username = getCookie('username');
let isAdmin = getCookie('isAdmin');
let isLoggedIn = getCookie('isLoggedIn');

const user = {
  token,
  name,
  email,
  phonenumber,
  username,
  isAdmin,
  isLoggedIn
};

if (isLoggedIn === 'False' || isLoggedIn === 'logged out' || token === 'logged out') {
  window.location.replace('signin.html');
}
