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
console.log(nowInMilliseconds);
console.log(expiration);
console.log(refreshWindow);

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

  const options = {
    method: 'POST',
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
      'x-access-token': user.token,
    }),
  };
  const request = new Request(uri, options);

  fetch(request)
    .then((response) => {
      if (response.ok) {
        return response.json();
      }
      return response.json();
    })
    .then((j) => {
      if (Object.prototype.hasOwnProperty.call(j, 'token')) {
        const newToken = j.token;
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
