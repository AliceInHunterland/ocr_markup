FROM python:3.6.5-stretch
MAINTAINER Sandeep Srinivasa "sss@lambdacurry.com"
ENV DEBIAN_FRONTEND noninteractive


RUN pip install Cython
RUN pip install Pillow
RUN apt-get update && apt-get install -y \
    autoconf automake libtool \
    rsync \
    libpng-dev \
    libjpeg-dev \
    libtiff-dev \
    zlib1g-dev tesseract-ocr  libtesseract-dev libleptonica-dev libcairo2-dev


RUN wget https://github.com/tesseract-ocr/tessdata/archive/4.00.tar.gz -O /tmp/tessdata.tgz 
RUN tar -xvf /tmp/tessdata.tgz --directory /tmp
WORKDIR /tmp
RUN  mkdir -p /usr/local/share/tessdata/ &&  rsync -a tessdata-4.00/ /usr/local/share/tessdata
WORKDIR /tmp/

RUN git clone --recursive https://github.com/sirfz/tesserocr

WORKDIR /tmp/tesserocr
RUN python setup.py bdist_wheel
RUN python setup.py install

RUN pip install --upgrade pip && pip install numpy Pillow opencv-python

RUN pip install fastapi uvicorn python-multipart

RUN mkdir /service
WORKDIR  /service

#RUN git clone --recursive https://github.com/OlegJakushkin/ocr_markup
#WORKDIR ./ocr_markup

CMD git clone --recursive https://github.com/OlegJakushkin/ocr_markup && cd ./ocr_markup && uvicorn app.app:app --host 0.0.0.0 --port 80
