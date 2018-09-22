echo "Running migrations..."
python manage.py migrate

echo "Starting Gunicorn..."
exec gunicorn -b 0.0.0.0:80 personal.wsgi:application
