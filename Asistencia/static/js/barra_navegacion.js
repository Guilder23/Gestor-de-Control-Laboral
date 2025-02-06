
document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector(".menu-toggle");
    const navLinks = document.querySelector(".nav-links");

    menuToggle.addEventListener("click", function () {
        navLinks.classList.toggle("active");
    });

    // Cerrar menú cuando se hace clic en un enlace
    navLinks.addEventListener("click", function () {
        navLinks.classList.remove("active");
    });
});

