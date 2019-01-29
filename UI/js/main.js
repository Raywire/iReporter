const mainNav = document.getElementById('js-menu');
const navBarToggle = document.getElementById('js-navbar-toggle');
const activeToggle = () => {
  mainNav.classList.toggle('active');
};

navBarToggle.addEventListener('click', activeToggle);
