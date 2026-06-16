document.addEventListener('DOMContentLoaded', function() {
    function agregarBotonRegresar() {
        // Evitamos duplicaciones molestas si el script se ejecuta dos veces
        if (document.getElementById('enlace-retorno-tienda')) return;

        // 1. Buscamos el contenedor flotante o menú del usuario
        const userTools = document.getElementById('user-tools') || 
                          document.querySelector('.sticky-nav-user') || 
                          document.querySelector('#header') ||
                          document.body; // Capa de seguridad por si cambia la estructura del DOM

        if (userTools) {
            // 2. Buscamos exhaustivamente todos los elementos dentro del menú
            const items = userTools.querySelectorAll('a, div, span, p');
            let targetElement = null;

            // Intentamos localizar "Ver perfil" como punto de anclaje
            for (let item of items) {
                if (item.textContent.trim() === 'Ver perfil') {
                    targetElement = item;
                    break;
                }
            }

            // 3. Si encontramos "Ver perfil", inyectamos la Tienda con su mismo estilo
            if (targetElement) {
                const tiendaLink = document.createElement('a');
                tiendaLink.id = 'enlace-retorno-tienda';
                tiendaLink.href = '/'; // Tu ruta raíz o de la tienda
                
                // Conservamos las clases originales del admin para que el CSS nativo aplique (paddings, hover, fuentes)
                tiendaLink.className = targetElement.className;
                
                if (targetElement.getAttribute('style')) {
                    tiendaLink.setAttribute('style', targetElement.getAttribute('style'));
                }

                // Agregamos el texto e icono dinámicamente
                tiendaLink.innerHTML = `
                    <i class="fas fa-shopping-basket" style="margin-right: 6px; color: #28a745;"></i> Tienda
                `;

                // Lo insertamos exactamente arriba de "Ver perfil"
                targetElement.parentNode.insertBefore(tiendaLink, targetElement);
                
            } else {
                // 4. Fallback: Si por alguna razón "Ver perfil" no aparece, usamos tu lógica original al final de la lista
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
                            <i class="fas fa-shopping-basket" style="margin-right: 6px;"></i> Regresar a Tienda
                        </a>
                    `;
                    userLinks.appendChild(tiendaLi);
                }
            }
        }
    }

    // Se ejecuta al instante y lleva el temporizador por si la carga de red en móviles demora
    agregarBotonRegresar();
    setTimeout(agregarBotonRegresar, 600);
});
