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
        const precioRedondeado = Math.round(precio * 100) / 100; // Redondear a 2 decimales
        const [parteEntera, parteDecimal] = precioRedondeado.toFixed(3).split('.'); // Formato con 2 decimales
        const parteEnteraFormateada = new Intl.NumberFormat('es-CO').format(parseInt(parteEntera)); // Formatear parte entera con separadores de miles
        return parteDecimal === '00' ? `$${parteEnteraFormateada}` : `$${parteEnteraFormateada}.${parteDecimal}`; // Usar punto en lugar de coma
    }
    

    function mostrarMensaje(mensaje, tipo = 'success') {
        modalContent.innerHTML = `
            <h2 style="color: ${tipo === 'success' ? '#28a745' : tipo === 'info' ? '#007bff' : '#dc3545'}; font-size: 36px; margin-bottom: 20px;">
                ${tipo === 'success' ? '¡Éxito!' : tipo === 'info' ? 'Información' : 'Atención'}
            </h2>
            <p style="font-size: 24px; margin-bottom: 30px;">${mensaje}</p>
            <button id="cerrarModal" 
                    style="background-color: #007bff; color: white; border: none; 
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
                    <button class="btn-remove" data-index="${index}" style="background-color: #c00000; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; margin-right: 5px;">Eliminar</button>
                    <br>
                    <br>
                    <button class="btn-comprar" data-index="${index}" style="background-color: #0c6834; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">Comprar</button>
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
            carrito[index].quantity += 1;
            mostrarMensaje(`Cantidad de "${product.name}" (${product.size}) aumentada. Ahora tienes ${carrito[index].quantity}.`, 'success');
        } else {
            carrito.push(product);
            mostrarMensaje(`Nuevo producto "${product.name}" (${product.size}) agregado al carrito.`, 'success');
        }
        actualizarCarrito();
    }

    // Supongamos que tienes una función o lógica que verifica si el usuario está logueado
    const usuarioLogueado = true; // Cambia a `true` si el usuario ha iniciado sesión.

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
                mostrarMensaje('Primero inicia sesión para realizar la compra.', 'info');
                return;
            }
        
            // Aquí se realiza la compra y se muestra el mensaje antes de redirigir
            const item = carrito[index];
            mostrarMensaje(`Has comprado ${item.quantity} ${item.name} (${item.size}) por ${formatearPrecio(item.price * item.quantity)}`);
            carrito.splice(index, 1); // Elimina el item del carrito después de mostrar el mensaje
            actualizarCarrito();
        
            // Redirigir al usuario a la página de perfil después de 3 segundos
            setTimeout(function() {
                window.location.href = '/perfil';
            }, 1500); // 3000 milisegundos = 3 segundos
            return;
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
            mostrarMensaje('Primero inicia sesión para realizar la compra.', 'info');
            return;
        }
    
        const total = carrito.reduce((sum, item) => sum + item.price * item.quantity, 0);
        mostrarMensaje(`Has comprado todos los productos por ${formatearPrecio(total)}. ¡Gracias por tu compra!`);
    
        // Limpia el carrito
        carrito.length = 0;
        actualizarCarrito();
    
        // Redirige a la página de perfil después de 3 segundos
        setTimeout(function() {
            window.location.href = '/perfil';
        }, 1500); // 3000 milisegundos = 3 segundos
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
                quantity: 1
            };

            agregarAlCarrito(product);
        });
    }

    actualizarCarrito();
});
