function actualizarReloj() {
    const opcionesFecha = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const fecha = new Date();
    const hora = fecha.toLocaleTimeString();
    const dia = fecha.toLocaleDateString('es-ES', opcionesFecha);

    // Mostrar la fecha y hora en el div con id "reloj"
    document.getElementById('reloj').innerHTML = `${dia} <br> ${hora}`;
}

// Actualizar el reloj cada segundo
setInterval(actualizarReloj, 1000);

// Iniciar el reloj al cargar la página
window.onload = actualizarReloj;

