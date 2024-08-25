document.addEventListener('DOMContentLoaded', function () {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const productosTable = document.getElementById('productosTable').getElementsByTagName('tbody')[0];
    const paginationElement = document.getElementById('pagination');

    let productos = [];
    let currentPage = 1;
    const itemsPerPage = 5;

    function formatPrice(price) {
        return new Intl.NumberFormat('es-CO', {
            style: 'currency',
            currency: 'COP',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(price);
    }

    function renderProducts(products) {
        productosTable.innerHTML = ''; // Limpiar tabla

        products.forEach((product, index) => {
            const row = productosTable.insertRow();
            row.innerHTML = `
                <td>${index + 1}</td>
                <td><img src="static/images/${product.imagen}" alt="${product.nombre}" style="width: 50px; height: 50px;"></td>
                <td>${product.nombre}</td>
                <td>${product.descripcion}</td>
                <td>${formatPrice(product.precio)}</td>
                <td>${product.stock}</td>
                <td>${product.categoriaNombre || 'N/A'}</td>
                <td>${product.talla || 'N/A'}</td>
                <td>
                    <a href="#editarProducto" class="edit-button" data-toggle="modal" data-id="${product.idProducto}">
                        <i class="material-icons" data-toggle="tooltip" title="Edit">&#xE254;</i>
                    </a>
                    <a href="#eliminarProducto" class="delete-button" data-toggle="modal" data-id="${product.idProducto}">
                        <i class="material-icons" data-toggle="tooltip" title="Delete">&#xE872;</i>
                    </a>
                </td>
            `;
        });

        initializeEventListeners();
    }

    function renderPagination(totalItems, itemsPerPage, currentPage) {
        const totalPages = Math.ceil(totalItems / itemsPerPage);
        paginationElement.innerHTML = '';

        if (currentPage > 1) {
            paginationElement.innerHTML += `<li class="page-item"><a href="#" class="page-link" data-page="${currentPage - 1}">Anterior</a></li>`;
        } else {
            paginationElement.innerHTML += `<li class="page-item disabled"><a href="#" class="page-link">Anterior</a></li>`;
        }

        for (let i = 1; i <= totalPages; i++) {
            paginationElement.innerHTML += `<li class="page-item ${i === currentPage ? 'active' : ''}"><a href="#" class="page-link" data-page="${i}">${i}</a></li>`;
        }

        if (currentPage < totalPages) {
            paginationElement.innerHTML += `<li class="page-item"><a href="#" class="page-link" data-page="${currentPage + 1}">Siguiente</a></li>`;
        } else {
            paginationElement.innerHTML += `<li class="page-item disabled"><a href="#" class="page-link">Siguiente</a></li>`;
        }

        initializePaginationEventListeners();
    }

    function initializeEventListeners() {
        document.querySelectorAll('.edit-button').forEach(button => {
            button.addEventListener('click', function () {
                const productoId = this.getAttribute('data-id');
                const form = document.getElementById('editarProductoForm');
                form.action = `/update_product/${productoId}`;

                fetch(`/producto/${productoId}`)
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('nombreEdit').value = data.nombre || '';
                        document.getElementById('descripcionEdit').value = data.descripcion || '';
                        document.getElementById('precioEdit').value = data.precio || '';
                        document.getElementById('stockEdit').value = data.stock || '';

                        const fileInput = document.getElementById('imagenEdit');
                        const fileName = document.querySelector('.file-name-edit');
                        const container = document.querySelector('.file-upload-container-edit');
                        const imagenActualInput = document.getElementById('imagenActual');

                        if (data.imagen) {
                            fileName.textContent = data.imagen;
                            container.classList.add('file-selected-edit', 'file-has-image');
                            imagenActualInput.value = data.imagen;
                        } else {
                            fileName.textContent = '';
                            container.classList.remove('file-selected-edit', 'file-has-image');
                            imagenActualInput.value = '';
                        }
                    })
                    .catch(error => console.error('Error:', error));
            });
        });

        document.querySelectorAll('.delete-button').forEach(button => {
            button.addEventListener('click', function () {
                const productoId = this.getAttribute('data-id');
                const deleteForm = document.getElementById('deleteForm');
                deleteForm.action = `/delete_product/${productoId}`;
                $('#eliminarProducto').modal('show');
            });
        });
    }

    function initializePaginationEventListeners() {
        document.querySelectorAll('.page-link').forEach(link => {
            link.addEventListener('click', function (event) {
                event.preventDefault();
                const page = parseInt(this.getAttribute('data-page'));
                if (!isNaN(page)) {
                    currentPage = page;
                    renderCurrentPage();
                }
            });
        });
    }

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
        renderProducts(productos.slice(start, end));
        renderPagination(productos.length, itemsPerPage, currentPage);
    }

    searchForm.addEventListener('submit', function (event) {
        event.preventDefault();
        filterProducts(searchInput.value);
    });

    fetch('/api/productos')
        .then(response => response.json())
        .then(data => {
            productos = data;
            renderCurrentPage();
        })
        .catch(error => console.error('Error fetching products:', error));
});