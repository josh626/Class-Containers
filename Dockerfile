FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 80
EXPOSE 443
WORKDIR /app
