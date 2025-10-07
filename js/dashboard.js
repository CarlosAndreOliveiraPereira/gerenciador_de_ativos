document.addEventListener('DOMContentLoaded', () => {
    const machineList = document.getElementById('machine-list')?.querySelector('tbody');
    const logoutButton = document.getElementById('logout-button');
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const API_BASE_URL = '../api/machines/';

    // Fetches and displays the list of machines, with an optional search term
    const loadMachines = async (searchTerm = '') => {
        if (!machineList) return;

        let fetchUrl = API_BASE_URL + 'read.php';
        if (searchTerm) {
            fetchUrl += `?search=${encodeURIComponent(searchTerm)}`;
        }

        try {
            const response = await fetch(fetchUrl);
            if (response.status === 403) { // Not authorized
                window.location.href = 'login.html';
                return;
            }
            const result = await response.json();

            machineList.innerHTML = ''; // Clear the list before populating
            if (result.success && result.machines.length > 0) {
                result.machines.forEach(machine => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${machine.localidade || '-'}</td>
                        <td>${machine.nome_dispositivo || '-'}</td>
                        <td>${machine.responsavel || '-'}</td>
                        <td>${machine.setor || '-'}</td>
                        <td>${machine.numero_serie || '-'}</td>
                        <td class="actions">
                            <a href="edit-machine.html?id=${machine.id}" class="btn btn-edit">Editar</a>
                            <button class="btn btn-delete" data-id="${machine.id}">Excluir</button>
                        </td>
                    `;
                    machineList.appendChild(row);
                });
            } else if (!result.success) {
                showMessage(result.message, false);
            } else {
                machineList.innerHTML = `<tr><td colspan="6">Nenhuma máquina encontrada.</td></tr>`;
            }
        } catch (error) {
            showMessage('Erro ao carregar a lista de máquinas.', false);
        }
    };

    // Handles search logic
    if (searchButton && searchInput) {
        const performSearch = () => {
            const searchTerm = searchInput.value.trim();
            loadMachines(searchTerm);
        };

        searchButton.addEventListener('click', performSearch);
        searchInput.addEventListener('keyup', (e) => {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }

    // Handles machine deletion
    if (machineList) {
        machineList.addEventListener('click', async (e) => {
            if (e.target.classList.contains('btn-delete')) {
                const machineId = e.target.getAttribute('data-id');
                if (confirm('Tem certeza que deseja excluir esta máquina?')) {
                    try {
                        const response = await fetch(API_BASE_URL + 'delete.php', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ id: machineId })
                        });
                        const result = await response.json();
                        showMessage(result.message, result.success);
                        if (result.success) {
                            loadMachines(searchInput.value.trim()); // Reload the list respecting the current search
                        }
                    } catch (error) {
                        showMessage('Ocorreu um erro de conexão. Tente novamente.', false);
                    }
                }
            }
        });
    }

    // Handles logout
    if (logoutButton) {
        logoutButton.addEventListener('click', async () => {
            const response = await fetch('../api/auth/logout.php');
            const result = await response.json();
            if (result.success) {
                window.location.href = '../index.html';
            }
        });
    }

    // Initial load of machines when the page is ready
    loadMachines();
});