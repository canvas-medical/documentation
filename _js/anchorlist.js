// Get all the anchor links in the list
const anchorLinks = document.querySelectorAll('.anchorlist__item a');

// Options for the Intersection Observer
const observerOptions = {
  rootMargin: '-20% 0px -70% 0px', // Only trigger when heading is in upper portion of viewport
  threshold: [0, 0.1, 0.5, 1.0] // Multiple thresholds for better detection
};

let activeLink = null;
let hashChangeTimeout = null;
let ignoreObserverUpdates = false;

// Function to set active link
function setActiveLink(link) {
  // Remove active class from all links
  anchorLinks.forEach((l) => {
    l.classList.remove('anchorlist__item__active');
  });
  // Add active class to the target link
  if (link) {
    link.classList.add('anchorlist__item__active');
    activeLink = link;
  }
}

// Function to set active link based on hash
function setActiveLinkFromHash() {
  const hash = window.location.hash;
  if (hash) {
    const targetLink = document.querySelector(`.anchorlist__item a[href="${hash}"]`);
    if (targetLink) {
      setActiveLink(targetLink);
      // Temporarily ignore observer updates to allow scroll to complete
      ignoreObserverUpdates = true;
      // Clear any existing timeout
      if (hashChangeTimeout) {
        clearTimeout(hashChangeTimeout);
      }
      // Re-enable observer updates after scroll completes
      hashChangeTimeout = setTimeout(() => {
        ignoreObserverUpdates = false;
      }, 500);
    }
  }
}

// Set active link on page load based on hash
setActiveLinkFromHash();

// Listen for hash changes (when clicking anchor links)
window.addEventListener('hashchange', () => {
  setActiveLinkFromHash();
});

// Create a new Intersection Observer
const observer = new IntersectionObserver((entries) => {
  // Ignore updates immediately after hash change
  if (ignoreObserverUpdates) {
    return;
  }

  const currentHash = window.location.hash;
  
  // If there's a hash in the URL, only update if the hash-matched heading is intersecting
  if (currentHash) {
    // Find the heading that matches the hash
    const hashHeading = document.querySelector(currentHash);
    if (hashHeading) {
      // Check if this heading is in the entries and intersecting
      const hashEntry = entries.find(entry => entry.target === hashHeading && entry.isIntersecting);
      if (hashEntry) {
        const headingId = hashHeading.getAttribute('id');
        const correspondingLink = document.querySelector(`.anchorlist__item a[href="#${headingId}"]`);
        if (correspondingLink) {
          setActiveLink(correspondingLink);
        }
      }
      // If hash heading is not intersecting, don't update (keep hash-based selection)
      return;
    }
  }

  // No hash or hash heading not found - use normal intersection logic
  const intersectingEntries = [];
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      intersectingEntries.push(entry);
    }
  });

  if (intersectingEntries.length > 0) {
    // Sort by position (top to bottom)
    intersectingEntries.sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    const topEntry = intersectingEntries[0];
    const headingId = topEntry.target.getAttribute('id');
    const correspondingLink = document.querySelector(`.anchorlist__item a[href="#${headingId}"]`);
    if (correspondingLink) {
      setActiveLink(correspondingLink);
    }
  }
}, observerOptions);

// Observe each heading level (H2, H3, H4)
const headings = document.querySelectorAll('article h2, article h3, article h4');
headings.forEach((heading) => {
  observer.observe(heading);
});
