const toggleSidenav = () => {
  const sidenav = document.querySelector('.sidenav__toggle');
  if (sidenav) {
    sidenav.addEventListener('click', () => {
      sidenav.parentNode.classList.toggle('sidenav__collapsed');
    });
  }
};
toggleSidenav();

const toggleNav = () => {
  const nav = document.querySelector('.navigation__wrapper');
  const toggle = document.querySelector('.navigation__toggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('navigation__toggle__expanded');
      toggle.classList.toggle('navigation__toggle__collapsed');
      nav.classList.toggle('navigation__wrapper__expanded');
    });
  }
};
toggleNav();
