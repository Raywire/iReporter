const config = {
  root: 'https://pure-wildwood-82378.herokuapp.com/api/v2/',
  resetlink: 'https://raywire.github.io/iReporter/UI/reset_password.html',
};

const setCookie = (cname, cvalue, expirationtime) => {
  const date = new Date();
  date.setTime(date.getTime() + (expirationtime * 60 * 1000));
  const expires = `expires=${date.toUTCString()}`;
  document.cookie = `${cname}=${cvalue};${expires};path=/;sameSite=Strict;`;
};

const getCookie = (cname) => {
  const name = `${cname}=`;
  const decodedCookie = decodeURIComponent(document.cookie);
  const ca = decodedCookie.split(';');
  for (let i = 0; i < ca.length; i += 1) {
    let c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
  return 'logged out';
};

const scrollFunction = () => {
  if (document.body.scrollTop > 40 || document.documentElement.scrollTop > 40) {
    document.getElementById('toTop').style.display = 'block';
  } else {
    document.getElementById('toTop').style.display = 'none';
  }
};

// When the user clicks on the button, scroll to the top of the document
const topFunction = () => {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
};

const hideLoader = (timer) => {
  function hide() {
    document.getElementById('loader').style.display = 'none';
  }
  setTimeout(hide, timer);
};

const showLoader = () => {
  document.getElementById('loader').style.display = 'block';
};

const checkPassword = () => {
  const pass1 = document.getElementById('password').value;
  const confirmPass1 = document.getElementById('confirm_password').value;

  if (pass1 === confirmPass1) {
    document.getElementById('password').style.borderColor = 'green';
    document.getElementById('confirm_password').style.borderColor = 'green';
  } else {
    document.getElementById('password').style.borderColor = 'red';
    document.getElementById('confirm_password').style.borderColor = 'red';
  }
};

const resetPassword = (event, profileusername, resettoken) => {
  event.preventDefault();
  document.getElementById('fa-spin-reset').style.display = 'block';

  const uri = `${config.root}users/${profileusername}`;

  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirm_password').value;

  if (password === confirmPassword) {
    const options = {
      method: 'PATCH',
      mode: 'cors',
      headers: new Headers({
        'Content-Type': 'application/json; charset=utf-8',
        'x-access-token': resettoken,
      }),
      body: JSON.stringify({
        password,
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
        if (Object.prototype.hasOwnProperty.call(j, 'message')) {
          if (j.message === 'Token is missing') {
            document.getElementById('error-message').innerHTML = 'Token is missing';
          }
          if (j.message === 'Token is invalid') {
            document.getElementById('error-message').innerHTML = 'Token is invalid or has expired';
          }
          if (j.message === 'User does not exist') {
            warningNotification({
              title: 'Warning',
              message: j.message,
            });
          }
          if (Object.prototype.hasOwnProperty.call(j.message, 'password')) {
            document.getElementById('password').style.borderColor = 'red';
            warningNotification({
              title: 'Warning',
              message: j.message.password,
            });
          }
          if (j.message === 'Only an admin or the user can update their own password') {
            warningNotification({
              title: 'Warning',
              message: j.message,
            });
          }

          if (j.message === 'User password has been changed') {
            successNotification({
              title: 'Success',
              message: `${j.message} for ${j.username}`,
            });
            setTimeout(logout(), 3000);
          }
        }

        document.getElementById('fa-spin-reset').style.display = 'none';
      })
      .catch((err) => {
        console.log(err);
        document.getElementById('fa-spin-reset').style.display = 'none';
      });
  } else if (password !== confirmPassword) {
    document.getElementById('fa-spin-reset').style.display = 'none';
    document.getElementById('password').style.borderColor = 'red';
    document.getElementById('confirm_password').style.borderColor = 'red';
  }
};
