document.addEventListener('DOMContentLoaded', () => {
  const accordionItems = document.querySelectorAll('.toc__toggle');

  accordionItems.forEach((item) => {
    item.addEventListener('click', () => {
      const tocItem = item.closest('.toc__item');
      if (tocItem) {
        const childMenu = tocItem.querySelector('.toc__accordion');
        if (childMenu) {
          childMenu.classList.toggle('toc__accordion__expanded');
          item.classList.toggle('toc__toggle__expanded');
        }
      }
    });
  });
});
