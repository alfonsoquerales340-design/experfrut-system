document.addEventListener('DOMContentLoaded', function() {
    function agregarBotonRegresar() {
        // Buscamos el contenedor flotante negro que me mostraste en la foto
        const userTools = document.getElementById('user-tools') || 
                          document.querySelector('.sticky-nav-user') || 
                          document.querySelector('#header');
        
        if (userTools) {
            // Intentamos buscar la lista interna de enlaces del perfil móvil
            let userLinks = userTools.querySelector('.dropdown-contents') || 
                            userTools.querySelector('.dropdown-menu') || 
                            userTools.querySelector('.dropdown-content');
            
            // Si el diseño responsive colapsa el menú de manera plana
            if (!userLinks) {
                userLinks = userTools;
            }
            
            // Evitamos duplicaciones molestas en la interfaz
            if (userLinks && !document.getElementById('enlace-retorno-tienda')) {
                const tiendaLi = document.createElement('div');
                tiendaLi.id = 'enlace-retorno-tienda';
                tiendaLi.style.borderTop = '1px solid #444';
                tiendaLi.style.marginTop = '6px';
                tiendaLi.style.paddingTop = '4px';
                tiendaLi.innerHTML = `
                    <a href="/" style="color: #28a745; font-weight: bold; display: block; padding: 10px 15px; text-decoration: none; font-size: 13px;">
                        <i class="fas fa-shopping-basket" style="margin-right: 6px;"></i> Regresar a Tienda
                    </a>
                `;
                userLinks.appendChild(tiendaLi);
            }
        }
    }

    // Se ejecuta al instante y lleva un temporizador por si la carga de red en móviles demora
    agregarBotonRegresar();
    setTimeout(agregarBotonRegresar, 600);
});
