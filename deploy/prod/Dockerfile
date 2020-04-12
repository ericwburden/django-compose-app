FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# create directory for the app user
RUN mkdir -p /home/app
RUN mkdir -p /home/app/staticfiles

# create the app user
RUN useradd -u 1234 -ms /bin/bash app

# create the appropriate directories
ENV APP_HOME=/home/app
WORKDIR $APP_HOME

#Install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    netcat 

RUN pip install --upgrade pip
COPY requirements.txt $APP_HOME
RUN pip install -r requirements.txt

COPY /app $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

ENTRYPOINT [ "/home/app/entrypoint.sh" ]
