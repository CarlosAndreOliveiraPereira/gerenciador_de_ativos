document.addEventListener('DOMContentLoaded', () => {
    const userNameElement = document.getElementById('user-name');
    const logoutButton = document.getElementById('logout-button');
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const machinesTbody = document.getElementById('machines-tbody');

    // Função para buscar os dados da sessão e atualizar a UI
    async function fetchSession() {
        try {
            const response = await fetch('../api/auth/session.php');
            const result = await response.json();

            if (result.success && result.data.user_name) {
                userNameElement.textContent = `Olá, ${result.data.user_name}`;
                fetchMachines(); // Carrega as máquinas após confirmar a sessão
            } else {
                window.location.href = 'login.html';
            }
        } catch (error) {
            window.location.href = 'login.html';
        }
    }

    // Função para buscar e renderizar as máquinas
    async function fetchMachines(searchTerm = '') {
        try {
            const response = await fetch(`../api/machines/list.php?search=${encodeURIComponent(searchTerm)}`);
            const machines = await response.json();

            machinesTbody.innerHTML = ''; // Limpa a tabela

            if (machines.length > 0) {
                machines.forEach(machine => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${machine.id}</td>
                        <td>${machine.nome_dispositivo}</td>
                        <td>${machine.setor}</td>
                        <td>${machine.responsavel}</td>
                        <td><button class="btn-view" data-id="${machine.id}">Ver</button></td>
                    `;
                    machinesTbody.appendChild(row);
                });
            } else {
                machinesTbody.innerHTML = '<tr><td colspan="5">Nenhum ativo encontrado.</td></tr>';
            }
        } catch (error) {
            machinesTbody.innerHTML = '<tr><td colspan="5">Erro ao carregar os ativos.</td></tr>';
        }
    }

    // Função para realizar o logout
    async function handleLogout() {
        try {
            await fetch('../api/auth/logout.php', { method: 'POST' });
        } finally {
            window.location.href = 'login.html';
        }
    }

    // Event Listeners
    if (logoutButton) {
        logoutButton.addEventListener('click', handleLogout);
    }

    if (searchButton) {
        searchButton.addEventListener('click', () => fetchMachines(searchInput.value));
    }

    if (searchInput) {
        searchInput.addEventListener('keyup', (e) => {
            if (e.key === 'Enter') {
                fetchMachines(searchInput.value);
            }
        });
    }

    machinesTbody.addEventListener('click', (e) => {
        if (e.target.classList.contains('btn-view')) {
            const machineId = e.target.dataset.id;
            window.location.href = `machine.html?id=${machineId}`;
        }
    });

    // Busca os dados da sessão ao carregar a página
    fetchSession();
});