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

    let currentMachine = null;

    if (!machineId) {
        handleMissingId();
        return;
    }

    editButton?.addEventListener('click', () => {
        const url = `edit-machine.html?id=${encodeURIComponent(machineId)}`;
        window.location.href = url;
    });

    copyButton?.addEventListener('click', async () => {
        if (!currentMachine) {
            return;
        }

        try {
            await navigator.clipboard.writeText(formatSummary(currentMachine));
            AssetManager.showToast({
                title: 'Resumo copiado',
                description: 'As principais informações do ativo foram copiadas.',
            });
        } catch (error) {
            AssetManager.showToast({
                title: 'Não foi possível copiar',
                description: 'Tente novamente em instantes.',
                variant: 'error',
            });
        }
    });

    async function loadMachine() {
        try {
            const response = await AssetManager.request(`machines/get.php?id=${encodeURIComponent(machineId)}`);
            if (!response || !response.data) {
                throw new Error('Ativo não encontrado.');
            }

            currentMachine = response.data;
            updateView(currentMachine);
            copyButton?.removeAttribute('disabled');
        } catch (error) {
            displayError(error);
        }
    }

    function handleMissingId() {
        nameElement.textContent = 'Ativo não encontrado';
        sectorElement.textContent = 'Setor não informado';
        locationElement.textContent = 'ID do ativo não foi informado.';
        ownerElement.textContent = '—';
        ownerEmailElement.textContent = '—';
        serialElement.textContent = '—';
        invoiceElement.textContent = '—';
        windowsUpdateElement.textContent = '—';
        osElement.textContent = '—';
        notesElement.textContent = 'Não foi possível localizar o ativo porque o identificador não foi informado.';
        updatedElement.textContent = '';
        editButton?.setAttribute('disabled', 'true');
        copyButton?.setAttribute('disabled', 'true');
    }

    function updateView(machine) {
        const deviceName = machine.nome_dispositivo || 'Ativo sem nome';
        nameElement.textContent = deviceName;
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
    }

    function formatSummary(machine) {
        return [
            `Ativo: ${machine.nome_dispositivo || 'N/D'}`,
            `Setor: ${machine.setor || 'N/D'}`,
            `Responsável: ${machine.responsavel || 'N/D'} (${machine.email_responsavel || 'sem e-mail'})`,
            `Localidade: ${machine.localidade || 'Não informada'}`,
            `Número de série: ${machine.numero_serie || 'N/D'}`,
            `Sistema operacional: ${machine.sistema_operacional || 'Não informado'}`,
            `Windows Update: ${machine.windows_update_ativo || 'Não informado'}`,
            `Observações: ${machine.observacao || 'Sem observações registradas.'}`,
        ].join('\n');
    }

    function present(value) {
        if (!value) {
            return '—';
        }
        const text = value.toString().trim();
        return text ? text : '—';
    }

    function displayError(error) {
        const message = error?.message || 'Erro ao carregar os dados do ativo.';
        nameElement.textContent = 'Erro ao carregar';
        notesElement.textContent = message;
        copyButton?.setAttribute('disabled', 'true');

        if (error?.status === 401) {
            window.location.href = 'login.html';
        }
    }

    loadMachine();
});
