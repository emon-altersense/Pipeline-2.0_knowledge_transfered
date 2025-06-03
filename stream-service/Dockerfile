FROM ubuntu:22.04

ARG OPENCV_VERSION=4.11.0
ARG LIBRDKAFKA_VERSION=v2.8.0


RUN apt update &&  \
    apt install -y git g++ cmake ninja-build build-essential  \
    libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-good  \
    librdkafka-dev libssl-dev

# OpenCV
RUN git clone --depth 1 --branch ${OPENCV_VERSION} https://github.com/opencv/opencv.git && \
    cd opencv && \
    git checkout ${OPENCV_VERSION} && \
    git submodule update --recursive --init && \
    mkdir build && cd build && \
    cmake -D CMAKE_BUILD_TYPE=MinSizeRel  \
        -D CMAKE_BUILD_PARALLEL_LEVEL=$(nproc)  \
        -D BUILD_LIST=core,highgui,videoio,imgproc \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D WITH_GSTREAMER=ON  \
        -G Ninja .. && ninja && ninja install

# LibRdKafka
RUN git clone --depth 1 --branch ${LIBRDKAFKA_VERSION} https://github.com/confluentinc/librdkafka.git && \
    cd librdkafka && \
    git checkout ${LIBRDKAFKA_VERSION} && \
    git submodule update --recursive --init && \
    mkdir build && cd build && \
    cmake -D CMAKE_BUILD_TYPE=MinSizeRel  \
    -D CMAKE_BUILD_PARALLEL_LEVEL=$(nproc)  \
    -D CMAKE_INSTALL_PREFIX=/usr/local  \
    -G Ninja .. && ninja && ninja install \

WORKDIR /app/
COPY / /app/

CMD ["bash", "run_stream_service.sh"]