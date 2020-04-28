FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./app /app
#ENV STATIC_PATH /app/static
#ENV STATIC_PATH /app/templates
WORKDIR /app
RUN pip install -r requirements.txt
