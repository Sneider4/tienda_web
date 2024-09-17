function mostrarFormulario(metodoPago) {
    // Ocultar todos los formularios
    document.getElementById('form-credito').style.display = 'none';
    document.getElementById('form-debito').style.display = 'none';
    document.getElementById('form-pse').style.display = 'none';

    // Mostrar el formulario correspondiente
    if (metodoPago === 'credito') {
        document.getElementById('form-credito').style.display = 'block';
    } else if (metodoPago === 'debito') {
        document.getElementById('form-debito').style.display = 'block';
    } else if (metodoPago === 'pse') {
        document.getElementById('form-pse').style.display = 'block';
    }
}

// Función para seleccionar un li y deseleccionar los demás
function seleccionarOpcion(element) {
    var lista = document.getElementById("lista-pagos").getElementsByTagName("li");
    for (var i = 0; i < lista.length; i++) {
        lista[i].classList.remove("selected");
    }
    element.parentElement.classList.add("selected"); 
}