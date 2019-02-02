const token = getCookie('token');
const name = localStorage.getItem('profileName');
const email = localStorage.getItem('profileEmail');
const phonenumber = localStorage.getItem('profilePhoneNumber');
const username = getCookie('username');
const isAdmin = getCookie('isAdmin');
const isLoggedIn = getCookie('isLoggedIn');
const currentDate = new Date();
const nowInMilliseconds = currentDate.getTime();
const expiration = localStorage.getItem('expiration');
const expirationTime = localStorage.getItem('expirationTime');
const refreshWindow = expiration - nowInMilliseconds;
const gracePeriod = 300000; // 5 minutes

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

const refreshToken = () => {
  const uri = `${config.root}users/${user.username}/refreshToken`;

  fetch(uri, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-access-token': user.token,
    },
    mode: 'cors',
  }).then((resp) => {
    if (resp.ok) {
      return resp.json();
    }
    return resp.json();
  }).then((resp) => {
    if (Object.prototype.hasOwnProperty.call(resp, 'token')) {
      const newToken = resp.token;
      setCookie('token', newToken, expirationTime);
      setCookie('username', user.username, expirationTime);
      setCookie('isAdmin', user.isAdmin, expirationTime);
      setCookie('isLoggedIn', 'True', expirationTime);
      const newExpirationTimeMilliseconds = nowInMilliseconds + (expirationTime * 60000);
      localStorage.setItem('expiration', newExpirationTimeMilliseconds);
    }
  });
};

if (refreshWindow <= gracePeriod) {
  refreshToken();
}
