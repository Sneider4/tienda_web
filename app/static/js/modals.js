// Función para abrir el modal con la imagen seleccionada
function openModal(imageUrl) {
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImage");

    // Establecer la imagen en el modal
    modalImg.src = imageUrl;

    // Mostrar el modal
    modal.style.display = "block";
}

// Función para cerrar el modal
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
    
    // Actualizar la acción del formulario con el ID del producto
    deleteForm.action = "/producto/delete/" + productId;
    
    // Mostrar el modal
    modal.style.display = "block";
}

// Cerrar el modal
function closeDeleteModal() {
    const modal = document.getElementById("deleteModal");
    modal.style.display = "none";
}
// funcion paera abrir el modal de confirmación de eliminación de producto
