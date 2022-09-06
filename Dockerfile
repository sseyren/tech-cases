FROM python:3.9-alpine
WORKDIR /app/src
COPY . .
RUN pip install -r requirements.txt

ARG STATIC_ROOT=/app/static/
ARG MEDIA_ROOT=/app/media/

ENV DEBUG=0
ENV ALLOWED_HOSTS=*
ENV STATIC_URL=static/
ENV MEDIA_URL=media/
ENV DATABASE_URL=sqlite:///db.sqlite3
ENV SECRET_KEY="temporary-secret-key"

RUN python manage.py migrate
RUN python manage.py collectstatic

CMD ["gunicorn", "--bind", "0.0.0.0:80", "website.wsgi"]
EXPOSE 80
