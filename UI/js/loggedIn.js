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
  const password = document.getElementById('password').value;

  const options = {
    method: 'POST',
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
    }),
    body: JSON.stringify({
      username,
      password,
    }),
  };
  const request = new Request(uri, options);

  fetch(request)
    .then((response) => {
      if (response.ok) {
        document.getElementById('fa-spin').style.display = 'none';
        document.getElementById('submit').value = 'Sign In';

        return response.json();
      }
      document.getElementById('fa-spin').style.display = 'none';
      document.getElementById('submit').value = 'Sign In';
      return response.json();
    })
    .then((j) => {
      if (Object.prototype.hasOwnProperty.call(j, 'message')) {
        if (Object.prototype.hasOwnProperty.call(j.message, 'password')) {
          document.getElementById('password').style.borderBottomColor = 'red';
        }
        if (Object.prototype.hasOwnProperty.call(j.message, 'username')) {
          document.getElementById('username').style.borderBottomColor = 'red';
        }
        if (j.message === 'password or username is invalid') {
          document.getElementById('username').style.borderBottomColor = 'red';
          document.getElementById('password').style.borderBottomColor = 'red';
          document.getElementById('error-message').innerHTML = j.message;
        }
        if (j.message === 'account has been disabled') {
          document.getElementById('error-message').innerHTML = j.message;
        }
      }
      if (Object.prototype.hasOwnProperty.call(j, 'data')) {
        document.getElementById('error-message').style.color = 'green';
        document.getElementById('error-message').innerHTML = 'Login successful';
        let othername = '';
        let phonenumber = '';

        const userData = j.data[0].user;
        const accessToken = j.data[0].token;
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

        setCookie('token', accessToken, expirationTime);
        setCookie('username', userData.username, expirationTime);
        setCookie('isAdmin', userData.isAdmin, expirationTime);
        setCookie('isLoggedIn', 'True', expirationTime);

        window.location.replace('home.html');
      }
    })
    .catch((err) => {
      console.log(err);
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

  const data = {
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
      body: JSON.stringify(data),
    };
    const request = new Request(uri, options);

    fetch(request)
      .then((response) => {
        if (response.ok) {
          document.getElementById('fa-spin').style.display = 'none';
          document.getElementById('submit').value = 'Sign Up';

          return response.json();
        }
        document.getElementById('fa-spin').style.display = 'none';
        document.getElementById('submit').value = 'Sign Up';
        return response.json();
      })
      .then((j) => {
        if (Object.prototype.hasOwnProperty.call(j, 'message')) {
          if (Object.prototype.hasOwnProperty.call(j.message, 'password')) {
            document.getElementById('error-message').innerHTML = j.message.password;
            document.getElementById('password').style.borderBottomColor = 'red';
          }
          if (Object.prototype.hasOwnProperty.call(j.message, 'firstname')) {
            document.getElementById('firstname').style.borderBottomColor = 'red';
          }
          if (Object.prototype.hasOwnProperty.call(j.message, 'lastname')) {
            document.getElementById('lastname').style.borderBottomColor = 'red';
          }
          if (Object.prototype.hasOwnProperty.call(j.message, 'username')) {
            document.getElementById('username').style.borderBottomColor = 'red';
          }
          if (Object.prototype.hasOwnProperty.call(j.message, 'email')) {
            document.getElementById('email').style.borderBottomColor = 'red';
          }
          if (j.message === 'email already exists') {
            document.getElementById('email').style.borderBottomColor = 'red';
            document.getElementById('error-message').innerHTML = j.message;
          }
          if (j.message === 'username already exists') {
            document.getElementById('username').style.borderBottomColor = 'red';
            document.getElementById('error-message').innerHTML = j.message;
          }
          if (j.message === 'You have been registered successfully') {
            document.getElementById('error-message').style.color = 'green';
            document.getElementById('error-message').innerHTML = j.message;
            window.location.replace('signin.html');
          }
        }

        if (Object.prototype.hasOwnProperty.call(j, 'data')) {
          window.location.replace('signin.html');
        }
      })
      .catch((error) => {
        console.log(error);
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

  const options = {
    method: 'POST',
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
    }),
    body: JSON.stringify({
      resetlink: config.resetlink,
    }),
  };
  const request = new Request(uri, options);

  fetch(request)
    .then((response) => {
      if (response.ok) {
        document.getElementById('fa-spin').style.display = 'none';

        return response.json();
      }
      document.getElementById('fa-spin').style.display = 'none';
      return response.json();
    })
    .then((j) => {
      const resetMessage = `If a user account exists for ${useremail}, an email will be sent with further instructions`;
      if (Object.prototype.hasOwnProperty.call(j, 'message')) {
        if (Object.prototype.hasOwnProperty.call(j.message, 'resetlink')) {
          document.getElementById('error-message').innerHTML = 'resetlink key is missing';
        }
        if (j.message === 'user does not exist') {
          document.getElementById('error-message').style.color = 'green';
          document.getElementById('error-message').innerHTML = resetMessage;
          setTimeout(redirection, 5000);
        }
        if (j.message === 'Reset link has been sent to your email') {
          document.getElementById('error-message').style.color = 'green';
          document.getElementById('error-message').innerHTML = resetMessage;
          setTimeout(redirection, 5000);
        }
        if (j.message === 'Password reset failed please try again') {
          document.getElementById('error-message').innerHTML = j.message;
        }
      }
    })
    .catch((err) => {
      console.log(err);
    });
};
