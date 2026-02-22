// ===== ДАННЫЕ ТОВАРОВ =====
const products = [
    {
 id: 1,
 title: 'Гроб классический',
 price: 25000,
 material: 'pine',
 size: 'standard',
 desc: 'Минималистичный гроб из массива сосны. Внутренняя обивка — натуральный шелк.'
    },
    {
 id: 2,
 title: 'Гроб премиум',
 price: 45000,
 material: 'oak',
 size: 'standard',
 desc: 'Дубовый гроб с бархатной обивкой. Ручная работа.'
    },
    {
 id: 3,
 title: 'Гроб дубовый',
 price: 65000,
        material: 'oak',
 size: 'large',
 desc: 'Увеличенный дубовый гроб. Для тех, кто ценит простор.'
    },
    {
 id: 4,
 title: 'Гроб металлический',
 price: 85000,
 material: 'metal',
 size: 'double',
 desc: 'Цинковый гроб. Герметичный, для долгих путешествий.'
    },
    {
        id: 5,
        title: 'Гроб сосновый',
        price: 18000,
        material: 'pine',
        size: 'standard',
        desc: 'Легкий сосновый гроб. Бюджетный вариант.'
    },
    {
        id: 6,
        title: 'Гроб элитный',
        price: 120000,
        material: 'oak',
        size: 'double',
        desc: 'Элитный дубовый гроб с золотыми ручками. Максимум статуса.'
    }
];

// ===== ЗАГРУЗКА ТОВАРОВ =====
function loadProducts(filteredProducts = products) {
    const grid = document.getElementById('productsGrid');
    if (!grid) return;
    
    grid.innerHTML = '';
    
    filteredProducts.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card fade-in';
        card.setAttribute('data-id', product.id);
        card.innerHTML = `
            <div class="product-image">
                <div class="image-placeholder">
                    <span>ГРОБ</span>
                </div>
            </div>
            <h3 class="product-title">${product.title}</h3>
            <p class="product-price">${product.price.toLocaleString()} ₽</p>
            <button class="btn btn-outline product-btn">Подробнее</button>
        `;
        
        card.addEventListener('click', (e) => {
            if (!e.target.classList.contains('product-btn')) {
                openModal(product);
            }
        });
        
        const btn = card.querySelector('.product-btn');
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            openModal(product);
        });
        
        grid.appendChild(card);
    });
}

// ===== ФИЛЬТРАЦИЯ =====
function filterProducts() {
    const priceFilter = document.getElementById('priceFilter')?.value || 'all';
    const sizeFilter = document.getElementById('sizeFilter')?.value || 'all';
    const materialFilter = document.getElementById('materialFilter')?.value || 'all';
    
    let filtered = products.filter(product => {
        if (priceFilter !== 'all') {
            const [min, max] = priceFilter.split('-').map(Number);
            if (max) {
                if (product.price < min || product.price > max) return false;
            } else {
                if (product.price < min) return false;
            }
        }
        
        if (sizeFilter !== 'all' && product.size !== sizeFilter) return false;
        if (materialFilter !== 'all' && product.material !== materialFilter) return false;
        
        return true;
    });
    
    loadProducts(filtered);
}

// ===== МОДАЛЬНОЕ ОКНО =====
let currentProduct = null;

function openModal(product) {
    currentProduct = product;
    
    const modal = document.getElementById('productModal');
    if (!modal) return;
    
    document.getElementById('modalTitle').textContent = product.title;
    document.getElementById('modalPrice').textContent = product.price.toLocaleString() + ' ₽';
    
    const materialNames = { oak: 'Дуб', pine: 'Сосна', metal: 'Металл' };
    document.getElementById('modalMaterial').textContent = materialNames[product.material] || product.material;
    
    const sizeNames = { standard: '180 см', large: '200 см', double: '220 см' };
    document.getElementById('modalSize').textContent = sizeNames[product.size] || product.size;
    
    document.getElementById('modalDesc').textContent = product.desc;
    
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    const modal = document.getElementById('productModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// ===== ГЛАВНАЯ ФУНКЦИЯ - ОТПРАВКА МЕНЕДЖЕРУ =====
function orderViaTelegram(product) {
    // ТВОЙ USERNAME
    const managerUsername = 'adviservs';  // ← @adviservs
    
    // Формируем сообщение с заказом
    const productName = product.title;
    const price = product.price;
    
    // Текст который отправится тебе
    const message = `🪦 Здравствуйте! Хочу заказать:%0A%0A📦 Товар: ${productName}%0A💰 Цена: ${price} ₽%0A%0A━━━━━━━━━━━━━━%0AНапишите пожалуйста:%0A• Нужный размер%0A• Предпочитаемый материал%0A• Адрес доставки%0A• Ваш телефон%0A━━━━━━━━━━━━━━`;
    
    // Ссылка на Telegram
    const telegramUrl = `https://t.me/${managerUsername}?text=${message}`;
    
    // Открываем чат
    window.open(telegramUrl, '_blank');
    
    alert('✅ Сейчас откроется чат с менеджером!\n\nНапишите туда:\n• Нужный размер\n• Материал\n• Адрес доставки\n• Ваш телефон');
    
    closeModal();
}

// ===== ПЛАВНЫЙ СКРОЛЛ =====
function initSmoothScroll() {
    document.querySelectorAll('[data-scroll]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('data-scroll');
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
            
            const navLinks = document.getElementById('navLinks');
            const burger = document.getElementById('burger');
            if (navLinks?.classList.contains('active')) {
                navLinks.classList.remove('active');
                burger?.classList.remove('active');
            }
        });
    });
}

// ===== БУРГЕР-МЕНЮ =====
function initBurger() {
    const burger = document.getElementById('burger');
    const navLinks = document.getElementById('navLinks');
    
    if (!burger || !navLinks) return;
    
    burger.addEventListener('click', () => {
        burger.classList.toggle('active');
        navLinks.classList.toggle('active');
    });
    
    document.addEventListener('click', (e) => {
        if (!burger.contains(e.target) && !navLinks.contains(e.target)) {
            burger.classList.remove('active');
            navLinks.classList.remove('active');
        }
    });
}

// ===== ИНИЦИАЛИЗАЦИЯ =====
document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
    initSmoothScroll();
    initBurger();
    
    // Фильтры
    document.getElementById('priceFilter')?.addEventListener('change', filterProducts);
    document.getElementById('sizeFilter')?.addEventListener('change', filterProducts);
    document.getElementById('materialFilter')?.addEventListener('change', filterProducts);
    
    document.getElementById('resetFilters')?.addEventListener('click', () => {
        document.getElementById('priceFilter').value = 'all';
        document.getElementById('sizeFilter').value = 'all';
        document.getElementById('materialFilter').value = 'all';
        loadProducts();
    });
    
    // Модальное окно
    const modal = document.getElementById('productModal');
    const closeBtn = document.querySelector('.modal-close');
    
    closeBtn?.addEventListener('click', closeModal);
    
    window.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });
    
    // Кнопка заказа - теперь открывает чат с @adviservs
    const orderBtn = document.querySelector('.modal-order');
    if (orderBtn) {
        orderBtn.addEventListener('click', () => {
            if (currentProduct) {
                orderViaTelegram(currentProduct);
            } else {
                alert('Ошибка: товар не выбран');
            }
        });
    }
});