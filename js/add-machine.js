document.addEventListener('DOMContentLoaded', () => {
    const addMachineForm = document.getElementById('add-machine-form');
    const messageDiv = document.getElementById('message');
    const API_BASE_URL = '../api/machines/';

    const showMessage = (msg, isSuccess) => {
        if (messageDiv) {
            messageDiv.textContent = msg;
            messageDiv.className = isSuccess ? 'success' : 'error';
            messageDiv.style.display = 'block';
        }
    };

    if (addMachineForm) {
        addMachineForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                name: document.getElementById('machine-name').value,
                model: document.getElementById('machine-model').value,
                serial_number: document.getElementById('serial-number').value,
                description: document.getElementById('machine-description').value,
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
                    setTimeout(() => window.location.href = 'dashboard.html', 2000);
                }
            } catch (error) {
                showMessage('Ocorreu um erro de conexão. Tente novamente.', false);
            }
        });
    }
});