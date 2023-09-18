const toggleSidenav = () => {
  const sidenav = document.querySelector('.sidenav__toggle');
  if (sidenav) {
    sidenav.addEventListener('click', () => {
      sidenav.parentNode.classList.toggle('sidenav__collapsed');
    });
  }
};
toggleSidenav();

const toggleSearch = () => {
  const searchbutton = document.querySelector('.search__toggle');
  const searchPanel = document.querySelector('.searchmain');  
  const overlay = document.getElementById('search-overlay');

  if (searchbutton) {
    searchbutton.addEventListener('click', () => {
      searchPanel.classList.toggle('toogle_searchmain');
      overlay.classList.toggle('search-overlay__toggle');
      if (overlay) {
      overlay.addEventListener('click', () => {
        searchPanel.classList.remove('toogle_searchmain');
        overlay.classList.remove('search-overlay__toggle');
       });
      }

     
    });
  }
};
toggleSearch();
