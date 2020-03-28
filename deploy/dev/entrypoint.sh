#! /bin/sh

echo "Waiting for PostgreSQL..."

while ! nc -z $SQL_HOST $SQL_PORT; do
    echo "Waiting for PostgreSQL..."
    sleep 0.1
done

echo "PostgreSQL started"

if [ "$FLUSH_DB" ]; then
    echo "Flushing database..."
    python manage.py flush --no-input
fi

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"