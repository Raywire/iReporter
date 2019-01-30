const token = getCookie('token');
const name = localStorage.getItem('profileName');
const email = localStorage.getItem('profileEmail');
const phonenumber = localStorage.getItem('profilePhoneNumber');
const username = getCookie('username');
const isAdmin = getCookie('isAdmin');
const isLoggedIn = getCookie('isLoggedIn');

const user = {
  token,
  name,
  email,
  phonenumber,
  username,
  isAdmin,
  isLoggedIn,
};

if (user.isLoggedIn === 'False' || user.isLoggedIn === 'logged out' || user.token === 'logged out') {
  window.location.replace('signin.html');
}
