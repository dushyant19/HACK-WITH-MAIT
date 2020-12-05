release: python manage.py migrate
web: daphne hack72.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker --settings=hack72.settings -v2
