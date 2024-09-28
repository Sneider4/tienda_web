// Funcion de buscar con el search
document.getElementById('searchInput').addEventListener('keyup', function() {
    const searchValue = this.value.toLowerCase();
    const tableBody = document.getElementById('productTable');
    const tableRows = tableBody.querySelectorAll('tr');
    let rowVisible = false;

    tableRows.forEach(function(row) {
        const cells = row.querySelectorAll('td');
        let match = false;

        cells.forEach(function(cell) {
            if (cell.textContent.toLowerCase().includes(searchValue)) {
                match = true;
            }
        });

        if (match) {
            row.style.display = '';
            rowVisible = true;
        } else {
            row.style.display = 'none';
        }
    });

    if (!rowVisible) {
        removeNoResultsRow();

        const noResultsRow = document.createElement('tr');
        const noResultsCell = document.createElement('td');
        noResultsCell.textContent = 'No hay productos similares';
        noResultsRow.appendChild(noResultsCell);
        tableBody.appendChild(noResultsRow);
    } else {
        removeNoResultsRow();
    }
});

function removeNoResultsRow() {
    const tableBody = document.getElementById('productTable');
    const noResultsRow = tableBody.querySelector('.no-results-row');
    if (noResultsRow) {
        tableBody.removeChild(noResultsRow);
    }
}