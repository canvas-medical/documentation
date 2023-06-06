// Create a fullscreen button for each parent element
const parentElements = document.querySelectorAll('div.highlighter-rouge');
parentElements.forEach((parentElement) => {
  const fullscreenButton = document.createElement('div');
  fullscreenButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 448 512"><path d="M32 32C14.3 32 0 46.3 0 64v96c0 17.7 14.3 32 32 32s32-14.3 32-32V96h64c17.7 0 32-14.3 32-32s-14.3-32-32-32H32zM64 352c0-17.7-14.3-32-32-32s-32 14.3-32 32v96c0 17.7 14.3 32 32 32h96c17.7 0 32-14.3 32-32s-14.3-32-32-32H64V352zM320 32c-17.7 0-32 14.3-32 32s14.3 32 32 32h64v64c0 17.7 14.3 32 32 32s32-14.3 32-32V64c0-17.7-14.3-32-32-32H320zM448 352c0-17.7-14.3-32-32-32s-32 14.3-32 32v64H320c-17.7 0-32 14.3-32 32s14.3 32 32 32h96c17.7 0 32-14.3 32-32V352z"/></svg>';

  // Add click event listener
  fullscreenButton.addEventListener('click', () => {
    const modalContentWrapper = document.createElement('div');
    modalContentWrapper.classList.add('highlighter-rouge');
    modalContentWrapper.innerHTML = parentElement.innerHTML;

    const closeIcon = document.createElement('span');
    closeIcon.classList.add('rogue__modal__close');
    closeIcon.innerHTML = '&times;';
    closeIcon.addEventListener('click', () => {
      document.body.removeChild(fullscreenModal);
      document.documentElement.style.overflow = ''; // Re-enable scrolling on the main page
    });

    const fullscreenModal = document.createElement('div');
    fullscreenModal.classList.add('rogue__modal');
    fullscreenModal.appendChild(modalContentWrapper);
    fullscreenModal.appendChild(closeIcon);

    document.body.appendChild(fullscreenModal);
    document.documentElement.style.overflow = 'hidden'; // Disable scrolling on the main page
    fullscreenModal.style.display = 'block';
  });

  // Append fullscreen button to parent element
  const fullscreenButtonContainer = document.createElement('div');
  fullscreenButtonContainer.classList.add('rogue__modal__open');
  fullscreenButtonContainer.appendChild(fullscreenButton);
  parentElement.insertBefore(fullscreenButtonContainer, parentElement.firstChild);
});
