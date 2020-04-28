FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
ENV VIRTUAL_HOST students.app.tomchris.net
