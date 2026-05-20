#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instalar las dependencias del archivo requirements.txt
pip install -r requirements.txt

# 2. Recopilar los archivos estáticos
python manage.py collectstatic --no-input

# 3. Aplicar las migraciones de la base de datos
python manage.py migrate
