document.addEventListener('DOMContentLoaded', function () {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const productosTable = document.getElementById('productosTable').getElementsByTagName('tbody')[0];
    const paginationContainer = document.getElementById('pagination');

    const itemsPerPage = 5;
    let currentPage = 1;
    let productos = [];

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
        renderPagination(filteredProducts.length);
    }

    function renderProducts(products) {
        productosTable.innerHTML = '';
        products.forEach(product => {
            const row = productosTable.insertRow();
            row.insertCell()
            row.insertCell().innerHTML = `<img src="/static/images/productos-insertados/${product.imagen}" alt="${product.nombre}" style="width: 50px; height: 50px;">`;
            row.insertCell().textContent = product.nombre;
            row.insertCell().textContent = product.descripcion;
            row.insertCell().textContent = `$${product.precio.toLocaleString()}`;
            row.insertCell().textContent = product.stock;
            row.insertCell().textContent = product.categoriaNombre;
            row.insertCell().textContent = product.talla;
            row.insertCell().innerHTML = `
                <a href="#editarProducto" class="edit-button" data-toggle="modal" data-id="${product.idProducto}">
                    <i class="material-icons" data-toggle="tooltip" title="Edit">&#xE254;</i>
                </a>
                <a href="#eliminarProducto" class="delete" data-toggle="modal" data-id="${product.idProducto}">
                    <i class="material-icons" data-toggle="tooltip" title="Delete">&#xE872;</i>
                </a>
            `;
        });

        attachEventListeners();
    }

    function renderPagination(totalItems) {
        paginationContainer.innerHTML = '';

        const totalPages = Math.ceil(totalItems / itemsPerPage);

        const createPageItem = (page, isActive = false) => {
            const li = document.createElement('li');
            li.className = `page-item ${isActive ? 'active' : ''}`;
            const a = document.createElement('a');
            a.className = 'page-link';
            a.href = '#';
            a.textContent = page;
            a.addEventListener('click', function (event) {
                event.preventDefault();
                currentPage = page;
                filterProducts(searchInput.value);
            });
            li.appendChild(a);
            return li;
        };

        const createPrevNextItem = (text, isDisabled, handler) => {
            const li = document.createElement('li');
            li.className = `page-item ${isDisabled ? 'disabled' : ''}`;
            const a = document.createElement('a');
            a.className = 'page-link';
            a.href = '#';
            a.textContent = text;
            a.addEventListener('click', function (event) {
                event.preventDefault();
                if (!isDisabled) handler();
            });
            li.appendChild(a);
            return li;
        };

        paginationContainer.appendChild(createPrevNextItem('Anterior', currentPage === 1, () => {
            currentPage--;
            filterProducts(searchInput.value);
        }));

        for (let page = 1; page <= totalPages; page++) {
            paginationContainer.appendChild(createPageItem(page, page === currentPage));
        }

        paginationContainer.appendChild(createPrevNextItem('Siguiente', currentPage === totalPages, () => {
            currentPage++;
            filterProducts(searchInput.value);
        }));
    }

    function fetchProductos() {
        fetch('/api/productos')
            .then(response => response.json())
            .then(data => {
                productos = data;
                filterProducts(searchInput.value); // Renderizar la primera página de productos
            })
            .catch(error => console.error('Error fetching products:', error));
    }

    function attachEventListeners() {
        // Configuración del botón de edición
        const editButtons = document.querySelectorAll('.edit-button');
        editButtons.forEach(button => {
            button.addEventListener('click', function () {
                const productoId = this.getAttribute('data-id');
                const form = document.getElementById('editarProductoForm');
                form.action = `/update_product/${productoId}`;

                fetch(`/producto/data/${productoId}`)
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
                            container.classList.add('file-selected-edit');
                            container.classList.add('file-has-image');
                            imagenActualInput.value = data.imagen;
                        } else {
                            fileName.textContent = '';
                            container.classList.remove('file-selected-edit');
                            container.classList.remove('file-has-image');
                            imagenActualInput.value = '';
                        }
                    })
                    .catch(error => console.error('Error:', error));
            });
        });

        // Configuración del botón de eliminación
        const deleteButtons = document.querySelectorAll('.delete');
        deleteButtons.forEach(button => {
            button.addEventListener('click', function () {
                const productoId = this.getAttribute('data-id');
                const deleteForm = document.getElementById('deleteForm');
                deleteForm.action = `/delete_product/${productoId}`;
                $('#eliminarProducto').modal('show');
            });
        });
    }

    // Llamada inicial para obtener productos
    fetchProductos();

    // Función de búsqueda en tiempo real
    searchInput.addEventListener('keyup', function () {
        filterProducts(searchInput.value);
    });
});
