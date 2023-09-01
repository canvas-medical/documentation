const toggles = document.querySelectorAll('.apidoc__object__children__toggle');
let i;

for (i = 0; i < toggles.length; i++) {
  toggles[i].addEventListener('click', function () {
    this.classList.toggle('is-active');
    if (this.classList.contains('is-active')) {
      this.innerHTML = 'Child attributes';
      this.parentElement.style.border = '2px solid #f5f5f5';
      this.style.display = 'block';
    } else {
      this.innerHTML = 'Click to view child attributes';
      this.parentElement.style.border = '0px solid #f5f5f5';
      this.style.display = 'block';
    }
    const panel = this.nextElementSibling;
    if (panel.style.display === 'block') {
      panel.style.display = 'none';
    } else {
      panel.style.display = 'block';
    }
  });

}
