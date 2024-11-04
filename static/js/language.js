const langMenu = document.querySelector('.lang-menu')
const langDropdown = document.querySelector('.lang-dropdown')
const selectedLanguage = document.querySelector('.selected_language')

function updateLangDropdownVisibility() {
    if (window.innerWidth > 950) {
        langDropdown.style.display = "none";
        selectedLanguage.style.borderBottomRightRadius = '5px'
        selectedLanguage.style.borderBottomLeftRadius = '5px'
    } else {
        langDropdown.style.display = "flex";
        selectedLanguage.style.borderBottomRightRadius = 'unset'
        selectedLanguage.style.borderBottomLeftRadius = 'unset'
    }
}

window.addEventListener('resize', updateLangDropdownVisibility);
updateLangDropdownVisibility();

langMenu.addEventListener('click', function () {
    if (window.innerWidth > 950) {
        langDropdown.style.display = (langDropdown.style.display === "none" || langDropdown.style.display === "") ? "block" : "none";
        selectedLanguage.style.borderBottomRightRadius = (selectedLanguage.style.borderBottomRightRadius === "unset" || selectedLanguage.style.borderBottomRightRadius === "") ? "5px" : "unset";
        selectedLanguage.style.borderBottomLeftRadius = (selectedLanguage.style.borderBottomLeftRadius === "unset" || selectedLanguage.style.borderBottomLeftRadius === "") ? "5px" : "unset";
    }
});