// Obtener todos los botones "Ver"
const verBtns = document.querySelectorAll('.verBtn');

// Agregar evento de clic a cada botón "Ver"
verBtns.forEach(btn => {
  btn.addEventListener('click', function() {
    // Obtener datos del cliente desde el botón
    const nombre = this.getAttribute('data-nombre');
    const telefono = this.getAttribute('data-telefono');
    const email = this.getAttribute('data-email');
    
    // Mostrar el pop-up
    document.getElementById("popupOverlay").classList.add("active");

    // Llenar la información del cliente en el pop-up
    document.getElementById("telefono").textContent = telefono;
    document.getElementById("email").textContent = email;
  });
});

// Cerrar el pop-up cuando se presiona "Cerrar"
document.getElementById("closePopupBtn").addEventListener('click', function() {
  document.getElementById("popupOverlay").classList.remove("active");
});
