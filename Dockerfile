FROM ubuntu:16.04

RUN apt -y update
RUN apt -y upgrade
RUN apt-get install -y git
RUN apt install -y libopencv-dev python-opencv
RUN apt install -y python3-pip python3-dev
RUN python3 --version
RUN apt-get install -y python3-venv
RUN ls
RUN git clone https://github.com/Shirataki2/flask-mnist.git
WORKDIR flask-mnist
RUN python3 -m venv env
RUN ls
RUN . env/bin/activate
RUN pip3 install -r requirements.txt
EXPOSE 40000
CMD python3 server.py
