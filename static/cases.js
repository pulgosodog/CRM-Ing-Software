let caseTickets;
let nombresAsistente = [];
document.addEventListener('DOMContentLoaded', () => {
    const caseRows = document.querySelectorAll('.clickable-case');
    const caseDetails = document.querySelector('.case-details');

    caseRows.forEach(row => {
        row.addEventListener('click', () => {
            // Obtener datos de la fila clickeada
            const id = row.dataset.id;
            const nombre = row.dataset.nombre;
            const estado = row.dataset.estado;
            const prioridad = row.dataset.prioridad;
            const abogado = row.dataset.abogado || 'Desconocido';
            const cliente = row.dataset.cliente || 'Desconocido';
            const tipo = row.dataset.tipo || 'Desconocido';
            const creacion = row.dataset.creacion;
            let clase = '';
            let prioridadTexto = '';
            switch (prioridad) {
                case "1":
                    clase = "rojo"
                    prioridadTexto = "Alta";
                    break;
                case "2":
                    clase = "amarillo"
                    prioridadTexto = "Media";
                    break;
                case "3":
                    clase = "verde"
                    prioridadTexto = "Baja";
                    break;
                default:
                    break;
            }
            caseDetails.innerHTML = `
                    <table>
                        <thead>
                            <tr>
                            <h3>Detalles de caso</h3>
                            </tr>
                        </thead>                       
                    </table>
                    <div>
                        <strong>ID de caso</strong><br>
                        ${id}
                    </div>
                    <div>
                        <strong>Nombre de caso</strong><br>
                        ${nombre}
                    </div>
                    <div>
                        <strong>Estado</strong><br>
                        ${estado}
                    </div>
                    <div>
                        <strong>Abogado(s) encargado(s)</strong><br>
                        ${abogado}
                    </div>
                    <div>
                        <strong>Cliente</strong><br>
                        ${cliente}
                    </div>
                    <div>
                        <strong>Tipo de caso</strong><br>
                        ${tipo}
                    </div>
                    <div>
                        <strong>Prioridad</strong><br>
                        <div id="estado-fix"><span class="estado ${clase}">${prioridadTexto}</span></div>
                    </div>
                    <div>
                        <strong>Creación</strong><br>
                        ${creacion.split(' ')[0]}
                    </div>
                `;
            fetch(`/cases/${id}`)  // Realiza una solicitud GET a Flask
                .then(response => response.json())  // Convierte la respuesta a JSON
                .then(data => {
                    caseTickets = data;
                    console.log(data);  // Verifica los datos recibidos en la consola
                    caseTickets.forEach(element => {
                        fetch(`/asistente/${element[1]}`)
                            .then(response => response.json())
                            .then(data => {
                                nombresAsistente.push(data[0][1]);
                            })
                            .catch(error => console.error('Error:', error));
                    });
                    // Itera sobre los datos y genera filas dinámicamente
                    function fillWithTickets(data) {
                        document.querySelector('.notes-section').innerHTML = `
                        <h3>Tickets asociados al caso</h3>
                        <table>
                            <thead>
                                <tr>
                                    <th>ID de Ticket</th>
                                    <th>Nombre</th>
                                    <th>Fecha de Creación</th>
                                    <th>Fecha de Tope</th>
                                </tr>
                            </thead>
                            <tbody id="notas">
                            </tbody>
                        </table>`;
                        const tbody = document.getElementById('notas');
                        tbody.innerHTML = '';
                        data.forEach(row => {
                            // Crea un elemento <tr>
                            const tr = document.createElement('tr');
                            tr.classList.add("clickable-ticket");

                            // Crea y llena cada <td> con los datos correspondientes
                            const td1 = document.createElement('td');
                            td1.textContent = row[0];  // Columna 0 de SQL

                            const td2 = document.createElement('td');
                            td2.textContent = row[4];  // Columna 4 de SQL

                            const td3 = document.createElement('td');
                            td3.textContent = row[8].split(' ')[0];  // Columna 8 de SQL

                            const td4 = document.createElement('td');
                            td4.textContent = row[7].split(' ')[0];  // Columna 7 de SQL

                            // Agrega los <td> a la fila <tr>
                            tr.appendChild(td1);
                            tr.appendChild(td2);
                            tr.appendChild(td3);
                            tr.appendChild(td4);

                            // Agrega la fila <tr> al <tbody>
                            tbody.appendChild(tr);
                        });
                        const ticketRows = document.querySelectorAll('.clickable-ticket');
                        ticketRows.forEach(row => {
                            console.log(row);
                            row.addEventListener('click', () => {
                                let id = row.querySelector('td').innerHTML
                                for (let i = 0; i < caseTickets.length; i++) {
                                    if (id == caseTickets[i][0]) {
                                        document.querySelector('.notes-section').innerHTML =
                                            `<button id="backButton">Volver</button>
                                            <table id="ticket-details">
                                            <thead>
                                                <tr>
                                                    <th colspan="4">Detalles de Ticket</th>
                                                </tr>
                                            </thead>
                                            <tr>
                                            <th>ID de Ticket</th>
                                                <th>Asistente encargado</th>
                                            </tr>
                                            <tr>
                                                <td>${caseTickets[i][0]}</td>
                                                <td>${nombresAsistente[i]}</td>
                                            </tr>
                                            <tr>
                                                <th>Fecha de Creacion</th>
                                                <th>Fecha Tope</th>
                                            </tr>
                                            <tr>
                                                <td>${caseTickets[i][8].split(' ')[0]}</td>
                                                <td>${caseTickets[i][7].split(' ')[0]}</td>
                                            </tr>
                                            <tr>
                                                <th colspan="2">Tarea</th>
                                            </tr>
                                            <tr>
                                                <td colspan="2">${caseTickets[i][4]}</tr>
                                            <tr>
                                                <th colspan="2">Descripcion</th>
                                            </tr>
                                            <tr>
                                                <td colspan="2">
                                                   ${caseTickets[i][5]}
                                                </td>
                                            </tr>
                                            <tr>
                                                <th>Estado</th>
                                                <th>Fecha de cierre</th>
    
                                            </tr>
                                            <tr>
                                                <td>${caseTickets[i][3] === 1 ? "Activo" : "Cerrado"}</td>
                                                <td>${caseTickets[i][9] == null ? "Abierto" : caseTickets[i][9].split(' ')[0]}</td>
                                            </tr>
                                            <tr>
                                                <th colspan="2">Nota de asistente</th>
                                            </tr>
                                            <tr>
                                                <td colspan="2">
                                                ${caseTickets[i][6] == null ? "Sin notas" : caseTickets[i][6]}
                                                </td>
                                            </tr>
                                        </table>`;
                                        document.getElementById('backButton').addEventListener('click', () => {
                                            fillWithTickets(data);
                                        });
                                        break;
                                    }
                                }
                            });
                        })
                    }
                    fillWithTickets(data);
                })
                .catch(error => console.error('Error:', error));
        });
    });
});
