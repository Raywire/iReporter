const isLoggedIn = getCookie('isLoggedIn');

const redirection = () => {
  window.location.replace('signin.html');
};

if (isLoggedIn === 'True') {
  window.location.replace('home.html');
}

const signIn = (event) => {
  event.preventDefault();
  document.getElementById('error-message').innerHTML = '';

  document.getElementById('username').style.borderBottomColor = 'white';
  document.getElementById('password').style.borderBottomColor = 'white';
  document.getElementById('error-message').style.color = 'red';
  document.getElementById('fa-spin').style.display = 'block';
  document.getElementById('submit').value = 'Signing In';

  const uri = `${config.root}auth/login`;

  const username = document.getElementById('username').value.toLowerCase();
  const currentPassword = document.getElementById('password').value;

  const options = {
    method: 'POST',
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
    }),
    body: JSON.stringify({
      username,
      password: currentPassword,
    }),
  };
  const signInRequest = new Request(uri, options);

  fetch(signInRequest)
    .then((signInResponse) => {
      if (signInResponse.ok) {
        document.getElementById('fa-spin').style.display = 'none';
        document.getElementById('submit').value = 'Sign In';

        return signInResponse.json();
      }
      return signInResponse.json();
    })
    .then((signInData) => {
      if (Object.prototype.hasOwnProperty.call(signInData, 'message')) {
        if (Object.prototype.hasOwnProperty.call(signInData.message, 'password')) {
          document.getElementById('password').style.borderBottomColor = 'red';
        }
        if (Object.prototype.hasOwnProperty.call(signInData.message, 'username')) {
          document.getElementById('username').style.borderBottomColor = 'red';
        }
        if (signInData.message === 'password or username is invalid') {
          document.getElementById('username').style.borderBottomColor = 'red';
          document.getElementById('password').style.borderBottomColor = 'red';
          document.getElementById('error-message').innerHTML = signInData.message;
        }
        if (signInData.message === 'account has been disabled') {
          document.getElementById('error-message').innerHTML = signInData.message;
        }
      }
      if (Object.prototype.hasOwnProperty.call(signInData, 'data')) {
        document.getElementById('error-message').style.color = 'green';
        document.getElementById('error-message').innerHTML = 'Login successful';
        let othername = '';
        let phonenumber = '';

        const userData = signInData.data[0].user;
        const accessToken = signInData.data[0].token;
        if (userData.othernames != null) {
          othername = userData.othernames;
        } else {
          othername = '';
        }
        if (userData.phoneNumber != null) {
          phonenumber = userData.phoneNumber;
        } else {
          phonenumber = '';
        }
        const name = `${userData.firstname} ${userData.lastname} ${othername}`;

        localStorage.setItem('profileName', name);
        localStorage.setItem('profilePhoneNumber', phonenumber);
        localStorage.setItem('profileFirstName', userData.firstname);
        localStorage.setItem('profileLastName', userData.lastname);
        localStorage.setItem('profileOtherName', othername);
        localStorage.setItem('profileEmail', userData.email);
        localStorage.setItem('profileEmailVerified', userData.emailVerified);
        localStorage.setItem('profilePhotoUrl', userData.photourl);

        const expirationTime = 59;
        const date = new Date();
        const now = date.getTime();
        const expirationTimeMilliseconds = now + (expirationTime * 60000);
        localStorage.setItem('expiration', expirationTimeMilliseconds);
        localStorage.setItem('expirationTime', expirationTime);
        localStorage.setItem('logInTime', moment().format());

        setCookie('token', accessToken, expirationTime);
        setCookie('username', userData.username, expirationTime);
        setCookie('isAdmin', userData.isAdmin, expirationTime);
        setCookie('isLoggedIn', 'True', expirationTime);

        window.location.replace('home.html');
      }
    })
    .catch(() => {
      document.getElementById('error-message').innerText = 'An error has occurred please try again';
    });
};

const signUp = (event) => {
  event.preventDefault();
  document.getElementById('error-message').innerHTML = '';
  document.getElementById('firstname').style.borderBottomColor = 'white';
  document.getElementById('lastname').style.borderBottomColor = 'white';
  document.getElementById('username').style.borderBottomColor = 'white';
  document.getElementById('email').style.borderBottomColor = 'white';
  document.getElementById('password').style.borderBottomColor = 'white';
  document.getElementById('confirm_password').style.borderBottomColor = 'white';
  document.getElementById('error-message').style.color = 'red';
  document.getElementById('fa-spin').style.display = 'block';
  document.getElementById('submit').value = 'Signing Up';

  const uri = `${config.root}auth/signup`;

  const firstname = document.getElementById('firstname').value;
  const lastname = document.getElementById('lastname').value;
  const username = document.getElementById('username').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirm_password').value;

  const newUserData = {
    firstname,
    lastname,
    username,
    email,
    password,
  };

  if (password === confirmPassword) {
    const options = {
      method: 'POST',
      mode: 'cors',
      headers: new Headers({
        'Content-Type': 'application/json; charset=utf-8',
      }),
      body: JSON.stringify(newUserData),
    };
    const signUpRequest = new Request(uri, options);

    fetch(signUpRequest)
      .then((signUpResponse) => {
        if (signUpResponse.ok) {
          document.getElementById('fa-spin').style.display = 'none';
          document.getElementById('submit').value = 'Sign Up';

          return signUpResponse.json();
        }
        document.getElementById('fa-spin').style.display = 'none';
        document.getElementById('submit').value = 'Sign Up';
        return signUpResponse.json();
      })
      .then((signUpData) => {
        if (Object.prototype.hasOwnProperty.call(signUpData, 'message')) {
          if (Object.prototype.hasOwnProperty.call(signUpData.message, 'password')) {
            document.getElementById('error-message').innerHTML = signUpData.message.password;
            document.getElementById('password').style.borderBottomColor = 'red';
          }
          if (Object.prototype.hasOwnProperty.call(signUpData.message, 'firstname')) {
            document.getElementById('firstname').style.borderBottomColor = 'red';
          }
          if (Object.prototype.hasOwnProperty.call(signUpData.message, 'lastname')) {
            document.getElementById('lastname').style.borderBottomColor = 'red';
          }
          if (Object.prototype.hasOwnProperty.call(signUpData.message, 'username')) {
            document.getElementById('username').style.borderBottomColor = 'red';
          }
          if (Object.prototype.hasOwnProperty.call(signUpData.message, 'email')) {
            document.getElementById('email').style.borderBottomColor = 'red';
          }
          if (signUpData.message === 'email already exists') {
            document.getElementById('email').style.borderBottomColor = 'red';
            document.getElementById('error-message').innerHTML = signUpData.message;
          }
          if (signUpData.message === 'username already exists') {
            document.getElementById('username').style.borderBottomColor = 'red';
            document.getElementById('error-message').innerHTML = signUpData.message;
          }
          if (signUpData.message === 'You have been registered successfully') {
            document.getElementById('error-message').style.color = 'green';
            document.getElementById('error-message').innerHTML = signUpData.message;
            window.location.replace('signin.html');
          }
        }

        if (Object.prototype.hasOwnProperty.call(signUpData, 'data')) {
          window.location.replace('signin.html');
        }
      })
      .catch(() => {
        document.getElementById('error-message').innerText = 'An error has occurred please try again';
      });
  } else if (password !== confirmPassword) {
    document.getElementById('fa-spin').style.display = 'none';
    document.getElementById('submit').value = 'Sign Up';
    document.getElementById('error-message').innerHTML = 'Passwords do not match';
    document.getElementById('password').style.borderBottomColor = 'red';
    document.getElementById('confirm_password').style.borderBottomColor = 'red';
  }
};

const requestReset = (event) => {
  event.preventDefault();
  document.getElementById('error-message').innerHTML = '';
  document.getElementById('fa-spin').style.display = 'block';

  const useremail = document.getElementById('useremail').value;

  const uri = `${config.root}users/${useremail}/resetPassword`;
  const domain = config.resetlink;

  const options = {
    method: 'POST',
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
    }),
    body: JSON.stringify({
      resetlink: domain,
    }),
  };
  const resetRequest = new Request(uri, options);

  fetch(resetRequest)
    .then((requestResetResponse) => {
      if (requestResetResponse.ok) {
        document.getElementById('fa-spin').style.display = 'none';

        return requestResetResponse.json();
      }
      document.getElementById('fa-spin').style.display = 'none';
      return requestResetResponse.json();
    })
    .then((resetRequestData) => {
      const resetMessage = `If a user account exists for ${useremail}, an email will be sent with further instructions`;
      if (Object.prototype.hasOwnProperty.call(resetRequestData, 'message')) {
        if (Object.prototype.hasOwnProperty.call(resetRequestData.message, 'resetlink')) {
          document.getElementById('error-message').innerHTML = 'resetlink key is missing';
        }
        if (resetRequestData.message === 'user does not exist' || resetRequestData.message === 'Reset link has been sent to your email') {
          document.getElementById('error-message').style.color = 'green';
          document.getElementById('error-message').innerHTML = resetMessage;
          setTimeout(redirection, 5000);
        }
        if (resetRequestData.message === 'Password reset failed please try again') {
          document.getElementById('error-message').innerHTML = resetRequestData.message;
        }
      }
    })
    .catch(() => {
      document.getElementById('error-message').innerText = 'An error has occurred please try again';
    });
};

/* eslint-disable-next-line no-unused-vars */
const globalFunctionsLoggedIn = [signIn, signUp, requestReset];
