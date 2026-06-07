document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password-field');
    
    if (passwordInput) {
        // Creación del contenedor y el botón del ojo
        const wrapper = document.createElement('div');
        wrapper.style.position = 'relative';
        wrapper.style.display = 'inline-block';
        wrapper.style.width = '100%';
        
        // Clonamos estilos y metemos el input en el wrapper
        passwordInput.parentNode.insertBefore(wrapper, passwordInput);
        wrapper.appendChild(passwordInput);
        
        // Crear el botón del ojo (usando FontAwesome que ya lo tienes cargado)
        const toggleBtn = document.createElement('span');
        toggleBtn.innerHTML = '<i class="fas fa-eye text-muted"></i>';
        toggleBtn.style.position = 'absolute';
        toggleBtn.style.right = '10px';
        toggleBtn.style.top = '50%';
        toggleBtn.style.transform = 'translateY(-50%)';
        toggleBtn.style.cursor = 'pointer';
        toggleBtn.style.zIndex = '10';
        
        wrapper.appendChild(toggleBtn);
        
        // Evento para alternar entre ver y ocultar
        toggleBtn.addEventListener('click', function() {
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                toggleBtn.innerHTML = '<i class="fas fa-eye-slash text-muted"></i>';
            } else {
                passwordInput.type = 'password';
                toggleBtn.innerHTML = '<i class="fas fa-eye text-muted"></i>';
            }
        });
    }
});
