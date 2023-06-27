const toggleBtn = document.querySelector('.navbar__toogleBtn');
const icons = document.querySelector('.navbar__icons');

toggleBtn.addEventListener('click', () => {
    icons.classList.toggle('active');
});
