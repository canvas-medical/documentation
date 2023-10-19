// Create the icon SVG element
const createIcon = (path) => {
  const svg = document.createElement('svg');
  svg.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
    ${path}
  </svg>`;
  return svg;
};

// Create the expand icon SVG element
const createExpandIcon = () => {
  const path = '<path d="M32 32C14.3 32 0 46.3 0 64v96c0 17.7 14.3 32 32 32s32-14.3 32-32V96h64c17.7 0 32-14.3 32-32s-14.3-32-32-32H32zM64 352c0-17.7-14.3-32-32-32s-32 14.3-32 32v96c0 17.7 14.3 32 32 32h96c17.7 0 32-14.3 32-32s-14.3-32-32-32H64V352zM320 32c-17.7 0-32 14.3-32 32s14.3 32 32 32h64v64c0 17.7 14.3 32 32 32s32-14.3 32-32V64c0-17.7-14.3-32-32-32H320zM448 352c0-17.7-14.3-32-32-32s-32 14.3-32 32v64H320c-17.7 0-32 14.3-32 32s14.3 32 32 32h96c17.7 0 32-14.3 32-32V352z"/>';
  return createIcon(path);
};

// Create the clipboard icon SVG element
const createClipboardIcon = () => {
  const path = '<path d="M384 112v352c0 26.51-21.49 48-48 48H48c-26.51 0-48-21.49-48-48V112c0-26.51 21.49-48 48-48h80c0-35.29 28.71-64 64-64s64 28.71 64 64h80c26.51 0 48 21.49 48 48zM192 40c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24m96 114v-20a6 6 0 0 0-6-6H102a6 6 0 0 0-6 6v20a6 6 0 0 0 6 6h180a6 6 0 0 0 6-6z"/>';
  return createIcon(path);
};

// Find all div.highlighter-rouge elements and add the clipboard and expand icons
const highlighterRougeDivs = document.querySelectorAll('div.highlighter-rouge');
highlighterRougeDivs.forEach((div) => {
  // Create the parent toolbar div
  const toolbarDiv = document.createElement('div');
  toolbarDiv.classList.add('rogue__toolbar');

  // Add the expand and clipboard icons
  const expandIconDiv = document.createElement('div');
  expandIconDiv.classList.add('rogue__expand');
  expandIconDiv.appendChild(createExpandIcon());
  toolbarDiv.appendChild(expandIconDiv);

  const clipboardIconDiv = document.createElement('div');
  clipboardIconDiv.classList.add('rogue__copy');
  clipboardIconDiv.appendChild(createClipboardIcon());
  toolbarDiv.appendChild(clipboardIconDiv);

  // Prepend the toolbar to the highlighter-rouge div
  div.prepend(toolbarDiv);
  console.log(toolbarDiv);

  // Add click event listener to the clipboard icon
  clipboardIconDiv.addEventListener('click', () => {
    const codeElement = div.querySelector('code');
    if (codeElement) {
      const textToCopy = codeElement.textContent;
      navigator.clipboard.writeText(textToCopy).catch((error) => {
        console.error('Unable to copy text to clipboard:', error);
      });
    }
  });

  

  // Add click event listener to the expand icon
  expandIconDiv.addEventListener('click', () => {
    const codeElement = div.querySelector('code');
    if (codeElement) {
      const content = codeElement.innerHTML;

      // Create the modal window
      const modal = document.createElement('div');
      modal.classList.add('rogue__modal');

      // Create the modal content
      const modalContent = document.createElement('div');
      modalContent.classList.add('rogue__modal__content');

      // Create the wrapper div.highlighter-rouge
      const highlighterRouge = document.createElement('div');
      highlighterRouge.classList.add('highlighter-rouge');

      // Create the inner div.highlight
      const innerHighlight = document.createElement('div');
      innerHighlight.classList.add('highlight');

      // Create the pre.highlight
      const preHighlight = document.createElement('pre');
      preHighlight.classList.add('highlight');
      preHighlight.innerHTML = content;

      // Append the pre.highlight to the inner div.highlight
      innerHighlight.appendChild(preHighlight);

      // Append the inner div.highlight to the wrapper div.highlighter-rouge
      highlighterRouge.appendChild(innerHighlight);

      // Append the wrapper div to the modal content
      modalContent.appendChild(highlighterRouge);

      // Create the close button
      const closeButton = document.createElement('span');
      closeButton.classList.add('rogue__modal__close');
      closeButton.innerHTML = '&times;'; // Close symbol

      // Add click event listener to close the modal
      closeButton.addEventListener('click', () => {
        document.body.removeChild(modal);
      });

      // Append the close button to the modal content
      modalContent.appendChild(closeButton);

      // Append the modal content to the modal window
      modal.appendChild(modalContent);

      // Append the modal window to the document body
      document.body.appendChild(modal);
    }
  });
});

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


// ** TROUBLESHOOTING CLICK NOT WORKING ON API PAGES


// document.querySelectorAll('li').forEach((item, index) => {
//   const ele = item.querySelector('div.rogue__toolbar');
//   if (ele) {
//     ele.addEventListener('click', () => {
//       const codeElement = div.querySelector('code');
//       if (codeElement) {
//         const content = codeElement.innerHTML;

//         // Create the modal window
//         const modal = document.createElement('div');
//         modal.classList.add('rogue__modal');

//         // Create the modal content
//         const modalContent = document.createElement('div');
//         modalContent.classList.add('rogue__modal__content');

//         // Create the wrapper div.highlighter-rouge
//         const highlighterRouge = document.createElement('div');
//         highlighterRouge.classList.add('highlighter-rouge');

//         // Create the inner div.highlight
//         const innerHighlight = document.createElement('div');
//         innerHighlight.classList.add('highlight');

//         // Create the pre.highlight
//         const preHighlight = document.createElement('pre');
//         preHighlight.classList.add('highlight');
//         preHighlight.innerHTML = content;

//         // Append the pre.highlight to the inner div.highlight
//         innerHighlight.appendChild(preHighlight);

//         // Append the inner div.highlight to the wrapper div.highlighter-rouge
//         highlighterRouge.appendChild(innerHighlight);

//         // Append the wrapper div to the modal content
//         modalContent.appendChild(highlighterRouge);

//         // Create the close button
//         const closeButton = document.createElement('span');
//         closeButton.classList.add('rogue__modal__close');
//         closeButton.innerHTML = '&times;'; // Close symbol

//         // Add click event listener to close the modal
//         closeButton.addEventListener('click', () => {
//           document.body.removeChild(modal);
//         });

//         // Append the close button to the modal content
//         modalContent.appendChild(closeButton);

//         // Append the modal content to the modal window
//         modal.appendChild(modalContent);

//         // Append the modal window to the document body
//         document.body.appendChild(modal);
//       }
//     });
//   }
// });

