#!/usr/bin/env bash
# exit on error
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --run-syncdb --fake-initial || true
python manage.py migrate notifications zero --fake
python manage.py migrate comments zero --fake
python manage.py migrate posts zero --fake
python manage.py migrate --fake-initial