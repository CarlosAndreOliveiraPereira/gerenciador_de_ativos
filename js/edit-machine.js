document.addEventListener('DOMContentLoaded', () => {
    const editMachineForm = document.getElementById('edit-machine-form');
    const API_BASE_URL = '../api/machines/';

    if (editMachineForm) {
        const urlParams = new URLSearchParams(window.location.search);
        const machineId = urlParams.get('id');

        if (!machineId) {
            window.location.href = 'dashboard.html';
            return;
        }

        // Populates the form with the machine's existing data
        const populateEditForm = async () => {
            try {
                const response = await fetch(API_BASE_URL + 'read.php');
                const result = await response.json();

                if (result.success) {
                    const machine = result.machines.find(m => m.id == machineId);
                    if (machine) {
                        document.getElementById('machine-id').value = machine.id;
                        document.getElementById('localidade').value = machine.localidade || '';
                        document.getElementById('nome_dispositivo').value = machine.nome_dispositivo || '';
                        document.getElementById('numero_serie').value = machine.numero_serie || '';
                        document.getElementById('nota_fiscal').value = machine.nota_fiscal || '';
                        document.getElementById('responsavel').value = machine.responsavel || '';
                        document.getElementById('email_responsavel').value = machine.email_responsavel || '';
                        document.getElementById('setor').value = machine.setor || '';
                        document.getElementById('windows_update_ativo').value = machine.windows_update_ativo || '';
                        document.getElementById('sistema_operacional').value = machine.sistema_operacional || '';
                        document.getElementById('observacao').value = machine.observacao || '';
                    } else {
                        showMessage('Máquina não encontrada.', false);
                        setTimeout(() => window.location.href = 'dashboard.html', 1500);
                    }
                } else {
                     window.location.href = 'login.html'; // Auth error
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
                localidade: document.getElementById('localidade').value,
                nome_dispositivo: document.getElementById('nome_dispositivo').value,
                numero_serie: document.getElementById('numero_serie').value,
                nota_fiscal: document.getElementById('nota_fiscal').value,
                responsavel: document.getElementById('responsavel').value,
                email_responsavel: document.getElementById('email_responsavel').value,
                setor: document.getElementById('setor').value,
                windows_update_ativo: document.getElementById('windows_update_ativo').value,
                sistema_operacional: document.getElementById('sistema_operacional').value,
                observacao: document.getElementById('observacao').value
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
                    setTimeout(() => window.location.href = 'dashboard.html', 1500);
                }
            } catch (error) {
                showMessage('Ocorreu um erro de conexão. Tente novamente.', false);
            }
        });
    }
});