document.addEventListener('DOMContentLoaded', function() {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    console.log("Carrito cargado desde localStorage:", carrito);
    const totalCarritoSpan = document.getElementById('total-valor');
    const carritoContainer = document.getElementById('carrito');
    const imgCarrito = document.getElementById('img-carrito');
    const verMasContainer = document.getElementById('ver-mas-container');
    const verMasLink = document.getElementById('toggle-productos');
    let mostrarMas = false;

    // Ocultar el carrito inicialmente
    carritoContainer.style.display = 'none';

    // Evento para mostrar/ocultar el carrito al hacer clic en el icono
    imgCarrito.addEventListener('click', function() {
        carritoContainer.style.display = carritoContainer.style.display === 'none' ? 'block' : 'none';
    });
  
    document.addEventListener('click', function(event) {
        const imgCarrito = document.getElementById('img-carrito');
    
        // Solo cerrar el carrito si está visible
        if (carritoContainer.style.display === 'block') {
            // Cerrar carrito solo si se hace clic fuera del contenedor y del ícono
            if (!carritoContainer.contains(event.target) && !imgCarrito.contains(event.target)) {
                carritoContainer.style.display = 'none';
            }
        }
    });
    
    // Evitar que el clic dentro del carrito cierre el contenedor
    carritoContainer.addEventListener('click', function(event) {
        event.stopPropagation(); // Evita que el clic dentro del carrito cierre el carrito
    });
    
    document.addEventListener('DOMContentLoaded', function () {
        // Obtener los elementos del DOM
        const quantityInput = document.querySelector('.input-quantity');
        const incrementButton = document.querySelector('#increment');
        const decrementButton = document.querySelector('#decrement');
        const addToCartButton = document.querySelector('#add-to-cart');
    
        // Asegurarse de que el campo de cantidad tenga un valor válido
        quantityInput.value = parseInt(quantityInput.value, 10) || 1;
    
        // Evento de clic en el botón de incremento
        incrementButton.addEventListener('click', function () {
            let currentValue = parseInt(quantityInput.value, 10);
            quantityInput.value = currentValue + 1;
        });
    
        // Evento de clic en el botón de decremento
        decrementButton.addEventListener('click', function () {
            let currentValue = parseInt(quantityInput.value, 10);
            if (currentValue > 1) { // Evitar que el valor sea menor que 1
                quantityInput.value = currentValue - 1;
            }
        });
    
        // Asegurarse de que el campo de entrada solo acepte números válidos
        quantityInput.addEventListener('input', function () {
            const value = parseInt(quantityInput.value, 10);
            if (isNaN(value) || value < 1) {
                quantityInput.value = 1;
            }
        });
    
        // Evento de clic en el botón "Agregar al carrito"
        addToCartButton.addEventListener('click', function () {
            const productId = this.getAttribute('data-product-id');
            const quantity = parseInt(quantityInput.value, 10);
            const productName = this.getAttribute('data-name');
            const productPrice = parseFloat(this.getAttribute('data-price'));
            const size = document.getElementById('size') ? document.getElementById('size').value : "Album";
            const requiereTalla = addToCartButton.getAttribute('data-size') === 'required';

            if (requiereTalla && (!size || size === "")) {
                mostrarMensaje('Por favor selecciona una talla antes de agregar al carrito.', 'info');
                return;
            }

            let cart = JSON.parse(localStorage.getItem('cart')) || [];
            const existingProductIndex = cart.findIndex(item => item.id === productId && item.size === size);

            if (existingProductIndex > -1) {
                // Actualizar la cantidad si el producto ya está en el carrito
                cart[existingProductIndex].quantity += quantity;
            } else {
                // Añadir nuevo producto al carrito
                cart.push({
                    id: productId,
                    name: productName,
                    price: productPrice,
                    quantity: quantity,
                    size: size,
                    image: this.getAttribute('data-img')
                });
            }

            localStorage.setItem('cart', JSON.stringify(cart));
            mostrarMensaje(`Se han añadido ${quantity} ${productName}(s) (${size}) al carrito.`, 'success');
        });
    });

    // Crear el modal para mensajes
    const modal = document.createElement('div');
    modal.style.display = 'none';
    modal.style.position = 'fixed';
    modal.style.zIndex = '1000';
    modal.style.left = '0';
    modal.style.top = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.overflow = 'auto';
    modal.style.backgroundColor = 'rgba(0,0,0,0.4)';
    document.body.appendChild(modal);

    const modalContent = document.createElement('div');
    modalContent.style.backgroundColor = '#fefefe';
    modalContent.style.margin = '10% auto';
    modalContent.style.padding = '40px';
    modalContent.style.border = '1px solid #888';
    modalContent.style.width = '90%';
    modalContent.style.maxWidth = '700px';
    modalContent.style.borderRadius = '15px';
    modalContent.style.textAlign = 'center';
    modalContent.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
    modal.appendChild(modalContent);

    function formatearPrecio(precio) {
        const precioRedondeado = Math.round(precio * 100) / 100;
        const [parteEntera, parteDecimal] = precioRedondeado.toFixed(2).split('.');
        const parteEnteraFormateada = new Intl.NumberFormat('es-CO').format(parseInt(parteEntera));
        return parteDecimal === '00' ? `$${parteEnteraFormateada}` : `$${parteEnteraFormateada},${parteDecimal}`;
    }

    function mostrarMensaje(mensaje, tipo = 'success') {
        modalContent.innerHTML = `
            <h2 style="color: ${tipo === 'success' ? '#ffbb00' : tipo === 'info' ? '#ffbb00' : '#dc3545'}; font-size: 36px; margin-bottom: 20px;">
                ${tipo === 'success' ? '¡Éxito!' : tipo === 'info' ? 'Información' : 'Atención'}
            </h2>
            <p style="font-size: 24px; margin-bottom: 30px;">${mensaje}</p>
            <button id="cerrarModal" 
                    style="background-color: #ffbb00; color: black; border: none; 
                    padding: 15px 30px; margin-top: 20px; border-radius: 8px; cursor: pointer;
                    font-size: 20px; transition: background-color 0.3s;">
                Cerrar
            </button>
        `;
        modal.style.display = 'block';
    
        document.getElementById('cerrarModal').addEventListener('click', function() {
            modal.style.display = 'none';
        });
    
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    }

    function actualizarCarrito() {
        const carritoBody = document.getElementById('productos');
        carritoBody.innerHTML = '';

        const itemsMostrar = mostrarMas ? carrito : carrito.slice(0, 3);

        itemsMostrar.forEach((item, index) => {
            const row = carritoBody.insertRow();
            row.innerHTML = `
                <td><img src="${item.img}" alt="${item.name}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;"></td>
                <td style="font-weight: bold;">${item.name} (${item.size}) ${item.quantity > 1 ? `x${item.quantity}` : ''}</td>
                <td style="color: #000;">${formatearPrecio(item.price * item.quantity)}</td>
                <td>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <button class="btn-decrease" data-index="${index}" style="background-color: #b4b6b9; color: black; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">-</button>
                        <span style="margin: 0 5px;">${item.quantity}</span>
                        <button class="btn-increase" data-index="${index}" style="background-color: #b4b6b9; color: black; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">+</button>
                    </div>
                </td>
                <td>
                    <button class="btn-remove" data-index="${index}" style="background-color: transparent; color: #c00000; border: none; padding: 6px; border-radius: 6px; cursor: pointer; margin-right: 6px; font-size: 12px;">
                        <i class="fas fa-trash-alt" style="font-size: 14px; color: #c00000;"></i>
                    </button>
                    <br>
                    <br>
                </td>
            `;
        });

        const total = carrito.reduce((sum, item) => sum + item.price * item.quantity, 0);
        totalCarritoSpan.textContent = formatearPrecio(total);

        verMasContainer.style.display = carrito.length > 3 ? 'block' : 'none';
        verMasLink.textContent = mostrarMas ? 'Ocultar productos' : 'Ver más productos agregados';

        localStorage.setItem('carrito', JSON.stringify(carrito));
    }

    function agregarAlCarrito(product) {
        const index = carrito.findIndex(item => item.name === product.name && item.size === product.size);
        if (index !== -1) {
            carrito[index].quantity += product.quantity;
            mostrarMensaje(`Cantidad de "${product.name}" (${product.size}) aumentada. Ahora tienes ${carrito[index].quantity}.`, 'success');
        } else {
            carrito.push(product);
            mostrarMensaje(`Nuevo producto "${product.name}" (${product.size}) agregado al carrito.`, 'success');
        }
        actualizarCarrito();
    }

    const usuarioLogueado = false; // Cambia a `true` si el usuario ha iniciado sesión.

    document.getElementById('productos').addEventListener('click', function(e) {
        const index = parseInt(e.target.dataset.index);

        if (e.target.classList.contains('btn-increase')) {
            carrito[index].quantity += 1;
            actualizarCarrito();
        }

        if (e.target.classList.contains('btn-decrease')) {
            if (carrito[index].quantity > 1) {
                carrito[index].quantity -= 1;
            } else {
                carrito.splice(index, 1);
            }
            actualizarCarrito();
        }

        if (e.target.classList.contains('btn-comprar')) {
            if (!usuarioLogueado) {
                mostrarMensaje('Primero inicia sesión para realizar la compra.', '');
                return;
            }

            const item = carrito[index];
            mostrarMensaje(`Has comprado ${item.quantity} ${item.name} (${item.size}) por ${formatearPrecio(item.price * item.quantity)}`);
            carrito.splice(index, 1);
            actualizarCarrito();
        }
        
        if (e.target.classList.contains('btn-remove')) {
            carrito.splice(index, 1);
            actualizarCarrito();
        }
    });

    document.getElementById('vaciar-carrito').addEventListener('click', function() {
        if (carrito.length === 0) {
            mostrarMensaje('El carrito ya está vacío.', 'info');
        } else {
            carrito.length = 0;
            actualizarCarrito();
            mostrarMensaje('El carrito ha sido vaciado.', 'info');
        }
    });

    document.getElementById('comprar-todo').addEventListener('click', function() {
        if (carrito.length === 0) {
            mostrarMensaje('El carrito está vacío.', 'info');
            return;
        }

        if (!usuarioLogueado) {
            mostrarMensaje('Primero inicia sesión para realizar la compra.', '');
            return;
        }

        const total = carrito.reduce((sum, item) => sum + item.price * item.quantity, 0);
        mostrarMensaje(`Has comprado todos los productos por ${formatearPrecio(total)}. ¡Gracias por tu compra!`);
        carrito.length = 0;
        actualizarCarrito();
    });

    verMasLink.addEventListener('click', function() {
        mostrarMas = !mostrarMas;
        actualizarCarrito();
    });

    // Agrega el evento para el botón "Agregar al carrito" en la página de detalles del producto
    const addToCartButton = document.getElementById('add-to-cart');
    if (addToCartButton) {
        addToCartButton.addEventListener('click', () => {
            const size = document.getElementById('size') ? document.getElementById('size').value : null;
            const requiereTalla = addToCartButton.getAttribute('data-size') === 'required';
            const quantityInput = document.querySelector('.input-quantity');
            const quantity = parseInt(quantityInput.value, 10) || 1;

            if (requiereTalla && (!size || size === "")) {
                mostrarMensaje('Por favor selecciona una talla antes de agregar al carrito.', 'info');
                return;
            }

            const product = {
                id: addToCartButton.getAttribute('data-product-id'),
                name: addToCartButton.getAttribute('data-name'),
                price: parseFloat(addToCartButton.getAttribute('data-price')),
                img: addToCartButton.getAttribute('data-img'),
                size: requiereTalla ? (size || "Album") : "Album",
                quantity: quantity
            };

            agregarAlCarrito(product);
        });
    }

    actualizarCarrito();
});

// Selecciona los elementos
const carrito = document.querySelector('#carrito');
const abrirCarritoBtn = document.querySelector('#abrir-carrito');
const closeBtn = document.querySelector('.close-btn');

// Función para cerrar el carrito
function cerrarCarrito() {
    carrito.style.display = 'none';
}

// Abrir el carrito
abrirCarritoBtn.addEventListener('click', function(event) {
    event.stopPropagation(); // Evita que el clic se propague
    carrito.style.display = 'block'; // Muestra el carrito
});

// Cerrar el carrito al hacer clic en el botón de cierre
closeBtn.addEventListener('click', cerrarCarrito);

// Cerrar el carrito al hacer clic fuera del carrito
document.addEventListener('click', function(event) {
    if (carrito.style.display === 'block' && !carrito.contains(event.target) && !abrirCarritoBtn.contains(event.target)) {
        cerrarCarrito();
    }
});

// Evitar que el carrito se cierre al hacer clic dentro de él
carrito.addEventListener('click', function(event) {
    event.stopPropagation(); // Evita que el clic se propague al documento
});
