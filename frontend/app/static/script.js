// Constante para a URL do backend
const BACKEND_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000/api/v1/orders' 
    : 'http://backend:8000/api/v1/orders';


let cart = JSON.parse(localStorage.getItem('cart')) || [];

function getElementSafe(id) {
    const element = document.getElementById(id);
    if (!element) {
        console.error(`Elemento não encontrado: ${id}`);
        return null;
    }
    return element;
}

// 2. Funções para Produtos
async function loadProducts(category = '') {
    const productsContainer = getElementSafe('products');
    if (!productsContainer) return;

    try {
        // Mostra loader enquanto carrega
        productsContainer.innerHTML = `
            <div class="col-12 text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Carregando...</span>
                </div>
                <p class="mt-2">Carregando produtos...</p>
            </div>
        `;

        const url = category 
            ? `https://fakestoreapi.com/products/category/${category}`
            : 'https://fakestoreapi.com/products';
        
        const response = await fetch(url);
        const products = await response.json();
        displayProducts(products);
    } catch (error) {
        console.error('Erro ao carregar produtos:', error);
        productsContainer.innerHTML = `
            <div class="col-12 alert alert-danger">
                Erro ao carregar produtos. Recarregue a página.
            </div>
        `;
    }
}

function displayProducts(products) {
    const container = getElementSafe('products');
    if (!container) return;
    
    container.innerHTML = products.map(product => `
        <div class="col-md-3 mb-4">
            <div class="card h-100">
                <img src="${product.image}" class="card-img-top p-3" style="height: 200px; object-fit: contain;" alt="${product.title}">
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">${product.title}</h5>
                    <p class="card-text">R$ ${product.price.toFixed(2)}</p>
                    <button class="btn btn-dark mt-auto add-to-cart" data-id="${product.id}">
                        Adicionar ao Carrinho
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// 3. Funções do Carrinho
function updateCartUI() {
    const cartItemsContainer = getElementSafe('cartItems');
    const cartBadge = getElementSafe('cartBadge');
    const totalElement = getElementSafe('cartTotal');
    
    if (!cartItemsContainer || !cartBadge || !totalElement) {
        console.error('Elementos do carrinho não encontrados no DOM');
        return;
    }
    
    // Atualizar contador
    const itemCount = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartBadge.textContent = itemCount;
    cartBadge.style.display = itemCount > 0 ? 'block' : 'none';
    
    // Atualizar lista de itens
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p class="text-muted">Seu carrinho está vazio</p>';
        totalElement.textContent = 'R$ 0,00';
        return;
    }
    
    let total = 0;
    cartItemsContainer.innerHTML = cart.map(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        
        return `
            <div class="cart-item mb-3 pb-3 border-bottom">
                <div class="d-flex justify-content-between">
                    <div>
                        <h6 class="mb-1">${item.title}</h6>
                        <small class="text-muted">
                            R$ ${item.price.toFixed(2)} × ${item.quantity}
                        </small>
                    </div>
                    <div class="d-flex align-items-center">
                        <span class="me-3">R$ ${itemTotal.toFixed(2)}</span>
                        <button class="btn btn-sm btn-outline-danger remove-from-cart" data-id="${item.id}">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    // Atualizar total
    totalElement.textContent = `R$ ${total.toFixed(2)}`;
}
    
let isAdding = false;

async function addToCart(productId) {
    if (isAdding) return;
    isAdding = true;

    try {
        const response = await fetch(`https://fakestoreapi.com/products/${productId}`);
        const product = await response.json();

        // Recarrega sempre o carrinho
        cart = JSON.parse(localStorage.getItem('cart')) || [];

        console.log('Carrinho atual:', cart);
        console.log('Tentando adicionar:', product.id);

        const existingItem = cart.find(item => item.id === product.id);

        if (existingItem) {
            existingItem.quantity++;
        } else {
            cart.push({
                id: product.id,
                title: product.title,
                price: product.price,
                image: product.image,
                quantity: 1
            });
        }

        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartUI();
        showAlert(`${product.title} adicionado ao carrinho!`, 'success');
    } catch (error) {
        console.error('Erro ao adicionar ao carrinho:', error);
        showAlert('Erro ao adicionar produto', 'danger');
    } finally {
        isAdding = false;
    }
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartUI();
    showAlert('Produto removido do carrinho', 'warning');
}


// 4. Função de Checkout
async function checkout() {
    if (cart.length === 0) {
        showAlert('Seu carrinho está vazio!', 'warning');
        return;
    }

    try {
        const order = {
            items: cart.map(item => ({
                product_id: item.id,
                title: item.title,
                price: item.price,
                quantity: item.quantity
            })),
            total: cart.reduce((sum, item) => sum + (item.price * item.quantity), 0),
            customer_email: "cliente@exemplo.com",
            status: "PENDENTE"
        };

        const response = await fetch(BACKEND_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(order),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Erro ao finalizar compra');
        }

        const result = await response.json();
        
        // Limpa o carrinho após sucesso
        cart = [];
        localStorage.removeItem('cart');
        updateCartUI();
        
        showAlert('Compra finalizada com sucesso!', 'success');
        return result;
    } catch (error) {
        console.error('Erro no checkout:', error);
        showAlert(`Falha ao finalizar: ${error.message}`, 'danger');
        throw error;
    }
}

// 5. Funções Auxiliares
function showAlert(message, type) {
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1100;
        `;
        document.body.appendChild(toastContainer);
    }

    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-white bg-${type} border-0`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');
    
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    toastContainer.appendChild(toastEl);
    
    const toast = new bootstrap.Toast(toastEl, {
        autohide: true,
        delay: 3000
    });
    toast.show();
    
    toastEl.addEventListener('hidden.bs.toast', () => {
        toastEl.remove();
    });
}

// 6. Inicialização
function init() {
    // Configura event listeners
    document.addEventListener('click', function (e) {
        const target = e.target;
    
        // Botão de adicionar ao carrinho
        if (target.matches('.add-to-cart')) {
            const productId = target.getAttribute('data-id');
            addToCart(parseInt(productId));
            return;
        }
    
        // Botão de remover do carrinho
        const removeBtn = target.closest('.remove-from-cart');
        if (removeBtn) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            const productId = removeBtn.getAttribute('data-id');
            if (productId) {
                removeFromCart(parseInt(productId));
            }
        }
    });    

    // Configura botão de checkout
    const checkoutButton = getElementSafe('checkoutButton');
    if (checkoutButton) {
        checkoutButton.addEventListener('click', checkout);
    }

    // Configura filtro de categoria
    const categoryFilter = getElementSafe('categoryFilter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function() {
            loadProducts(this.value);
        });
    }

    // Configura busca
    const searchInput = getElementSafe('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            document.querySelectorAll('#products .card').forEach(card => {
                const title = card.querySelector('.card-title')?.textContent.toLowerCase();
                if (title) {
                    card.closest('.col-md-3').style.display = 
                        title.includes(searchTerm) ? 'block' : 'none';
                }
            });
        });
    }

    // Carrega dados iniciais
    loadProducts();
    updateCartUI();
}

// Inicia quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', init);