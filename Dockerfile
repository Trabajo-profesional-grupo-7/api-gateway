FROM python:3.10-slim

WORKDIR /code
 
COPY ./requirements.txt /code/requirements.txt
 
RUN apt-get update

RUN apt-get install -y awscli

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./test /code/test

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8001"]
