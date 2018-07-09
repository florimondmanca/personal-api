echo "Running migrations..."
pipenv run python manage.py migrate

echo "Starting Gunicorn..."
exec pipenv run gunicorn -b 0.0.0.0:80 personal.wsgi:application
