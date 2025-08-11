FROM python:3.13.6-alpine3.22

RUN mkdir /app

WORKDIR /app

COPY ../  .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD uvicorn app.main:app --reload