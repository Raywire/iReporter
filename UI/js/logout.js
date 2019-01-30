const logout = () => {
  document.cookie = 'token=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/;';
  document.cookie = 'username=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/;';
  document.cookie = 'isAdmin=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/;';
  document.cookie = 'isLoggedIn=False;path=/;sameSite=Strict';
  localStorage.clear();
  window.location.replace('signin.html');
};

document.getElementById('logout').addEventListener('click', logout);
