// Get all the anchor links in the list
const anchorLinks = document.querySelectorAll('.anchorlist__item a');

// Options for the Intersection Observer
const observerOptions = {
  rootMargin: '0px',
  threshold: 1.0
};

let activeLink = null;

// Create a new Intersection Observer
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    const headingId = entry.target.getAttribute('id');
    const correspondingLink = document.querySelector(`.anchorlist__item a[href="#${headingId}"]`);

    if (entry.isIntersecting) {
      // If a heading is in view, update the active link
      activeLink = correspondingLink;
    }
  });

  // Remove the active class from all links
  anchorLinks.forEach((link) => {
    link.classList.remove('anchorlist__item__active');
  });

  // Add the active class to the last observed active link
  if (activeLink) {
    activeLink.classList.add('anchorlist__item__active');
  }
}, observerOptions);

// Observe each heading level (H2, H3, H4)
const headings = document.querySelectorAll('article h2, article h3, article h4');
headings.forEach((heading) => {
  observer.observe(heading);
});
