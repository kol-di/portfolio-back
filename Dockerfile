FROM python:3.8

RUN mkdir -p usr/src/app
WORKDIR usr/src/app

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./BUL ./BUL/
COPY ./services ./services/
COPY ./manage.py entrypoint.sh ./

EXPOSE 8000

RUN apt-get update && apt-get install -y

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ./entrypoint.sh