#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instalar las dependencias
pip install -r requirements.txt

# 2. Recopilar los archivos estáticos
python manage.py collectstatic --no-input

# 3. Crear el superusuario automáticamente si no existe
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'tu_correo@gmail.com', 'Experfrut2026')"


