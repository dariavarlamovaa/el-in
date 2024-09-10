let scrollContainer = document.querySelector('.pictures')
let prevBtn = document.getElementById('prevBtn')
let nextBtn = document.getElementById('nextBtn')

prevBtn.addEventListener('click', () => {
        scrollContainer.scrollLeft -= 420;
    }
)

nextBtn.addEventListener('click', () => {
        scrollContainer.scrollLeft += 420;
    }
)