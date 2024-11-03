const searchImg = document.getElementById('search-img')
const searchInput = document.getElementById('search-input')

searchInput.style.display = searchInput.style.display || "none";

searchImg.addEventListener('click', function () {
    searchInput.style.display = (searchInput.style.display === "none" || searchInput.style.display === "") ? "block" : "none";
});