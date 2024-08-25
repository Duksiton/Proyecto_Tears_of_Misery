document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const usuariosTable = document.getElementById('usuariosTable');
    const tableRows = usuariosTable.getElementsByTagName('tr');

    searchInput.addEventListener('keyup', function () {
        const searchTerm = searchInput.value.toLowerCase();

        for (let i = 1; i < tableRows.length; i++) { // Empezamos desde 1 para saltar el encabezado
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
