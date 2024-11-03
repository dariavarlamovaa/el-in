const burgerMenu = document.getElementById('burger-menu')
const header = document.querySelector('.header')
const body = document.querySelector('body')

burgerMenu.addEventListener('click', function () {
    let menuLang = document.querySelector('.menu-lang')
    let menu = document.querySelector('.menu');
    let languages = document.querySelector('.languages');
    burgerMenu.classList.toggle('active')
    body.classList.toggle('menu-open');
    header.classList.toggle('full-page')
    menuLang.classList.toggle('show')
    menu.classList.toggle('show');
    languages.classList.toggle('show');

});