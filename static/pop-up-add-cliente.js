// Función para abrir el modal
function openModal() {
    document.getElementById('addClientModal').style.display = 'block';
}

// Función para cerrar el modal
function closeModal() {
    document.getElementById('addClientModal').style.display = 'none';
}

// Manejar el envío del formulario
document.getElementById('addClientForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevenir el envío estándar del formulario

    // Capturar los datos del formulario
    const formData = new FormData(event.target); // Crear FormData a partir del formulario
    const data = Object.fromEntries(formData.entries()); // Convertir a objeto JSON

    // Imprimir los datos capturados para depuración
    console.log("Datos enviados:", data);

    try {
        // Enviar los datos al backend usando fetch
        const response = await fetch('/add-client', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Indicar que el contenido es JSON
            },
            body: JSON.stringify(data), // Convertir los datos a JSON
        });

        if (response.ok) {
            // Si el cliente se agregó con éxito
            alert('Cliente agregado exitosamente');
            closeModal(); // Cerrar el modal
            location.reload(); // Recargar la página para mostrar los nuevos datos
        } else {
            // Manejo de errores del servidor
            const error = await response.json();
            alert(`Error: ${error.message}`);
        }
    } catch (error) {
        // Manejo de errores en la conexión
        console.error('Error al enviar los datos:', error);
        alert('Error al procesar la solicitud. Intenta nuevamente.');
    }
});
