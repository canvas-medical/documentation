const toggleSidenav = () => {
  const sidenav = document.querySelector('.sidenav__toggle');
  if (sidenav) {
    sidenav.addEventListener('click', () => {
      sidenav.parentNode.classList.toggle('sidenav__collapsed');
    });
  }
};
toggleSidenav();
