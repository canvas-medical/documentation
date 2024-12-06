document.addEventListener('DOMContentLoaded', () => {
  // Get the scrollable container and the side panel element
  const scrollableWrapperContainer = document.querySelector('.pagelayout__centerdocs__wrapper');
  const sidePanel = document.querySelector('.sidepanels');

  if (!scrollableWrapperContainer || !sidePanel) { return; }

  // Listen for scroll events on the wrapper container
  scrollableWrapperContainer.addEventListener('scroll', function() {

    const offsetTop = 20; // Adjust this value to set the top spacing
    const scrollPosition = scrollableWrapperContainer.scrollTop; // Get the scroll position of the wrapper

    // Set the top position dynamically based on the scroll position
    if (scrollPosition > offsetTop) {
      sidePanel.style.top = `${offsetTop}px`; // Maintain offset from the top
    } else {
      sidePanel.style.top = '0px'; // Reset the top position
    }
  });
});