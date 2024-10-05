const burgerIcon = document.getElementById('burger-icon')

burgerIcon.addEventListener('click', function () {
    console.log('hi')
    let menu = document.querySelector('.menu');
    let languages = document.querySelector('.languages');
    menu.classList.toggle('show');
    languages.classList.toggle('show');

});