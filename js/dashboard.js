document.addEventListener('DOMContentLoaded', () => {
    const userNameElement = document.getElementById('user-name');
    const logoutButton = document.getElementById('logout-button');
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const refreshButton = document.getElementById('refresh-button');
    const machinesTbody = document.getElementById('machines-tbody');

    if (!machinesTbody) return;

    async function requireSession() {
        try {
            const session = await AssetManager.request('auth/session.php');
            if (session?.data?.user_name) {
                userNameElement.textContent = `Olá, ${session.data.user_name}`;
            }
            return session;
        } catch (error) {
            window.location.href = 'login.html';
            throw error;
        }
    }

    async function loadMachines(search = '') {
        const query = search ? `?search=${encodeURIComponent(search)}` : '';
        machinesTbody.innerHTML = `<tr><td colspan="5" class="empty-state">Carregando ativos...</td></tr>`;

        try {
            const machines = await AssetManager.request(`machines/list.php${query}`);

            if (!Array.isArray(machines) || machines.length === 0) {
                machinesTbody.innerHTML = '<tr><td colspan="5" class="empty-state">Nenhum ativo encontrado.</td></tr>';
                return;
            }

            machinesTbody.innerHTML = '';
            machines.forEach((machine) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${machine.id}</td>
                    <td>${machine.nome_dispositivo || '—'}</td>
                    <td>${machine.setor || '—'}</td>
                    <td>${machine.responsavel || '—'}</td>
                    <td><button type="button" class="secondary" data-id="${machine.id}">Abrir</button></td>
                `;
                machinesTbody.appendChild(row);
            });
        } catch (error) {
            machinesTbody.innerHTML = `<tr><td colspan="5" class="empty-state">${error.message || 'Erro ao carregar a lista.'}</td></tr>`;
            if (error.status === 401) {
                window.location.href = 'login.html';
            }
        }
    }

    async function handleLogout() {
        try {
            await AssetManager.request('auth/logout.php', { method: 'POST' });
        } catch (error) {
            // ignorar
        } finally {
            window.location.href = 'login.html';
        }
    }

    machinesTbody.addEventListener('click', (event) => {
        const target = event.target;
        if (target instanceof HTMLElement && target.matches('button[data-id]')) {
            const id = target.getAttribute('data-id');
            if (id) {
                window.location.href = `machine.html?id=${encodeURIComponent(id)}`;
            }
        }
    });

    searchButton?.addEventListener('click', () => loadMachines(searchInput.value.trim()));

    searchInput?.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            loadMachines(searchInput.value.trim());
        }
    });

    refreshButton?.addEventListener('click', () => {
        searchInput.value = '';
        loadMachines();
        AssetManager.showToast({ title: 'Lista atualizada' });
    });

    logoutButton?.addEventListener('click', handleLogout);

    requireSession().then(() => loadMachines());
});
