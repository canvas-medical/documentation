// Create the expand icon SVG element
const createExpandIcon = () => {
  const svg = document.createElement("svg");
  svg.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
    <path d="M32 32C14.3 32 0 46.3 0 64v96c0 17.7 14.3 32 32 32s32-14.3 32-32V96h64c17.7 0 32-14.3 32-32s-14.3-32-32-32H32zM64 352c0-17.7-14.3-32-32-32s-32 14.3-32 32v96c0 17.7 14.3 32 32 32h96c17.7 0 32-14.3 32-32s-14.3-32-32-32H64V352zM320 32c-17.7 0-32 14.3-32 32s14.3 32 32 32h64v64c0 17.7 14.3 32 32 32s32-14.3 32-32V64c0-17.7-14.3-32-32-32H320zM448 352c0-17.7-14.3-32-32-32s-32 14.3-32 32v64H320c-17.7 0-32 14.3-32 32s14.3 32 32 32h96c17.7 0 32-14.3 32-32V352z"/>
  </svg>`;
  return svg;
};

// Create the clipboard icon SVG element
const createClipboardIcon = () => {
  const svg = document.createElement("svg");
  svg.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512">
    <path d="M384 112v352c0 26.51-21.49 48-48 48H48c-26.51 0-48-21.49-48-48V112c0-26.51 21.49-48 48-48h80c0-35.29 28.71-64 64-64s64 28.71 64 64h80c26.51 0 48 21.49 48 48zM192 40c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24m96 114v-20a6 6 0 0 0-6-6H102a6 6 0 0 0-6 6v20a6 6 0 0 0 6 6h180a6 6 0 0 0 6-6z"/>
  </svg>`;
  return svg;
};

// Find all div.highlighter-rouge elements and add the clipboard and expand icons
const highlighterRougeDivs = document.querySelectorAll("div.highlighter-rouge");
highlighterRougeDivs.forEach((div) => {
  // Create the parent toolbar div
  const toolbarDiv = document.createElement("div");
  toolbarDiv.classList.add("rogue__toolbar");

  // Add the expand icon
  const expandIconDiv = document.createElement("div");
  expandIconDiv.classList.add("rogue__expand");
  expandIconDiv.appendChild(createExpandIcon());
  toolbarDiv.appendChild(expandIconDiv);

  // Add the clipboard icon
  const clipboardIconDiv = document.createElement("div");
  clipboardIconDiv.classList.add("rogue__copy");
  clipboardIconDiv.appendChild(createClipboardIcon());
  toolbarDiv.appendChild(clipboardIconDiv);

  // Prepend the toolbar to the highlighter-rouge div
  div.prepend(toolbarDiv);

  // Add click event listener to the clipboard icon
  clipboardIconDiv.addEventListener("click", () => {
    const codeElement = div.querySelector("code");
    if (codeElement) {
      const textToCopy = codeElement.textContent;
      navigator.clipboard.writeText(textToCopy)
        .catch((error) => {
          console.error("Unable to copy text to clipboard:", error);
        });
    }
  });

  // Add click event listener to the expand icon
  expandIconDiv.addEventListener("click", () => {
    div.classList.toggle("rogue__expanded");
  });
});

