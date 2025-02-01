document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.getElementById("menuToggle");
    const sideMenu = document.getElementById("sideMenu");

    // Recuperar estado del menú
    const isMenuOpen = localStorage.getItem("menuOpen") === "true";

    // Aplicar estado inicial
    if (isMenuOpen) {
        sideMenu.classList.add("open");
    }

    // Toggle del menú
    menuToggle.addEventListener("click", () => {
        const menuIsOpen = sideMenu.classList.toggle("open");
        localStorage.setItem("menuOpen", menuIsOpen);
    });
});
