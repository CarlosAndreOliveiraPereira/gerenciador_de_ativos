document.addEventListener('DOMContentLoaded', () => {
    const messageDiv = document.getElementById('message');
    const machineList = document.getElementById('machine-list')?.querySelector('tbody');
    const addMachineForm = document.getElementById('add-machine-form');
    const editMachineForm = document.getElementById('edit-machine-form');
    const logoutButton = document.getElementById('logout-button');

    const API_BASE_URL = '../api/machines/';

    // Função para exibir mensagens
    const showMessage = (msg, isSuccess) => {
        if (messageDiv) {
            messageDiv.textContent = msg;
            messageDiv.className = isSuccess ? 'success' : 'error';
        }
    };

    // --- Lógica do Dashboard: Listar Máquinas ---
    const loadMachines = async () => {
        if (!machineList) return;

        const response = await fetch(API_BASE_URL + 'read.php');
        if (response.status === 403) { // Não autorizado
            window.location.href = 'login.html';
            return;
        }
        const result = await response.json();

        machineList.innerHTML = ''; // Limpa a lista
        if (result.success && result.machines.length > 0) {
            result.machines.forEach(machine => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${machine.name}</td>
                    <td>${machine.model}</td>
                    <td>${machine.serial_number}</td>
                    <td class="actions">
                        <a href="edit-machine.html?id=${machine.id}" class="btn-edit">Editar</a>
                        <button class="btn-delete" data-id="${machine.id}">Excluir</button>
                    </td>
                `;
                machineList.appendChild(row);
            });
        } else if (!result.success) {
            showMessage(result.message, false);
        } else {
             machineList.innerHTML = '<tr><td colspan="4">Nenhuma máquina cadastrada.</td></tr>';
        }
    };

    // --- Lógica para Adicionar Máquina ---
    if (addMachineForm) {
        addMachineForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                name: document.getElementById('machine-name').value,
                model: document.getElementById('machine-model').value,
                serial_number: document.getElementById('serial-number').value,
                description: document.getElementById('machine-description').value,
            };

            const response = await fetch(API_BASE_URL + 'create.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            showMessage(result.message, result.success);

            if (result.success) {
                setTimeout(() => window.location.href = 'dashboard.html', 1500);
            }
        });
    }

    // --- Lógica para Editar Máquina ---
    if (editMachineForm) {
        const urlParams = new URLSearchParams(window.location.search);
        const machineId = urlParams.get('id');

        if (!machineId) {
            window.location.href = 'dashboard.html';
            return;
        }

        // Preenche o formulário com os dados da máquina
        const populateEditForm = (machines) => {
            const machine = machines.find(m => m.id == machineId);
            if (machine) {
                document.getElementById('machine-id').value = machine.id;
                document.getElementById('machine-name').value = machine.name;
                document.getElementById('machine-model').value = machine.model;
                document.getElementById('serial-number').value = machine.serial_number;
                document.getElementById('machine-description').value = machine.description;
            } else {
                 window.location.href = 'dashboard.html'; // Máquina não encontrada
            }
        };

        // Busca os dados para popular o formulário
        fetch(API_BASE_URL + 'read.php').then(res => res.json()).then(result => {
             if (result.success) populateEditForm(result.machines);
        });


        editMachineForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                id: document.getElementById('machine-id').value,
                name: document.getElementById('machine-name').value,
                model: document.getElementById('machine-model').value,
                serial_number: document.getElementById('serial-number').value,
                description: document.getElementById('machine-description').value,
            };

            const response = await fetch(API_BASE_URL + 'update.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            showMessage(result.message, result.success);

            if (result.success) {
                setTimeout(() => window.location.href = 'dashboard.html', 1500);
            }
        });
    }

    // --- Lógica para Excluir Máquina ---
    if (machineList) {
        machineList.addEventListener('click', async (e) => {
            if (e.target.classList.contains('btn-delete')) {
                const machineId = e.target.getAttribute('data-id');
                if (confirm('Tem certeza que deseja excluir esta máquina?')) {
                    const response = await fetch(API_BASE_URL + 'delete.php', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ id: machineId })
                    });
                    const result = await response.json();
                    showMessage(result.message, result.success);
                    if (result.success) {
                        loadMachines(); // Recarrega a lista
                    }
                }
            }
        });
    }

    // --- Lógica de Logout ---
    if (logoutButton) {
        logoutButton.addEventListener('click', async () => {
            const response = await fetch('../api/auth/logout.php');
            const result = await response.json();
            if (result.success) {
                window.location.href = '../index.html';
            }
        });
    }

    // Carrega as máquinas ao entrar no dashboard
    if (window.location.pathname.endsWith('dashboard.html')) {
        loadMachines();
    }
});