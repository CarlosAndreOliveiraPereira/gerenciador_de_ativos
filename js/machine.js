document.addEventListener('DOMContentLoaded', () => {
    const machineDetails = document.getElementById('machine-details');
    const userNameElement = document.getElementById('user-name');
    const logoutButton = document.getElementById('logout-button');

    const urlParams = new URLSearchParams(window.location.search);
    const machineId = urlParams.get('id');

    async function fetchMachineDetails() {
        if (!machineId) {
            machineDetails.innerHTML = '<p>ID do ativo não fornecido.</p>';
            return;
        }

        try {
            const response = await fetch(`../api/machines/get.php?id=${machineId}`);
            const result = await response.json();

            if (result.success) {
                const machine = result.data;
                machineDetails.innerHTML = `
                    <p><strong>ID:</strong> ${machine.id}</p>
                    <p><strong>Dispositivo:</strong> ${machine.nome_dispositivo}</p>
                    <p><strong>Setor:</strong> ${machine.setor}</p>
                    <p><strong>Responsável:</strong> ${machine.responsavel}</p>
                    <p><strong>E-mail do Responsável:</strong> ${machine.email_responsavel || 'N/A'}</p>
                    <p><strong>Localidade:</strong> ${machine.localidade}</p>
                    <p><strong>Número de Série:</strong> ${machine.numero_serie || 'N/A'}</p>
                    <p><strong>Sistema Operacional:</strong> ${machine.sistema_operacional || 'N/A'}</p>
                    <p><strong>Observação:</strong> ${machine.observacao || 'N/A'}</p>
                `;
            } else {
                machineDetails.innerHTML = `<p>${result.message}</p>`;
            }
        } catch (error) {
            machineDetails.innerHTML = '<p>Erro ao carregar os detalhes do ativo.</p>';
        }
    }

    async function fetchSession() {
        try {
            const response = await fetch('../api/auth/session.php');
            const result = await response.json();
            if (result.success && result.data.user_name) {
                userNameElement.textContent = `Olá, ${result.data.user_name}`;
            } else {
                window.location.href = 'login.html';
            }
        } catch (error) {
            window.location.href = 'login.html';
        }
    }

    async function handleLogout() {
        try {
            await fetch('../api/auth/logout.php', { method: 'POST' });
        } finally {
            window.location.href = 'login.html';
        }
    }

    if (logoutButton) {
        logoutButton.addEventListener('click', handleLogout);
    }

    fetchSession();
    fetchMachineDetails();
});
