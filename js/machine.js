document.addEventListener('DOMContentLoaded', () => {
    const machineId = AssetManager.getQueryParam('id');
    const nameElement = document.getElementById('machine-name');
    const sectorElement = document.getElementById('machine-sector');
    const locationElement = document.getElementById('machine-location');
    const ownerElement = document.getElementById('machine-owner');
    const ownerEmailElement = document.getElementById('machine-owner-email');
    const serialElement = document.getElementById('machine-serial');
    const invoiceElement = document.getElementById('machine-invoice');
    const windowsUpdateElement = document.getElementById('machine-windows-update');
    const osElement = document.getElementById('machine-os');
    const notesElement = document.getElementById('machine-notes');
    const updatedElement = document.getElementById('machine-updated');
    const editButton = document.getElementById('edit-machine-button');
    const copyButton = document.getElementById('copy-summary');

    if (!machineId) {
        nameElement.textContent = 'Ativo não encontrado';
        notesElement.textContent = 'O identificador do ativo não foi informado.';
        editButton?.setAttribute('disabled', 'true');
        copyButton?.setAttribute('disabled', 'true');
        return;
    }

    editButton?.addEventListener('click', () => {
        window.location.href = `edit-machine.html?id=${encodeURIComponent(machineId)}`;
    });

    function present(value) {
        return value && value.trim() ? value : '—';
    }

    function formatSummary(machine) {
        return [
            `Ativo: ${machine.nome_dispositivo || 'N/D'}`,
            `Setor: ${machine.setor || 'N/D'}`,
            `Responsável: ${machine.responsavel || 'N/D'} (${machine.email_responsavel || 'sem e-mail'})`,
            `Localidade: ${machine.localidade || 'Não informada'}`,
            `Série: ${machine.numero_serie || 'N/D'}`,
            `Sistema operacional: ${machine.sistema_operacional || 'Não informado'}`,
            `Windows Update: ${machine.windows_update_ativo || 'Não informado'}`,
            `Observações: ${machine.observacao || 'Sem observações registradas.'}`,
        ].join('\n');
    }

    async function loadMachine() {
        try {
            const response = await AssetManager.request(`machines/get.php?id=${encodeURIComponent(machineId)}`);
            if (!response?.data) {
                throw new Error('Ativo não encontrado.');
            }

            const machine = response.data;
            nameElement.textContent = machine.nome_dispositivo || 'Ativo sem nome';
            sectorElement.textContent = machine.setor ? `Setor: ${machine.setor}` : 'Setor não informado';
            locationElement.textContent = machine.localidade ? `Local: ${machine.localidade}` : 'Localidade não informada';
            ownerElement.textContent = present(machine.responsavel);
            ownerEmailElement.textContent = present(machine.email_responsavel);
            serialElement.textContent = present(machine.numero_serie);
            invoiceElement.textContent = present(machine.nota_fiscal);
            windowsUpdateElement.textContent = present(machine.windows_update_ativo);
            osElement.textContent = present(machine.sistema_operacional);
            notesElement.textContent = machine.observacao?.trim() || 'Sem observações registradas.';

            const now = new Intl.DateTimeFormat('pt-BR', {
                dateStyle: 'long',
                timeStyle: 'short',
            }).format(new Date());
            updatedElement.textContent = `Visualizado em ${now}`;

            copyButton?.addEventListener('click', async () => {
                try {
                    await navigator.clipboard.writeText(formatSummary(machine));
                    AssetManager.showToast({ title: 'Resumo copiado', description: 'As informações foram copiadas para a área de transferência.' });
                } catch (error) {
                    AssetManager.showToast({ title: 'Não foi possível copiar', variant: 'error' });
                }
            });
        } catch (error) {
            nameElement.textContent = 'Erro ao carregar';
            notesElement.textContent = error.message || 'Não foi possível recuperar os dados deste ativo.';
            if (error.status === 401) {
                window.location.href = 'login.html';
            }
        }
    }

    loadMachine();
});
