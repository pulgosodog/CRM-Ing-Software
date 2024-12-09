function actualizarReloj() {
    const reloj = document.getElementById('reloj');
    const ahora = new Date();
    const horas = ahora.getHours().toString().padStart(2, '0');
    const minutos = ahora.getMinutes().toString().padStart(2, '0');
    const segundos = ahora.getSeconds().toString().padStart(2, '0');
    reloj.textContent = `${horas}:${minutos}:${segundos}`;
}

// Actualizar el reloj cada segundo
setInterval(actualizarReloj, 1000);

// Inicializar el reloj inmediatamente
actualizarReloj();
