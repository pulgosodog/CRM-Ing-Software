const ticketsRows = document.querySelectorAll('.ticket-row');
const modal = document.getElementById('modal');
const modalContent = document.getElementById('modalContent');
const closeModalButton = document.getElementById('closeModal');

// Iterar sobre cada fila de ticket
ticketsRows.forEach(row => {
  let ticketId = row.querySelector('[data-label="id"]').innerHTML;
  const openModalButton = row.querySelector('.open-modal-btn'); // Asegúrate de tener un botón en cada fila con clase 'open-modal-btn'

  openModalButton.addEventListener('click', async () => {
    modal.style.display = 'block';
      fetch(`/client/${ticketId}`)
      .then(response => response.json())  // Convierte la respuesta a JSON
      .then(cliente => {
        console.log(cliente)
      if (cliente == null) throw new Error('Error al obtener datos');
      modalContent.innerHTML = `
        <p><strong>ID:</strong> ${cliente[0][0]}</p>
        <p><strong>Nombre completo:</strong> ${cliente[0][1]}</p>
        <p><strong>Teléfono:</strong> ${cliente[0][2]}</p>
        <p><strong>Email:</strong> ${cliente[0][3]}</p>
        <p><strong>Preferencia de contacto:</strong> ${cliente[0][4]}</p>
        <p><strong>Fecha de nacimiento:</strong> ${cliente[0][5]}</p>
      `;
    })
      .catch (error => modalContent.innerHTML = '<p>Error al cargar los datos del cliente.</p>')
  });
});

// Evento para cerrar el modal
closeModalButton.addEventListener('click', () => {
  modal.style.display = 'none';
});

// Cerrar el modal si se hace clic fuera de él
window.addEventListener('click', (event) => {
  if (event.target === modal) {
    modal.style.display = 'none';
  }
});
