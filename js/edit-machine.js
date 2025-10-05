document.addEventListener('DOMContentLoaded', () => {
    const editMachineForm = document.getElementById('edit-machine-form');
    const messageDiv = document.getElementById('message');
    const API_BASE_URL = '../api/machines/';

    const showMessage = (msg, isSuccess) => {
        if (messageDiv) {
            messageDiv.textContent = msg;
            messageDiv.className = isSuccess ? 'success' : 'error';
            messageDiv.style.display = 'block';
        }
    };

    if (editMachineForm) {
        const urlParams = new URLSearchParams(window.location.search);
        const machineId = urlParams.get('id');

        if (!machineId) {
            window.location.href = 'dashboard.html';
            return;
        }

        // Populates the form with the machine's data
        const populateEditForm = async () => {
            try {
                const response = await fetch(API_BASE_URL + 'read.php');
                const result = await response.json();

                if (result.success) {
                    const machine = result.machines.find(m => m.id == machineId);
                    if (machine) {
                        document.getElementById('machine-id').value = machine.id;
                        document.getElementById('machine-name').value = machine.name;
                        document.getElementById('machine-model').value = machine.model;
                        document.getElementById('serial-number').value = machine.serial_number;
                        document.getElementById('machine-description').value = machine.description;
                    } else {
                        showMessage('Máquina não encontrada.', false);
                        setTimeout(() => window.location.href = 'dashboard.html', 2000);
                    }
                } else {
                     window.location.href = 'login.html'; // Auth error or other issue
                }
            } catch (error) {
                 showMessage('Erro ao carregar dados da máquina.', false);
            }
        };

        populateEditForm();

        // Handles the form submission
        editMachineForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                id: document.getElementById('machine-id').value,
                name: document.getElementById('machine-name').value,
                model: document.getElementById('machine-model').value,
                serial_number: document.getElementById('serial-number').value,
                description: document.getElementById('machine-description').value,
            };

            try {
                const response = await fetch(API_BASE_URL + 'update.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                showMessage(result.message, result.success);

                if (result.success) {
                    setTimeout(() => window.location.href = 'dashboard.html', 2000);
                }
            } catch (error) {
                showMessage('Ocorreu um erro de conexão. Tente novamente.', false);
            }
        });
    }
});