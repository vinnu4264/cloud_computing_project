FROM python:3.8

COPY ./requirements.txt /requirements.txt
COPY ./app.py /app.py

RUN pip3 install -r requirements.txt
EXPOSE 5000

WORKDIR /

ENTRYPOINT [ "python","app.py" ]
