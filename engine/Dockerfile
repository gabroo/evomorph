FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y g++ cmake xsltproc libxml2-utils doxygen git zlib1g-dev libboost-dev libboost-program-options-dev libtiff5-dev libsbml5-dev gnuplot python3-pip python3-dev

RUN git clone https://gitlab.com/morpheus.lab/morpheus.git /opt/morpheus && \
    cd /opt/morpheus && \
    mkdir build && \
    cd build && \
    cmake -DMORPHEUS_GUI=OFF .. && \
    make -j`nproc` install

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "api.py"]
