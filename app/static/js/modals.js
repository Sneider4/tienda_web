// Función para abrir el modal con la imagen seleccionada
function openModal(imageUrl, productName) {
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImage");
    const modalProductName = document.getElementById("modalProductName");

    modalImg.src = imageUrl;
    modalProductName.textContent = productName;

    modal.style.display = "block";
}

function closeModal() {
    const modal = document.getElementById("imageModal");
    modal.style.display = "none";
}
// Función para abrir el modal con la imagen seleccionada


// ---------


// funcion paera abrir el modal de confirmación de eliminación de producto

function openDeleteModal(productId) {
    const modal = document.getElementById("deleteModal");
    const deleteForm = document.getElementById("deleteForm");

    deleteForm.action = "/producto/delete/" + productId;    
    
    modal.style.display = "block";
}

function closeDeleteModal() {
    const modal = document.getElementById("deleteModal");
    modal.style.display = "none";
}
// funcion paera abrir el modal de confirmación de eliminación de producto


// ---------


// funcion paera abrir el modal de confirmación de eliminación de categoria
{function openDeleteModalCategoria(categoriaId) {

    const modal = document.getElementById("deleteModalCategoria");
    const deleteFormCategoria = document.getElementById("deleteFormCategoria");

    deleteFormCategoria.action = "/categoria/delete/" + categoriaId;    
    
    modal.style.display = "block";
}

function closeDeleteModalCategoria() {
    const modal = document.getElementById("deleteModalCategoria");
    modal.style.display = "none";
}}
// funcion paera abrir el modal de confirmación de eliminación de categoria


// ---------


// funcion paera abrir el modal de editar de producto
function openEditModal(productoId, nombre, descripcion, precio, stock, categoriaId, imagen) {
    
    const modal = document.getElementById("editModalProducto");
    const editForm = document.getElementById("editFormProducto");

    document.getElementById("edit_nombre").value = nombre;
    document.getElementById("edit_descripcion").value = descripcion;
    document.getElementById("edit_precio").value = precio;
    document.getElementById("edit_stock").value = stock;
    document.getElementById("edit_categoria").value = categoriaId;
    
    if (imagen) {
        document.getElementById("imagen_actual").src = "/static/images/" + imagen;
        document.getElementById("imagen_actual").style.display = "block";
    } else {
        document.getElementById("imagen_actual").style.display = "none";
    }

    editForm.action = "/producto/edit/" + productoId;

    modal.style.display = "block";
}

function closeEditModalProducto() {
    const modal = document.getElementById("editModalProducto");
    modal.style.display = "none";
}
// funcion paera abrir el modal de editar de producto


// ---------


// funcion paera abrir el modal de editar de categoria
function openEditModalCategoria(categoriaId, nombre, descripcion) {
    
    const modal = document.getElementById("editModalCategoria");
    const editForm = document.getElementById("editFormCategoria");

    document.getElementById("edit_categoria_nombre").value = nombre;
    document.getElementById("edit_categoria_descripcion").value = descripcion;

    editForm.action = "/categoria/edit/" + categoriaId;

    modal.style.display = "block";
}

function closeEditModalCategoria() {
    const modal = document.getElementById("editModalCategoria");
    modal.style.display = "none";
}
// funcion paera abrir el modal de editar de categoria


// ---------


// funcion paera abrir el modal de mostrar productos asociados
function openCategoryProductsModal(categoriaId) {
    fetch('/categoria/productos/' + categoriaId)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#productosTable tbody');
            tableBody.innerHTML = '';  

            if (data.length === 0) {
                tableBody.innerHTML = '<tr><td colspan="4">No hay productos asociados a esta categoría.</td></tr>';
            } else {

                data.forEach(producto => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${producto.nombre}</td>
                        <td>$${producto.precio.toFixed(3)}</td>
                        <td>${producto.stock}</td>
                        <td>
                            <button class="btn-1" onclick="openModal('/static/images/${producto.imagen}')" class="btn btn-primary btn-sm">Imagen</button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
            }

            const modal = document.getElementById('categoryProductsModal');
            modal.style.display = 'block';
        })
        .catch(error => console.error('Error al obtener los productos:', error));
}

function closeCategoryProductsModal() {
    const modal = document.getElementById('categoryProductsModal');
    modal.style.display = 'none';
}
// funcion paera abrir el modal de mostrar productos asociados
