FROM nvidia/cuda:10.2-devel-ubuntu18.04

ARG packages

ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:$LD_LIBRARY_PATH

RUN apt update
RUN apt install -y wget software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.8 python3-pip python3.8-dev

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.8 get-pip.py

COPY ./setup.py /functional-cat/setup.py
COPY ./pyproject.toml /functional-cat/pyproject.toml
COPY ./functional_cat /functional-cat/functional_cat

WORKDIR /functional-cat
RUN pip3.8 install ".${packages}"

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN alias pip=pip3.8
WORKDIR /

SHELL ["/bin/bash", "-c"]