const toggleSidenav = () => {
  const sidenav = document.querySelector('.pagelayout__docpanels__sidenav__toggle');
  if (sidenav) {
    sidenav.addEventListener('click', () => {
      sidenav.parentNode.classList.toggle('pagelayout__docpanels__sidenav__collapsed');
    });
  }
};
toggleSidenav();
