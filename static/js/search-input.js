const searchImg = document.getElementById('search-img')
const searchInput = document.getElementById('search-input')

searchImg.addEventListener('click', function () {
    if (searchInput.style.display === "none") {
        searchInput.style.display = "block";
    } else {
        searchInput.style.display = "none";
    }
})