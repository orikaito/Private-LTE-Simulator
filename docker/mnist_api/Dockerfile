FROM python:3.10.5-slim-bullseye

WORKDIR /usr/src/app
ENV FLASK_APP=flask_api.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80

COPY /app/requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# RUN pip freeze > requirements_freeze.txt

CMD [ "flask", "run"]