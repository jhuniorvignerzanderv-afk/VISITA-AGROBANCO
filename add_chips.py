import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add CSS for product chips
css_chips = """
        .product-chip {
            display: inline-block;
            padding: 4px 10px;
            margin: 2px 4px 2px 0;
            background-color: #e3f2fd;
            color: #1976d2;
            border-radius: 12px;
            font-size: 11px;
            cursor: pointer;
            border: 1px solid #90caf9;
            transition: all 0.2s;
            user-select: none;
        }
        .product-chip:hover {
            background-color: #bbdefb;
        }
        body.dark-mode .product-chip {
            background-color: #1e3a5f;
            color: #64b5f6;
            border-color: #1565c0;
        }
"""
if '.product-chip {' not in html:
    html = html.replace('</style>', css_chips + '\n    </style>')

# 2. Add Quick Products Container below the input
form_product_old = """            <div class="form-group">
                <label for="producto">PRODUCTO</label>
                <input type="text" id="producto" placeholder="Ej: Maíz, Arroz">
            </div>"""
form_product_new = """            <div class="form-group">
                <label for="producto">PRODUCTO</label>
                <input type="text" id="producto" placeholder="Ej: Maíz, Arroz" style="margin-bottom: 5px;">
                <div id="quick-products-container" style="display: flex; flex-wrap: wrap;"></div>
            </div>"""
html = html.replace(form_product_old, form_product_new)

# 3. Add JS function to populate the chips based on dynamic extraction
chips_js = """
    window.setProduct = function(prod) {
        document.getElementById('producto').value = prod;
    };

    function renderQuickProducts() {
        const container = document.getElementById('quick-products-container');
        if (!container) return;
        
        // Frecuentes fijos por si la lista está vacía
        const defaultProducts = ['Maíz', 'Arroz', 'Café', 'Cacao', 'Ganado'];
        
        // Extraer productos únicos de la base de datos
        const productCounts = {};
        clients.forEach(c => {
            const p = (c.producto || '').trim();
            if (p && p !== '-' && p !== '') {
                // Capitalizar primera letra para uniformidad
                const cleanP = p.charAt(0).toUpperCase() + p.slice(1).toLowerCase();
                productCounts[cleanP] = (productCounts[cleanP] || 0) + 1;
            }
        });
        
        // Juntar los fijos con los dinámicos
        defaultProducts.forEach(dp => {
            if (!productCounts[dp]) productCounts[dp] = 0; // Añadir con peso 0 si no existe
        });
        
        // Ordenar por frecuencia de uso (los más usados primero)
        const sortedProducts = Object.keys(productCounts).sort((a, b) => productCounts[b] - productCounts[a]);
        
        // Mostrar máximo los 10 más populares
        const topProducts = sortedProducts.slice(0, 10);
        
        container.innerHTML = topProducts.map(p => 
            `<span class="product-chip" onclick="setProduct('${p}')">+ ${p}</span>`
        ).join('');
    }
"""

if 'window.setProduct =' not in html:
    html = html.replace('// --- NUEVAS MEJORAS JS ---', chips_js + '\n    // --- NUEVAS MEJORAS JS ---')

# 4. Call renderQuickProducts() whenever the modal is opened
open_modal_old = """    function openModal(client = null) {
        modal.style.display = 'block';
        if (client) {"""
open_modal_new = """    function openModal(client = null) {
        modal.style.display = 'block';
        renderQuickProducts();
        if (client) {"""
html = html.replace(open_modal_old, open_modal_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
