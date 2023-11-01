document.addEventListener('DOMContentLoaded', () => {
  const scrollPosition = localStorage.getItem('scroll-position-side-nav');
  const sideNav = document.querySelector('.sidenav');

  if (scrollPosition && sideNav) {
    sideNav.scrollTo(0, parseFloat(scrollPosition));
  }
});

window.addEventListener('beforeunload', () => {
  const sideNav = document.querySelector('.sidenav');

  if (sideNav) {
    localStorage.setItem('scroll-position-side-nav', sideNav.scrollTop);
  }
});
