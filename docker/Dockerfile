FROM ubuntu:18.04

RUN apt-get -y update && \
    apt-get -y install wget apt-utils xz-utils

COPY dist/blender-2.83.5-linux64.tar.xz /root

RUN cd /root && unxz blender-2.83.5-linux64.tar.xz && tar xvf blender-2.83.5-linux64.tar

RUN apt-get install -y libx11-dev  libxi-dev libxxf86vm-dev libxrender-dev libgl-dev