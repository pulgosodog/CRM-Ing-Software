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

                // Actualizar el contenido de case-details
                caseDetails.innerHTML = `
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
                        <div id="estado-fix"><span class="estado ${prioridad.toLowerCase()}">${prioridad}</span></div>
                    </div>
                    <div>
                        <strong>Creación</strong><br>
                        ${creacion}
                    </div>
                `;
            });
        });
    });