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
