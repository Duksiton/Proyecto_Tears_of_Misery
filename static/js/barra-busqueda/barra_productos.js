document.addEventListener('DOMContentLoaded', function () {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const productosTable = document.getElementById('productosTable').getElementsByTagName('tbody')[0];

    
    searchForm.addEventListener('submit', function (event) {
        event.preventDefault();
        filterProducts(searchInput.value);
    });

    function filterProducts(query) {
        const filteredProducts = productos.filter(product =>
            product.nombre.toLowerCase().includes(query.toLowerCase()) ||
            product.descripcion.toLowerCase().includes(query.toLowerCase()) ||
            (product.talla && product.talla.toLowerCase().includes(query.toLowerCase())) ||
            product.precio.toString().includes(query) ||
            product.stock.toString().includes(query) ||
            (product.categoriaNombre && product.categoriaNombre.toLowerCase().includes(query.toLowerCase()))
        );
        renderProducts(filteredProducts.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage));
        renderPagination(filteredProducts.length, itemsPerPage, currentPage);
    }

    function renderCurrentPage() {
        const start = (currentPage - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        const paginatedProducts = productos.slice(start, end);
        renderProducts(paginatedProducts);
        renderPagination(productos.length, itemsPerPage, currentPage);
    }

    // Función para obtener productos desde la API y llenar la tabla
    function fetchProductos() {
        fetch('/api/productos')
            .then(response => response.json())
            .then(data => {
                productos = data;
                renderCurrentPage(); // Renderizar la primera página de productos
            })
            .catch(error => console.error('Error fetching products:', error));
    }

    // Llamada inicial para obtener productos
    fetchProductos();

    // Función de búsqueda
    searchInput.addEventListener('keyup', function () {
        const searchTerm = searchInput.value.toLowerCase();
        const tableRows = productosTable.getElementsByTagName('tr');

        for (let i = 0; i < tableRows.length; i++) {
            const row = tableRows[i];
            const cells = row.getElementsByTagName('td');
            let rowContainsSearchTerm = false;

            for (let j = 0; j < cells.length; j++) {
                const cellText = cells[j].textContent.toLowerCase();
                if (cellText.includes(searchTerm)) {
                    rowContainsSearchTerm = true;
                    break;
                }
            }

            if (rowContainsSearchTerm) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
    });
});
