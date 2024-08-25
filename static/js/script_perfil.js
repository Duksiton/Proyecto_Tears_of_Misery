document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('editar-perfil').addEventListener('click', function() {
        document.querySelectorAll('input').forEach(input => {
            input.removeAttribute('readonly');
        });
        this.textContent = 'Guardar Cambios'; // Cambia el texto del botón a "Guardar Cambios"
        this.setAttribute('type', 'submit'); // Cambia el tipo del botón a submit
    });
});
