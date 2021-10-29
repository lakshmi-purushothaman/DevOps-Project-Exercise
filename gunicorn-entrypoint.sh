# Running Gunicorn server with 2 workers
poetry run gunicorn --workers=2 --bind=0.0.0.0:5000 'todo_app.app:create_app()'