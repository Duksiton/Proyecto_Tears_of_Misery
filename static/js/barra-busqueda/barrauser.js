document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const usuariosTable = document.getElementById("usuariosTable");
    const tableBody = usuariosTable.getElementsByTagName("tbody")[0];
    const paginationContainer = document.getElementById("pagination");
  
    const itemsPerPage = 5;
    let currentPage = 1;
    let totalItems = 0;
    let usuarios = [];
  
    function filterUsers(query) {
      fetchUsuarios(query); // Fetch data with the current query
    }
  
    function renderUsers(users) {
      tableBody.innerHTML = "";
      users.forEach((user) => {
        const row = tableBody.insertRow();
        row.insertCell();
        row.insertCell().textContent = user.nombre;
        row.insertCell().textContent = user.email;
        row.insertCell().textContent = user.direccion;
        row.insertCell().textContent = user.telefono;
        row.insertCell().textContent = user.nombreRol;
        row.insertCell().innerHTML = `
          <a href="#editarUsuario" class="edit-button" data-toggle="modal" data-id="${user.idUsuario}">
              <i class="material-icons" data-toggle="tooltip" title="Edit">&#xE254;</i>
          </a>
          <a href="#eliminarUsuario" class="delete" data-toggle="modal" data-id="${user.idUsuario}">
              <i class="material-icons" data-toggle="tooltip" title="Delete">&#xE872;</i>
          </a>
        `;
      });
  
      // Re-attach event listeners for edit and delete buttons
      attachEditListeners();
      attachDeleteListeners();
    }
  
    function renderPagination(totalItems) {
      paginationContainer.innerHTML = "";
  
      const totalPages = Math.ceil(totalItems / itemsPerPage);
  
      const createPageItem = (page, isActive = false) => {
        const li = document.createElement("li");
        li.className = `page-item ${isActive ? "active" : ""}`;
        const a = document.createElement("a");
        a.className = "page-link";
        a.href = "#";
        a.textContent = page;
        a.addEventListener("click", function (event) {
          event.preventDefault();
          currentPage = page;
          filterUsers(searchInput.value);
        });
        li.appendChild(a);
        return li;
      };
  
      const createPrevNextItem = (text, isDisabled, handler) => {
        const li = document.createElement("li");
        li.className = `page-item ${isDisabled ? "disabled" : ""}`;
        const a = document.createElement("a");
        a.className = "page-link";
        a.href = "#";
        a.textContent = text;
        a.addEventListener("click", function (event) {
          event.preventDefault();
          if (!isDisabled) handler();
        });
        li.appendChild(a);
        return li;
      };
  
      paginationContainer.appendChild(
        createPrevNextItem("Anterior", currentPage === 1, () => {
          currentPage--;
          filterUsers(searchInput.value);
        })
      );
  
      for (let page = 1; page <= totalPages; page++) {
        paginationContainer.appendChild(
          createPageItem(page, page === currentPage)
        );
      }
  
      paginationContainer.appendChild(
        createPrevNextItem("Siguiente", currentPage === totalPages, () => {
          currentPage++;
          filterUsers(searchInput.value);
        })
      );
    }
  
    function fetchUsuarios(query = "") {
      fetch(
        `/api/usuarios?page=${currentPage}&items_per_page=${itemsPerPage}&query=${encodeURIComponent(query)}`
      )
        .then((response) => response.json())
        .then((data) => {
          usuarios = data.usuarios;
          totalItems = data.total;
          renderUsers(usuarios);
          renderPagination(totalItems);
        })
        .catch((error) => console.error("Error fetching users:", error));
    }
  
    function attachEditListeners() {
      const editButtons = document.querySelectorAll(".edit-button");
  
      editButtons.forEach(button => {
        button.addEventListener("click", function () {
          const usuarioId = this.getAttribute("data-id");
          const form = document.getElementById("editarUsuarioForm");
          form.action = `/update_user/${usuarioId}`;
  
          fetch(`/usuarios/${usuarioId}`)
            .then(response => {
              if (!response.ok) {
                throw new Error("Network response was not ok");
              }
              return response.json();
            })
            .then(data => {
              console.log("Datos recibidos correctamente del servidor:");
  
              document.getElementById("nombreEditar").value = data.nombre || "";
              document.getElementById("emailEditar").value = data.email || "";
              document.getElementById("contraseñaEditar").value = data.contraseña || "";
              document.getElementById("direccionEditar").value = data.direccion || "";
              document.getElementById("telefonoEditar").value = data.telefono || "";
  
              const selectRol = document.getElementById("nombreRolEditar");
              if (selectRol) {
                for (let i = 0; i < selectRol.options.length; i++) {
                  if (selectRol.options[i].value === data.nombreRol) {
                    selectRol.selectedIndex = i;
                    break;
                  }
                }
              }
  
              console.log("Nombre: OK");
              console.log("Email: OK");
              console.log("Contraseña: OK");
              console.log("Dirección: OK");
              console.log("Teléfono: OK");
              console.log("NombreRol: OK");
            })
            .catch(error => {
              console.error("Error al obtener datos del usuario:", error);
            });
        });
      });
    }
  
    function attachDeleteListeners() {
      const deleteButtons = document.querySelectorAll(".delete");
  
      deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
          const usuarioId = this.getAttribute("data-id");
          const form = document.getElementById("deleteUserForm");
          form.action = `/delete_user/${usuarioId}`;
          document.getElementById("userIdToDelete").value = usuarioId;
  
          // Mostrar modal de confirmación (si está implementado)
          const deleteModal = document.getElementById("eliminarUsuario");
          if (deleteModal) {
            $(deleteModal).modal("show"); // Asumiendo que estás usando Bootstrap para el modal
          } else {
            console.error("Modal de eliminación no encontrado");
          }
        });
      });
    }
  
    function togglePasswordVisibility() {
      const passwordField = document.getElementById("contraseñaEditar");
      const eyeIcon = document.getElementById("eye-icon");
  
      if (passwordField.type === "password") {
        passwordField.type = "text";
        eyeIcon.classList.remove("far", "fa-eye");
        eyeIcon.classList.add("fas", "fa-eye-slash");
      } else {
        passwordField.type = "password";
        eyeIcon.classList.remove("fas", "fa-eye-slash");
        eyeIcon.classList.add("far", "fa-eye");
      }
    }
  
    const togglePasswordButton = document.getElementById("togglePasswordButton");
    if (togglePasswordButton) {
      togglePasswordButton.addEventListener("click", togglePasswordVisibility);
    } else {
      console.error("Botón de alternar contraseña no encontrado");
    }
  
    // Llamada inicial para obtener usuarios
    fetchUsuarios();
  
    // Función de búsqueda
    searchInput.addEventListener("keyup", function () {
      currentPage = 1; // Reset the page number when searching
      filterUsers(searchInput.value);
    });
  });
  document.addEventListener('DOMContentLoaded', function () {
    // Función para alternar la visibilidad de la contraseña
    function togglePasswordVisibility() {
        const passwordField = document.getElementById('contraseñaEditar');
        const eyeIcon = document.getElementById('eye-icon');

        if (passwordField.type === 'password') {
            passwordField.type = 'text';
            eyeIcon.classList.remove('far', 'fa-eye');
            eyeIcon.classList.add('fas', 'fa-eye-slash');
        } else {
            passwordField.type = 'password';
            eyeIcon.classList.remove('fas', 'fa-eye-slash');
            eyeIcon.classList.add('far', 'fa-eye');
        }
    }

    const togglePasswordButton = document.getElementById('togglePasswordButton');
    if (togglePasswordButton) {
        togglePasswordButton.addEventListener('click', togglePasswordVisibility);
    } else {
        console.error('Botón de alternar contraseña no encontrado');
    }
});
  