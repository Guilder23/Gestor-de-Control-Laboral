// Buscador de a cauerdo a su cargo
document.addEventListener("DOMContentLoaded", function () {
    const botonesFiltro = document.querySelectorAll(".filtro-btn");
    const tarjetas = document.querySelectorAll(".tarjeta-usuario");
    const mensajeVacio = document.querySelector(".mensaje-vacio");

    botonesFiltro.forEach(boton => {
        boton.addEventListener("click", function () {
            const filtro = this.getAttribute("data-cargo");
            let hayCoincidencias = false;

            tarjetas.forEach(tarjeta => {
                const cargo = tarjeta.getAttribute("data-cargo");

                if (filtro === "all" || cargo === filtro) {
                    tarjeta.style.display = "block";
                    hayCoincidencias = true;
                } else {
                    tarjeta.style.display = "none";
                }
            });

            mensajeVacio.style.display = hayCoincidencias ? "none" : "block";
        });
    });
});
