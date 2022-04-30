web: gunicorn --pythonpath backend backend.wsgi
release: python backend/manage.py makemigrations
release: python backend/manage.py migrate