document.addEventListener('DOMContentLoaded', function () {
    const productosTable = document.getElementById('productosTable').getElementsByTagName('tbody')[0];
    const pagination = document.getElementById('pagination');
    const itemsPerPage = 10; // Número máximo de productos por página
    let productos = [];
    let currentPage = 1;

    // Función para formatear precios
    function formatPrice(price) {
        return new Intl.NumberFormat('es-CO', {
            style: 'currency',
            currency: 'COP',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(price);
    }

    // Función para renderizar productos en la tabla
    function renderProducts(page) {
        productosTable.innerHTML = ''; // Limpiar tabla

        const start = (page - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        const paginatedProducts = productos.slice(start, end);

        paginatedProducts.forEach(product => {
            const row = productosTable.insertRow();
            row.innerHTML = `
                <td></td>
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

        updatePagination();
        initializeEventListeners();
    }

    // Función para actualizar los botones de paginación
    function updatePagination() {
        pagination.innerHTML = ''; // Limpiar paginación

        const pageCount = Math.ceil(productos.length / itemsPerPage);

        if (currentPage > 1) {
            const prevButton = document.createElement('li');
            prevButton.className = 'page-item';
            prevButton.innerHTML = `<a href="#" class="page-link">Previous</a>`;
            prevButton.querySelector('a').addEventListener('click', function () {
                currentPage--;
                renderProducts(currentPage);
            });
            pagination.appendChild(prevButton);
        }

        for (let i = 1; i <= pageCount; i++) {
            const pageItem = document.createElement('li');
            pageItem.className = `page-item ${i === currentPage ? 'active' : ''}`;
            pageItem.innerHTML = `<a href="#" class="page-link">${i}</a>`;
            pageItem.querySelector('a').addEventListener('click', function () {
                currentPage = i;
                renderProducts(currentPage);
            });
            pagination.appendChild(pageItem);
        }

        if (currentPage < pageCount) {
            const nextButton = document.createElement('li');
            nextButton.className = 'page-item';
            nextButton.innerHTML = `<a href="#" class="page-link">Next</a>`;
            nextButton.querySelector('a').addEventListener('click', function () {
                currentPage++;
                renderProducts(currentPage);
            });
            pagination.appendChild(nextButton);
        }
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
                        // Rellenar el formulario de edición con los datos del producto
                        document.getElementById('nombreEdit').value = data.nombre || '';
                        document.getElementById('descripcionEdit').value = data.descripcion || '';
                        document.getElementById('precioEdit').value = data.precio || '';
                        document.getElementById('stockEdit').value = data.stock || '';

                        // Manejo de la imagen
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

        document.querySelectorAll('.delete-button').forEach(button => {
            button.addEventListener('click', function () {
                const productoId = this.getAttribute('data-id');
                const deleteForm = document.getElementById('deleteForm');
                deleteForm.action = `/delete_product/${productoId}`;
                $('#eliminarProducto').modal('show');
            });
        });
    }

    function loadProducts() {
        fetch('/api/productos')
            .then(response => response.json())
            .then(data => {
                productos = data;
                renderProducts(currentPage);
            })
            .catch(error => console.error('Error:', error));
    }

    loadProducts();
});
