const setViewportHeightAsCSSVariable = () => {
  // Get the height of the viewport
  const viewportHeight = window.innerHeight || document.documentElement.clientHeight;

  // Set the viewport height as a CSS variable
  document.documentElement.style.setProperty('--viewport-height', `${viewportHeight}px`);
};

// Call the function initially to set the CSS variable
setViewportHeightAsCSSVariable();

// Recalculate and update the CSS variable when the viewport is resized
window.addEventListener('resize', setViewportHeightAsCSSVariable);
