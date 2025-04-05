const BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000/api/v1/orders'
    : 'http://backend:8000/api/v1/orders';

let currentPage = 1;
const ordersPerPage = 10;
let allOrders = [];

const ordersTable = document.getElementById('ordersTableBody');
const orderModalEl = document.getElementById('orderModal');
const modal = window.bootstrap?.Modal
    ? new bootstrap.Modal(orderModalEl)
    : new (window.bootstrap = new bootstrap.Modal(orderModalEl))();

const form = document.getElementById('orderForm');
const formFields = {
    id: document.getElementById('orderId'),
    email: document.getElementById('email'),
    status: document.getElementById('status'),
    total: document.getElementById('total'),
    items: document.getElementById('items')
};

const filterEmail = document.getElementById('filterEmail');
const filterStatus = document.getElementById('filterStatus');
const paginationContainer = document.getElementById('pagination');

filterEmail.addEventListener('input', applyFiltersLocal);
filterStatus.addEventListener('change', applyFiltersLocal);

// Carrega todos os pedidos na primeira vez
async function loadOrders() {
    try {
        const response = await fetch(BASE_URL);
        const orders = await response.json();
        allOrders = orders;
        renderPage();
    } catch (error) {
        console.error('Erro ao carregar pedidos:', error);
        alert('Erro ao carregar pedidos');
    }
}

function applyFiltersLocal() {
    currentPage = 1;
    renderPage();
}

// Busca os pedidos atualizados do backend e aplica os filtros
const applyFiltersBtn = document.getElementById('applyFilters');
applyFiltersBtn.addEventListener('click', async () => {
    try {
        const response = await fetch(BASE_URL);
        const orders = await response.json();
        allOrders = orders;
        currentPage = 1;
        renderPage();
    } catch (error) {
        console.error('Erro ao aplicar filtros:', error);
        alert('Erro ao buscar pedidos atualizados');
    }
});

// Retorna os pedidos filtrados com base nos campos
function getFilteredOrders() {
    const email = filterEmail?.value.toLowerCase() || "";
    const status = filterStatus?.value;

    return allOrders.filter(order =>
        order.customer_email.toLowerCase().includes(email) &&
        (!status || status === "TODOS" || order.status === status)
    );
}

function renderPage() {
    const filtered = getFilteredOrders();
    const start = (currentPage - 1) * ordersPerPage;
    const paginated = filtered.slice(start, start + ordersPerPage);

    displayOrders(paginated);
    renderPagination(filtered.length);
}

function renderPagination(totalItems) {
    paginationContainer.innerHTML = '';
    const totalPages = Math.ceil(totalItems / ordersPerPage);

    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement('button');
        btn.className = `btn btn-sm ${i === currentPage ? 'btn-primary' : 'btn-outline-primary'} me-1`;
        btn.textContent = i;
        btn.onclick = () => {
            currentPage = i;
            renderPage();
        };
        paginationContainer.appendChild(btn);
    }
}

// Mostra os pedidos na tabela
function displayOrders(orders) {
    ordersTable.innerHTML = '';

    if (orders.length === 0) {
        ordersTable.innerHTML = '<tr><td colspan="6" class="text-center">Nenhum pedido encontrado.</td></tr>';
        return;
    }

    orders.forEach(order => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${order.id}</td>
            <td>${order.customer_email}</td>
            <td>R$ ${order.total.toFixed(2)}</td>
            <td>${order.status}</td>
            <td>${new Date(order.created_at).toLocaleString()}</td>
            <td>
                <button class="btn btn-sm btn-info me-1" onclick="openEditModal(${order.id})">Editar</button>
                <button class="btn btn-sm btn-danger" onclick="deleteOrder(${order.id})">Excluir</button>
            </td>
        `;
        ordersTable.appendChild(row);
    });
}

// Abre o modal de edição com dados do pedido
async function openEditModal(id) {
    try {
        const response = await fetch(`${BASE_URL}/${id}`);
        const order = await response.json();

        formFields.id.value = order.id;
        formFields.email.value = order.customer_email;
        formFields.status.value = order.status;
        formFields.total.value = order.total.toFixed(2);

        // Mostrar os itens como JSON (editável)
        formFields.items.value = JSON.stringify(order.items, null, 2);

        modal.show();
    } catch (error) {
        console.error('Erro ao buscar pedido:', error);
        alert('Erro ao buscar pedido');
    }
}

// Atualiza um pedido após salvar no modal
form?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const id = formFields.id.value;
    let itemsParsed = [];

    try {
        itemsParsed = JSON.parse(formFields.items.value);
    } catch (err) {
        alert("Erro ao converter os itens. Certifique-se de que o JSON está válido.");
        return;
    }

    const payload = {
        customer_email: formFields.email.value,
        status: formFields.status.value.toUpperCase(),
        total: parseFloat(formFields.total.value),
        items: itemsParsed
    };

    try {
        const response = await fetch(`${BASE_URL}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao atualizar pedido');
        }

        alert('Pedido atualizado com sucesso!');
        modal.hide();
        loadOrders();
    } catch (error) {
        console.error('Erro ao atualizar pedido:', error);
        alert(`Erro: ${error.message}`);
    }
});

// Exclui um pedido
async function deleteOrder(id) {
    if (!confirm(`Deseja realmente excluir o pedido #${id}?`)) return;

    try {
        const response = await fetch(`${BASE_URL}/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Erro ao excluir pedido');

        alert('Pedido excluído com sucesso!');
        loadOrders();
    } catch (error) {
        console.error('Erro ao excluir pedido:', error);
        alert('Erro ao excluir pedido');
    }
}

// Carrega os pedidos assim que a página estiver pronta
document.addEventListener('DOMContentLoaded', loadOrders);