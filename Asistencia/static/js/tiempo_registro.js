
function calcularTiempoTranscurrido(horaEntrada) {
    const ahora = new Date();
    const entrada = new Date(horaEntrada);
    const diferencia = ahora - entrada;  // Diferencia en milisegundos
    
    const horas = Math.floor(diferencia / (1000 * 60 * 60));  // Calcular horas
    const minutos = Math.floor((diferencia % (1000 * 60 * 60)) / (1000 * 60));  // Calcular minutos
    const segundos = Math.floor((diferencia % (1000 * 60)) / 1000);  // Calcular segundos
    
    return { horas, minutos, segundos };
}

function mostrarTiempo() {
    const elementos = document.querySelectorAll('.tiempo-transcurrido');

    elementos.forEach(function(elemento) {
        const horaEntrada = elemento.getAttribute('data-hora-entrada');
        
        // Calcular el tiempo transcurrido
        const tiempo = calcularTiempoTranscurrido(horaEntrada);
        
        // Mostrar el tiempo formateado
        elemento.textContent = `${tiempo.horas} horas, ${tiempo.minutos} minutos, ${tiempo.segundos} segundos`;
    });
}

// Actualizar el tiempo cada segundo
setInterval(mostrarTiempo, 1000);
