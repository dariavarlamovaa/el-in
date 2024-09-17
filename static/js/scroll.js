const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const picturesBlock = document.querySelector('.pictures');

function checkButtonsVisibility() {
    if (picturesBlock.scrollLeft === 0) {
        prevBtn.style.visibility = 'hidden';
    } else {
        prevBtn.style.visibility = 'visible';
    }

    if (picturesBlock.scrollLeft + picturesBlock.clientWidth >= picturesBlock.scrollWidth) {
        nextBtn.style.visibility = 'hidden';
    } else {
        nextBtn.style.visibility = 'visible';
    }
}

prevBtn.addEventListener('click', () => {
    picturesBlock.scrollLeft -= 420;
})

nextBtn.addEventListener('click', () => {
    picturesBlock.scrollLeft += 420;
})

picturesBlock.addEventListener('scroll', checkButtonsVisibility);

window.onload = checkButtonsVisibility;