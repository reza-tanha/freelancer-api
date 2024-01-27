FROM python:3.9-alpine

WORKDIR /app

COPY . /app


RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN apt update && apt install nodejs npm -y

# RUN npm install elasticdump -g

# ENTRYPOINT [ "python", "run.py"]