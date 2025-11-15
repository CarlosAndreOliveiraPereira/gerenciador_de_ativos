(() => {
    const metaApi = document.querySelector('meta[name="api-base"]');
    const apiBase = metaApi ? metaApi.content.replace(/\/$/, '') : '../api';
    const toastRoot = document.getElementById('toast-root');

    function ensureToastRoot() {
        if (!toastRoot) {
            const root = document.createElement('div');
            root.className = 'toast-root';
            root.id = 'toast-root';
            root.setAttribute('aria-live', 'polite');
            root.setAttribute('aria-atomic', 'false');
            document.body.appendChild(root);
            return root;
        }
        return toastRoot;
    }

    function showToast({ title, description = '', variant = 'success', timeout = 3200 }) {
        const root = ensureToastRoot();
        const toast = document.createElement('div');
        toast.className = `toast is-${variant}`;

        if (title) {
            const strong = document.createElement('strong');
            strong.textContent = title;
            toast.appendChild(strong);
        }

        if (description) {
            const paragraph = document.createElement('p');
            paragraph.textContent = description;
            toast.appendChild(paragraph);
        }

        root.appendChild(toast);

        window.setTimeout(() => {
            toast.classList.add('is-leaving');
            toast.addEventListener('animationend', () => toast.remove(), { once: true });
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(-6px)';
        }, timeout);
    }

    function setFeedback(element, message, type = 'info') {
        if (!element) return;
        if (!message) {
            element.hidden = true;
            element.textContent = '';
            element.classList.remove('is-error', 'is-success');
            return;
        }

        element.hidden = false;
        element.textContent = message;
        element.classList.toggle('is-error', type === 'error');
        element.classList.toggle('is-success', type === 'success');
        if (type !== 'error') {
            element.classList.remove('is-error');
        }
        if (type !== 'success') {
            element.classList.remove('is-success');
        }
    }

    async function request(endpoint, { method = 'GET', data, headers = {}, skipJson = false } = {}) {
        const url = `${apiBase}/${endpoint.replace(/^\/+/, '')}`;
        const options = {
            method,
            headers: {
                Accept: 'application/json',
                ...headers,
            },
            credentials: 'same-origin',
        };

        if (data !== undefined) {
            options.body = JSON.stringify(data);
            options.headers['Content-Type'] = 'application/json';
        }

        const response = await fetch(url, options);
        const contentType = response.headers.get('Content-Type') || '';
        let payload = null;

        if (!skipJson && contentType.includes('application/json')) {
            try {
                payload = await response.json();
            } catch (error) {
                payload = null;
            }
        } else if (!skipJson) {
            const text = await response.text();
            try {
                payload = text ? JSON.parse(text) : null;
            } catch (error) {
                payload = text || null;
            }
        }

        if (!response.ok) {
            const message = payload && typeof payload === 'object' && 'message' in payload
                ? payload.message
                : 'Não foi possível completar a solicitação.';
            const error = new Error(message);
            error.status = response.status;
            error.payload = payload;
            throw error;
        }

        return payload;
    }

    function parseQuery() {
        const { search } = window.location;
        return new URLSearchParams(search);
    }

    function getQueryParam(key) {
        return parseQuery().get(key);
    }

    window.AssetManager = {
        apiBase,
        request,
        showToast,
        setFeedback,
        parseQuery,
        getQueryParam,
    };
})();
