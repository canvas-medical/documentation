const toggleSidenav = () => {
  const sidenav = document.querySelector('.sidenav__toggle');
  const sidenavoutter = document.querySelector('.sidenavtoc');
  const divv = document.querySelector('.navsidetogle');
  const mediaQuery = window.matchMedia('(max-width: 576px)');
  const divvsidenav = document.querySelector('.sidenav');
  if (sidenavoutter) {
    divv.style.visibility = 'visible';
    sidenavoutter.classList.add('sidenav__collapsed');
  }
  if (sidenav) {
    sidenav.addEventListener('click', () => {
      sidenavoutter.classList.toggle('sidenav__collapsed');
      divv.classList.toggle('open');
      sidenavoutter.parentElement.classList.toggle('overflowhiddenX')
      
    });
  }
};
toggleSidenav();

const toggleNav = () => {
  const nav = document.querySelector('.navigation__wrapper');
  const toggle = document.querySelector('.navigation__toggle');
  const navHeight = document.querySelector('.navigation__toggle__collapsed');

  if (toggle) {
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('navigation__toggle__expanded');
      toggle.classList.toggle('navigation__toggle__collapsed');
      nav.classList.toggle('navigation__wrapper__expanded');
      navHeight.parentElement.style.height = 'auto';
    });
  }
};
toggleNav();
