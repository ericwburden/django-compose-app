FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    netcat 

RUN mkdir /code
WORKDIR /code

RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY /app /code/

ENTRYPOINT [ "/code/entrypoint.sh" ]
