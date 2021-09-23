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
RUN mkdir /tmp/tesserocr

ADD setup.py README.rst tesseract.pxd tesserocr_experiment.pyx tesserocr.pyx tests/ tox.ini /tmp/tesserocr/

WORKDIR /tmp/tesserocr
RUN python setup.py bdist_wheel
RUN python setup.py install


RUN pip install numpy Pillow opencv-python

RUN pip install fastapi

COPY ./app.py /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
