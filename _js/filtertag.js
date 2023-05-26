const filterLinks = document.querySelectorAll('.filtertag__link');
const items = document.querySelectorAll('.filtertag__item');

filterLinks.forEach(link => {
  link.addEventListener('click', event => {
    event.preventDefault();

    const filterTag = link.getAttribute('filter-tag');
    const isActive = link.classList.contains('filtertag__link__active');

    // Toggle active class
    link.classList.toggle('filtertag__link__active');

    const activeFilterLinks = document.querySelectorAll('.filtertag__link.filtertag__link__active');
    const activeFilterTags = Array.from(activeFilterLinks).map(activeLink => activeLink.getAttribute('filter-tag'));

    items.forEach(item => {
      const dataTags = item.getAttribute('data-tag').split(',').map(tag => tag.trim());

      if (activeFilterTags.length === 0 || activeFilterTags.every(tag => dataTags.includes(tag))) {
        item.classList.remove('filtertag__item__hidden');
      } else {
        item.classList.add('filtertag__item__hidden');
      }
    });
  });
});