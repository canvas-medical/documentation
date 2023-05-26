const filterLinks = document.querySelectorAll('.filterdate__link');
const items = document.querySelectorAll('.filterdate__item');

filterLinks.forEach(link => {
  link.addEventListener('click', event => {
    event.preventDefault();

    const filterDate = link.getAttribute('filter-date');
    const isActive = link.classList.contains('filterdate__link__active');

    // Reset active classes
    filterLinks.forEach(otherLink => {
      otherLink.classList.remove('filterdate__link__active');
    });

    if (!isActive) {
      link.classList.add('filterdate__link__active');

      items.forEach(item => {
        const itemDate = item.getAttribute('data-date');

        if (itemDate === filterDate) {
          item.classList.remove('filterdate__item__hidden');
        } else {
          item.classList.add('filterdate__item__hidden');
        }
      });
    } else {
      // Show all items when filter is unselected
      items.forEach(item => {
        item.classList.remove('filterdate__item__hidden');
      });
    }
  });
});
