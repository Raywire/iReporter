let isLoggedIn = getCookie('isLoggedIn');

if (isLoggedIn === 'True'){
    window.location.replace("home.html");
}