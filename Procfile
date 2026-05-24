web: python manage.py createsuperuser --noinput --username $SUPERUSER_NAME --email alfonso@example.com || true && python manage.py migrate && gunicorn experfrut_project.wsgi --log-file -
