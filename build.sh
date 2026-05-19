#!/usr/bin/env bash
set -o errexit

# Instalar dependencias de Python
pip install -r requirements.txt

# Recopilar archivos estáticos (CSS, JS, iconos de la PWA)
python manage.py collectstatic --no-input

# Aplicar las migraciones a tu base de datos demo
python manage.py migrate