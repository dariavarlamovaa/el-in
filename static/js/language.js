const langMenu = document.querySelector('.lang-menu')
const langDropdown = document.querySelector('.lang-dropdown')
const selectedLanguage = document.querySelector('.selected_language')

langDropdown.style.display = langDropdown.style.display || "none";
selectedLanguage.style.borderBottomRightRadius = langDropdown.style.borderBottomRightRadius || "5px";
selectedLanguage.style.borderBottomLeftRadius = langDropdown.style.borderBottomLeftRadius || "5px";

langMenu.addEventListener('click', function () {
    langDropdown.style.display = (langDropdown.style.display === "none" || langDropdown.style.display === "") ? "block" : "none";
    selectedLanguage.style.borderBottomRightRadius = (selectedLanguage.style.borderBottomRightRadius === "unset" || selectedLanguage.style.borderBottomRightRadius === "") ? "5px" : "unset";
    selectedLanguage.style.borderBottomLeftRadius = (selectedLanguage.style.borderBottomLeftRadius === "unset" || selectedLanguage.style.borderBottomLeftRadius === "") ? "5px" : "unset";
});