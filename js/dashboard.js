document.addEventListener('DOMContentLoaded', () => {
    const machineList = document.getElementById('machine-list')?.querySelector('tbody');
    const logoutButton = document.getElementById('logout-button');
    const messageDiv = document.getElementById('message');
    const API_BASE_URL = '../api/machines/';

    const showMessage = (msg, isSuccess) => {
        if (messageDiv) {
            messageDiv.textContent = msg;
            messageDiv.className = isSuccess ? 'success' : 'error';
            messageDiv.style.display = 'block';
        }
    };

    // Fetches and displays the list of machines
    const loadMachines = async () => {
        if (!machineList) return;

        try {
            const response = await fetch(API_BASE_URL + 'read.php');
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
                        <td>${machine.name}</td>
                        <td>${machine.model}</td>
                        <td>${machine.serial_number}</td>
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
                machineList.innerHTML = '<tr><td colspan="4">Nenhuma máquina cadastrada.</td></tr>';
            }
        } catch (error) {
            showMessage('Erro ao carregar a lista de máquinas.', false);
        }
    };

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
                            loadMachines(); // Reload the list after deletion
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