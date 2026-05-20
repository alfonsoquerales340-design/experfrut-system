#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instalar las dependencias del archivo requirements.txt
pip install -r requirements.txt

# 2. Recopilar los archivos estáticos
python manage.py collectstatic --no-input


