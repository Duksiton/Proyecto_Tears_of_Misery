document.getElementById('toggle-menu').addEventListener('click', function () {
    var sidebar = document.getElementById('sidebar');
    if (sidebar.style.display === 'block') {
        sidebar.style.display = 'none';
    } else {
        sidebar.style.display = 'block';
    }
});

document.getElementById('toggle-update').addEventListener('click', function () {
    var userData = document.getElementById('user-data');
    var updateForm = document.getElementById('update-profile');
    if (updateForm.classList.contains('show')) {
        updateForm.classList.remove('show');
        userData.classList.remove('show');
    } else {
        updateForm.classList.add('show');
        userData.classList.add('show');
    }
});
