document.addEventListener('DOMContentLoaded', () => {
    const addMachineForm = document.getElementById('add-machine-form');
    const API_BASE_URL = '../api/machines/';

    if (addMachineForm) {
        addMachineForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Coleta os dados de todos os novos campos do formulário
            const data = {
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
            } catch (error) {
                showMessage('Ocorreu um erro de conexão. Tente novamente.', false);
            }
        });
    }
});