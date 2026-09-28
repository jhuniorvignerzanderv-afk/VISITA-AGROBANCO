document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const excelUpload = document.getElementById('excel-upload');
    const clearDataBtn = document.getElementById('clear-data');
    const clientsListContainer = document.getElementById('clients-list');
    const searchInput = document.getElementById('search-input');
    const statusFilter = document.getElementById('status-filter');
    
    // Modal Elements
    const modal = document.getElementById('visit-modal');
    const closeBtn = document.querySelector('.close');
    const visitForm = document.getElementById('visit-form');
    const modalClientId = document.getElementById('modal-client-id');
    const modalClientName = document.getElementById('modal-client-name');
    const visitDate = document.getElementById('visit-date');
    const visitTime = document.getElementById('visit-time');
    const visitNotes = document.getElementById('visit-notes');
    const visitCompleted = document.getElementById('visit-completed');

    // App State
    let clients = [];
    try {
        const stored = localStorage.getItem('agrobanco_clients');
        if (stored) {
            clients = JSON.parse(stored);
        }
    } catch (e) {
        console.error("Error loading from localStorage:", e);
        clients = [];
    }

    // Initialize App
    renderClients();

    // Event Listeners
    excelUpload.addEventListener('change', handleExcelUpload);
    clearDataBtn.addEventListener('click', clearData);
    searchInput.addEventListener('input', renderClients);
    statusFilter.addEventListener('change', renderClients);
    
    // Modal Events
    closeBtn.addEventListener('click', closeModal);
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
    visitForm.addEventListener('submit', handleFormSubmit);

    // Funciones principales
    function handleExcelUpload(e) {
        const file = e.target.files[0];
        if (!file) return;
        
        console.log("Archivo seleccionado:", file.name);

        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                const data = new Uint8Array(e.target.result);
                const workbook = XLSX.read(data, { type: 'array' });
                const firstSheetName = workbook.SheetNames[0];
                const worksheet = workbook.Sheets[firstSheetName];
                
                // Extraer datos omitiendo las primeras 3 filas (header está en la fila 4 - index 3)
                // Utilizamos raw: false para intentar obtener strings de fechas/números
                const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1, defval: "" });
                
                // Encontrar la fila de encabezados (la que contiene 'CLIENTE' o 'DNI')
                let headerRowIndex = -1;
                for (let i = 0; i < jsonData.length; i++) {
                    const row = jsonData[i];
                    if (row && row.some(cell => typeof cell === 'string' && (cell.toUpperCase().includes('CLIENTE') || cell.toUpperCase().includes('DNI')))) {
                        headerRowIndex = i;
                        break;
                    }
                }

                if (headerRowIndex === -1) {
                    throw new Error("No se pudo encontrar la fila de encabezados (CLIENTE, DNI, etc.) en el Excel.");
                }

                const headers = jsonData[headerRowIndex];
                const rawClients = jsonData.slice(headerRowIndex + 1); // Datos debajo de los encabezados
                
                const newClients = rawClients.map((row, index) => {
                    // Si el nombre del cliente está vacío o no es válido, saltarlo
                    const nombre = row[0] ? String(row[0]).trim() : '';
                    if (!nombre || nombre.toLowerCase() === 'nan') return null;
                    
                    return {
                        id: `client_${Date.now()}_${index}`,
                        nombre: nombre || 'Sin Nombre',
                        dni: (row[1] || 'S/N').toString().trim(),
                        telefono: (row[2] || 'S/N').toString().trim(),
                        producto: (row[3] || 'S/N').toString().trim(),
                        monto: (row[4] || '0').toString().trim(),
                        compromiso: (row[5] || '').toString().trim(),
                        // Campos de programación
                        fechaVisita: '',
                        horaVisita: '',
                        notas: '',
                        completada: false
                    };
                }).filter(client => client !== null);

                if (newClients.length > 0) {
                    // Unir clientes nuevos con existentes, evitando duplicados por DNI y Nombre
                    const existingSignatures = clients.map(c => c.dni + c.nombre);
                    
                    const clientsToAdd = newClients.filter(c => !existingSignatures.includes(c.dni + c.nombre));
                    
                    if (clientsToAdd.length === 0) {
                        alert("Los clientes en este archivo ya estaban cargados.");
                    } else {
                        clients = [...clients, ...clientsToAdd];
                        saveData();
                        renderClients();
                        alert(`${clientsToAdd.length} clientes nuevos cargados con éxito.`);
                    }
                } else {
                    alert("No se encontraron clientes válidos en el archivo Excel. Revisa el formato.");
                }
            } catch (error) {
                console.error(error);
                const errorBanner = document.getElementById('error-banner');
                if (errorBanner) {
                    errorBanner.textContent = "Error al leer el archivo Excel: " + (error.message || error);
                    errorBanner.style.display = 'block';
                }
                alert("Error al leer el archivo Excel: " + (error.message || error));
            }
            
            // Reset input
            excelUpload.value = '';
        };
        
        if (typeof XLSX === 'undefined') {
            const errorBanner = document.getElementById('error-banner');
            if (errorBanner) {
                errorBanner.textContent = "Error Crítico: No se pudo cargar la librería Excel. Verifica tu conexión a Internet o usa un navegador que permita scripts.";
                errorBanner.style.display = 'block';
            }
            alert("No se pudo cargar la herramienta para leer Excel. Asegúrate de estar conectado a Internet.");
            excelUpload.value = '';
            return;
        }
        
        reader.readAsArrayBuffer(file);
    }

    function renderClients() {
        const searchTerm = searchInput.value.toLowerCase();
        const status = statusFilter.value;

        const filteredClients = clients.filter(client => {
            const matchesSearch = client.nombre.toLowerCase().includes(searchTerm) || 
                                  client.dni.toString().toLowerCase().includes(searchTerm);
            
            const matchesStatus = status === 'all' || 
                                  (status === 'pending' && !client.completada) || 
                                  (status === 'completed' && client.completada);
            
            return matchesSearch && matchesStatus;
        });

        if (clients.length === 0) {
            clientsListContainer.innerHTML = '<p class="empty-state">No hay clientes cargados. Por favor, carga el archivo Excel.</p>';
            return;
        }

        if (filteredClients.length === 0) {
            clientsListContainer.innerHTML = '<p class="empty-state">No se encontraron clientes con los filtros actuales.</p>';
            return;
        }

        clientsListContainer.innerHTML = '';
        
        filteredClients.forEach(client => {
            const statusClass = client.completada ? 'completed' : 'pending';
            const statusText = client.completada ? 'Completada' : 'Pendiente';
            const hasDateTime = client.fechaVisita ? `${client.fechaVisita} ${client.horaVisita}` : 'Sin programar';

            const card = document.createElement('div');
            card.className = 'client-card';
            card.innerHTML = `
                <span class="status ${statusClass}">${statusText}</span>
                <h3>${client.nombre}</h3>
                <p><strong>DNI:</strong> ${client.dni}</p>
                <p><strong>Teléfono:</strong> ${client.telefono}</p>
                <p><strong>Producto:</strong> ${client.producto}</p>
                <p><strong>Monto:</strong> ${client.monto}</p>
                <p><strong>Compromiso:</strong> ${client.compromiso}</p>
                <hr style="margin: 10px 0; border: 0; border-top: 1px solid #ddd;">
                <p><strong>Visita:</strong> ${hasDateTime}</p>
                ${client.notas ? `<p><strong>Notas:</strong> ${client.notas.substring(0, 50)}${client.notas.length > 50 ? '...' : ''}</p>` : ''}
                
                <div class="card-actions">
                    <button class="edit-btn" data-id="${client.id}">Programar / Editar Visita</button>
                </div>
            `;
            
            clientsListContainer.appendChild(card);
        });

        // Add event listeners to edit buttons
        document.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', (e) => openModal(e.target.getAttribute('data-id')));
        });
    }

    function openModal(clientId) {
        const client = clients.find(c => c.id === clientId);
        if (!client) return;

        modalClientId.value = client.id;
        modalClientName.textContent = client.nombre;
        visitDate.value = client.fechaVisita;
        visitTime.value = client.horaVisita;
        visitNotes.value = client.notas;
        visitCompleted.checked = client.completada;

        modal.style.display = 'block';
    }

    function closeModal() {
        modal.style.display = 'none';
        visitForm.reset();
    }

    function handleFormSubmit(e) {
        e.preventDefault();
        
        const clientId = modalClientId.value;
        const index = clients.findIndex(c => c.id === clientId);
        
        if (index !== -1) {
            clients[index].fechaVisita = visitDate.value;
            clients[index].horaVisita = visitTime.value;
            clients[index].notas = visitNotes.value;
            clients[index].completada = visitCompleted.checked;
            
            saveData();
            renderClients();
            closeModal();
        }
    }

    function clearData() {
        if (confirm('¿Estás seguro de que deseas borrar todos los clientes y datos programados? Esta acción no se puede deshacer.')) {
            clients = [];
            saveData();
            renderClients();
        }
    }

    function saveData() {
        localStorage.setItem('agrobanco_clients', JSON.stringify(clients));
    }
});
