(function() {
    function crearBotonFlotanteTienda() {
        // Evitamos duplicar el botón si ya existe en la pantalla
        if (document.getElementById('boton-flotante-tienda-fijo')) return;

        // 1. Creamos el elemento de enlace (A)
        var boton = document.createElement('a');
        boton.id = 'boton-flotante-tienda-fijo';
        boton.href = '/'; // Te regresa directo a la tienda principal
        boton.innerHTML = '<i class="fas fa-shopping-basket" style="margin-right: 8px;"></i> Ver Tienda 🏪';

        // 2. Le aplicamos los estilos CSS directamente por JS para asegurar inmunidad
        boton.style.position = 'fixed';
        boton.style.bottom = '25px';
        boton.style.right = '25px';
        boton.style.backgroundColor = '#28a745'; // Verde éxito
        boton.style.color = '#ffffff';
        boton.style.fontWeight = 'bold';
        boton.style.fontSize = '15px';
        boton.style.padding = '12px 22px';
        boton.style.borderRadius = '50px';
        boton.style.boxShadow = '0px 5px 15px rgba(0, 0, 0, 0.3)';
        boton.style.zIndex = '999999'; // Por encima de cualquier capa de Jazzmin
        boton.style.textDecoration = 'none';
        boton.style.display = 'flex';
        boton.style.alignItems = 'center';
        boton.style.justifyContent = 'center';
        boton.style.transition = 'transform 0.2s ease';
        boton.style.cursor = 'pointer';

        # Efecto visual al pasar el cursor o presionar en celular
        boton.addEventListener('mouseenter', function() { boton.style.transform = 'scale(1.05)'; boton.style.backgroundColor = '#218838'; });
        boton.addEventListener('mouseleave', function() { boton.style.transform = 'scale(1)'; boton.style.backgroundColor = '#28a745'; });

        // Ajuste responsivo para celulares pequeños
        if (window.innerWidth <= 768) {
            boton.style.bottom = '20px';
            boton.style.right = '20px';
            boton.style.padding = '10px 18px';
            boton.style.fontSize = '14px';
        }

        // 3. Lo clavamos directo en el Body del HTML
        document.body.appendChild(boton);
    }

    // Ejecutamos la función en cuanto carga la ventana
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', crearBotonFlotanteTienda);
    } else {
        crearBotonFlotanteTienda();
    }
})();
