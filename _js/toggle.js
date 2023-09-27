const toggleSidenav = () => {
  const sidenav = document.querySelector('.sidenav__toggle');
  const sidenavoutter = document.querySelector('.sidenavtoc');
  const divv = document.querySelector('.navsidetogle');
  if (sidenavoutter) {
    divv.style.visibility = 'visible';
    sidenavoutter.classList.add('sidenav__collapsed');
  }
  if (sidenav) {
    sidenav.addEventListener('click', () => {
      sidenavoutter.classList.toggle('sidenav__collapsed');
      divv.classList.toggle('open');
      sidenavoutter.parentElement.classList.toggle('overflowhiddenX');
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

const toggleSearch = () => {
  const searchbutton = document.querySelector('.search__toggle');
  const searchPanel = document.querySelector('.searchmain');
  const overlay = document.getElementById('search-overlay');

  if (searchbutton) {
    searchbutton.addEventListener('click', () => {
      searchPanel.classList.toggle('toogle_searchmain');
      overlay.classList.toggle('search-overlay__toggle');

      const searchInput = document.querySelector('.ais-SearchBox-input');

      if (searchInput) {
        searchInput.focus();
      }
    });
  }

  if (overlay) {
    overlay.addEventListener('click', () => {
      searchPanel.classList.remove('toogle_searchmain');
      overlay.classList.remove('search-overlay__toggle');
    });
  }
};
toggleSearch();
