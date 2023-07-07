#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
poetry add 'whitenoise[brotli]'
pip install --upgrade Pillow

rm poetry.lock
poetry lock
poetry install

python manage.py collectstatic --no-input
python manage.py migrate

pip install --force-reinstall -U setuptools

