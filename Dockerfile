FROM python:3.10-slim-buster

WORKDIR /app

ARG MIGRATION_DB_URL

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=SayaMauDatang.settings \
    PORT=8000 \
    WEB_CONCURRENCY=2

# Install system packages required Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
&& rm -rf /var/lib/apt/lists/*

RUN addgroup --system django \
    && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy project code
COPY . .

# RUN python manage.py --noinput --clear
# RUN python manage.py migrate

# Run as non-root user
RUN chown -R django:django /app
USER django

# Run application
# CMD gunicorn project_name.wsgi:application
CMD ["gunicorn", "SayaMauDatang.wsgi"]