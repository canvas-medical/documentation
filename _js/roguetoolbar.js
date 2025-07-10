// Create the icon SVG element
const createIcon = (path) => {
  const svg = document.createElement('svg');
  svg.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
    ${path}
  </svg>`;
  return svg;
};

// Create the expand icon SVG element
const createExpandIcon = () => {
  const path = '<path d="M32 32C14.3 32 0 46.3 0 64v96c0 17.7 14.3 32 32 32s32-14.3 32-32V96h64c17.7 0 32-14.3 32-32s-14.3-32-32-32H32zM64 352c0-17.7-14.3-32-32-32s-32 14.3-32 32v96c0 17.7 14.3 32 32 32h96c17.7 0 32-14.3 32-32s-14.3-32-32-32H64V352zM320 32c-17.7 0-32 14.3-32 32s14.3 32 32 32h64v64c0 17.7 14.3 32 32 32s32-14.3 32-32V64c0-17.7-14.3-32-32-32H320zM448 352c0-17.7-14.3-32-32-32s-32 14.3-32 32v64H320c-17.7 0-32 14.3-32 32s14.3 32 32 32h96c17.7 0 32-14.3 32-32V352z"/>';
  return createIcon(path);
};

// Path for a clipboard SVG element
const clipboardIconPath = '<path d="M208 0L332.1 0c12.7 0 24.9 5.1 33.9 14.1l67.9 67.9c9 9 14.1 21.2 14.1 33.9L448 336c0 26.5-21.5 48-48 48l-192 0c-26.5 0-48-21.5-48-48l0-288c0-26.5 21.5-48 48-48zM48 128l80 0 0 64-64 0 0 256 192 0 0-32 64 0 0 48c0 26.5-21.5 48-48 48L48 512c-26.5 0-48-21.5-48-48L0 176c0-26.5 21.5-48 48-48z"/>';

// Path for a checkbox SVG element
const copySuccessIconPath = '<path d="M128 64c0-35.3 28.7-64 64-64L352 0l0 128c0 17.7 14.3 32 32 32l128 0 0 288c0 35.3-28.7 64-64 64l-256 0c-35.3 0-64-28.7-64-64l0-112 174.1 0-39 39c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0l80-80c9.4-9.4 9.4-24.6 0-33.9l-80-80c-9.4-9.4-24.6-9.4-33.9 0s-9.4 24.6 0 33.9l39 39L128 288l0-224zm0 224l0 48L24 336c-13.3 0-24-10.7-24-24s10.7-24 24-24l104 0zM512 128l-128 0L384 0 512 128z"/>';

// Create the clipboard icon SVG element
const createClipboardIcon = () => {
  return createIcon(clipboardIconPath);
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

  // Add click event listener to the clipboard icon
  clipboardIconDiv.addEventListener('click', (e) => {
    const codeElement = div.querySelector('code');
    if (codeElement) {
      const textToCopy = codeElement.textContent;
      navigator.clipboard.writeText(textToCopy).catch((error) => {
        console.error('Unable to copy text to clipboard:', error);
        return;
      });
    }

    const copyButtonSvg = e.currentTarget.querySelector('svg > svg')
    copyButtonSvg.innerHTML = copySuccessIconPath;
    setTimeout(() => {
      copyButtonSvg.innerHTML = clipboardIconPath;
    }, 1000);
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

