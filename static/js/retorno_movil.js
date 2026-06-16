document.addEventListener('DOMContentLoaded', function() {
    function agregarBotonRegresar() {
        // Evitamos duplicaciones molestas si el script se ejecuta dos veces
        if (document.getElementById('enlace-retorno-tienda')) return;

        // 1. Buscamos el contenedor flotante o menú del usuario
        const userTools = document.getElementById('user-tools') || 
                          document.querySelector('.sticky-nav-user') || 
                          document.querySelector('#header') ||
                          document.body;

        if (userTools) {
            // 2. Buscamos todos los elementos dentro del menú para encontrar el ancla
            const items = userTools.querySelectorAll('a, div, span, p');
            let targetElement = null;

            // Localizamos "Ver perfil" para posicionar el nuevo enlace
            for (let item of items) {
                if (item.textContent.trim() === 'Ver perfil') {
                    targetElement = item;
                    break;
                }
            }

            // 3. Si encontramos "Ver perfil", inyectamos "Ver tienda" justo arriba con su mismo estilo
            if (targetElement) {
                const tiendaLink = document.createElement('a');
                tiendaLink.id = 'enlace-retorno-tienda';
                tiendaLink.href = '/'; // Cambia esto por la URL de tu HTML de la tienda si es diferente (ej: '/tienda/')
                
                // Heredamos las clases de "Ver perfil" para que se vea idéntico
                tiendaLink.className = targetElement.className;
                
                if (targetElement.getAttribute('style')) {
                    tiendaLink.setAttribute('style', targetElement.getAttribute('style'));
                }

                // Estructura interna con icono y texto alineado al estilo del admin
                tiendaLink.innerHTML = `
                    <i class="fas fa-store" style="margin-right: 6px; color: #28a745;"></i> Ver tienda
                `;

                // Lo insertamos exactamente arriba de "Ver perfil"
                targetElement.parentNode.insertBefore(tiendaLink, targetElement);
                
            } else {
                // 4. Fallback: Si no se encuentra el elemento de anclaje, usamos la inserción al final del contenedor
                let userLinks = userTools.querySelector('.dropdown-contents') || 
                                userTools.querySelector('.dropdown-menu') || 
                                userTools.querySelector('.dropdown-content');
                
                if (!userLinks) userLinks = userTools;

                if (userLinks) {
                    const tiendaLi = document.createElement('div');
                    tiendaLi.id = 'enlace-retorno-tienda';
                    tiendaLi.style.borderTop = '1px solid #444';
                    tiendaLi.style.marginTop = '6px';
                    tiendaLi.style.paddingTop = '4px';
                    tiendaLi.innerHTML = `
                        <a href="/" style="color: #28a745; font-weight: bold; display: block; padding: 10px 15px; text-decoration: none; font-size: 13px;">
                            <i class="fas fa-store" style="margin-right: 6px;"></i> Ver tienda
                        </a>
                    `;
                    userLinks.appendChild(tiendaLi);
                }
            }
        }
    }

    // Ejecución inicial y retraso por carga asíncrona en dispositivos móviles
    agregarBotonRegresar();
    setTimeout(agregarBotonRegresar, 600);
});
