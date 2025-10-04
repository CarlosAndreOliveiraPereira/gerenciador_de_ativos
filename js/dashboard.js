document.addEventListener('DOMContentLoaded', () => {
    const machinesList = document.getElementById('machines-list');
    const addMachineForm = document.getElementById('add-machine-form');
    const logoutBtn = document.getElementById('logout-btn');

    // Função para carregar e exibir as máquinas
    const loadMachines = async () => {
        const response = await fetch('api/machines/read.php');
        
        if (response.status === 403) { // Se não estiver autorizado, volta pro login
            window.location.href = 'index.html';
            return;
        }
        
        const result = await response.json();

        machinesList.innerHTML = ''; // Limpa a lista antes de adicionar
        if (result.success && result.machines.length > 0) {
            result.machines.forEach(machine => {
                const item = document.createElement('div');
                item.className = 'machine-item';
                item.innerHTML = `
                    <div>
                        <strong>${machine.name}</strong> (${machine.type})<br>
                        <small>Modelo: ${machine.model || 'N/A'} | Série: ${machine.serial_number || 'N/A'}</small>
                    </div>
                    <div class="machine-item-actions">
                        <button class="delete-btn" data-id="${machine.id}">Excluir</button>
                    </div>
                `;
                machinesList.appendChild(item);
            });
        } else {
            machinesList.innerHTML = '<p>Nenhuma máquina cadastrada.</p>';
        }
    };

    // Adicionar nova máquina
    addMachineForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('machine-name').value;
        const type = document.getElementById('machine-type').value;
        const model = document.getElementById('machine-model').value;
        const serial_number = document.getElementById('machine-serial').value;

        await fetch('api/machines/create.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, type, model, serial_number })
        });

        addMachineForm.reset(); // Limpa o formulário
        loadMachines(); // Recarrega a lista
    });
    
    // Deletar máquina (usando delegação de evento)
    machinesList.addEventListener('click', async (e) => {
        if (e.target.classList.contains('delete-btn')) {
            const machineId = e.target.dataset.id;
            if (confirm('Tem certeza que deseja excluir esta máquina?')) {
                await fetch('api/machines/delete.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id: machineId })
                });
                loadMachines(); // Recarrega a lista
            }
        }
    });

    // Logout
    logoutBtn.addEventListener('click', async () => {
        await fetch('api/auth/logout.php');
        window.location.href = 'index.html';
    });

    // Carrega as máquinas ao iniciar a página
    loadMachines();
});