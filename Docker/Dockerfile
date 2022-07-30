FROM fnndsc/ubuntu-python3

RUN apt-get update -y
COPY ./requirements.txt /requirements.txt
COPY ./Config_files /Config_files

RUN pip3 install -r /requirements.txt