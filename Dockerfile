FROM python:2.7.14-jessie

WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt

ENV FLASK_APP=web/app.py
ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["flask", "run", "--with-threads", "--host=0.0.0.0"]
