(function() {
    function inyectarBotonTienda() {
        // Si el botón ya fue inyectado en el menú actual, no hacemos nada
        if (document.getElementById('enlace-retorno-tienda')) return;

        // Buscamos de forma masiva cualquier enlace o elemento que tenga el texto exacto
        const todosLosElementos = document.querySelectorAll('a, span, div, p');
        let botonPerfil = null;

        for (let el of todosLosElementos) {
            if (el.textContent.trim() === 'Ver perfil') {
                botonPerfil = el;
                break;
            }
        }

        // Si encontramos el botón "Ver perfil", le metemos "Ver tienda" justo arriba
        if (botonPerfil) {
            const nuevoEnlace = document.createElement('a');
            nuevoEnlace.id = 'enlace-retorno-tienda';
            nuevoEnlace.href = '/'; // Te regresa a la raíz de tu tienda HTML
            
            // Le copiamos las clases exactas para que herede el diseño (márgenes, tipografía, hovers)
            nuevoEnlace.className = botonPerfil.className;
            
            // Si tiene estilos en línea del tema, se los copiamos también
            if (botonPerfil.getAttribute('style')) {
                nuevoEnlace.setAttribute('style', botonPerfil.getAttribute('style'));
            }

            # Estilos de seguridad para asegurar que se adapte visualmente al menú desplegable
            nuevoEnlace.style.display = 'block';
            nuevoEnlace.style.padding = '10px 15px';
            nuevoEnlace.style.color = '#28a745'; // Color verde llamativo para identificarlo
            nuevoEnlace.style.fontWeight = 'bold';
            nuevoEnlace.style.textDecoration = 'none';

            // Estructura interna idéntica al menú
            nuevoEnlace.innerHTML = `
                <i class="fas fa-store" style="margin-right: 8px; color: #28a745;"></i> Ver tienda
            `;

            // Lo colocamos exactamente encima de "Ver perfil"
            botonPerfil.parentNode.insertBefore(nuevoEnlace, botonPerfil);
        }
    }

    // Ejecutamos la función de inmediato al cargar la página
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', inyectarBotonTienda);
    } else {
        inyectarBotonTienda();
    }

    // Monitoreamos el DOM constantemente. Cuando haces clic en el usuario y el tema de Django
    // dibuja el cuadro de "Cuenta", este observador detecta a "Ver perfil" y le clona el botón al instante
    const observadorDOM = new MutationObserver(function(mutaciones) {
        inyectarBotonTienda();
    });

    observadorDOM.observe(document.body, {
        childList: true,
        subtree: true
    });
})();
