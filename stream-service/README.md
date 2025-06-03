## Stream Service

The Stream service is used to **Pull data** from Producer, **Preprocess** the data and **Upload** the result to Data Warehouse.

### Language and Version

---
- `C++ 17`
- `CMake 3.22`
## Libraries

---
- [OpenCV](https://github.com/opencv/opencv)
- [LibRdKafka](https://github.com/confluentinc/librdkafka)

### Project Structure

---
- [include](../stream-service/include) : Contains all the header files.
- [src](../stream-service/src) : Contains the source file.
- [CMakeLists.txt](../stream-service/CMakeLists.txt) : CMake configuration file.
- [Dockerfile](../stream-service/Dockerfile) : Docker configuration file.
- [run_stream_service.sh](../stream-service/run_stream_service.sh) : Script to run the stream service.

### Running the project

---
- Install dependencies:
  ```bash
  export OPENCV_VERSION=4.11.0 LIBRDKAFKA_VERSION=v2.8.0
  ```
  ```bash 
  apt update &&  \
  apt install -y git g++ cmake ninja-build build-essential  \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-good  \
  librdkafka-dev libssl-dev
  ```
  ```bash
  git clone --depth 1 --branch ${OPENCV_VERSION} https://github.com/opencv/opencv.git && \
  cd opencv && \
  git checkout ${OPENCV_VERSION} && \
  git submodule update --recursive --init && \
  mkdir build && cd build && \
  cmake -D CMAKE_BUILD_TYPE=MinSizeRel  \
        -D CMAKE_BUILD_PARALLEL_LEVEL=$(nproc)  \
        -D BUILD_LIST=core,highgui,videoio,imgproc \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D WITH_GSTREAMER=ON  \
        -G Ninja .. && \
  ninja && \
  sudo ninja install
  ```  
  ```bash
  git clone --depth 1 --branch ${LIBRDKAFKA_VERSION} https://github.com/confluentinc/librdkafka.git && \
  cd librdkafka && \
  git checkout ${LIBRDKAFKA_VERSION} && \
  git submodule update --recursive --init && \
  mkdir build && cd build && \
  cmake -D CMAKE_BUILD_TYPE=MinSizeRel  \
        -D CMAKE_BUILD_PARALLEL_LEVEL=$(nproc)  \
        -D CMAKE_INSTALL_PREFIX=/usr/local  \
        -G Ninja .. && \
  ninja && \
  sudo ninja install
  ```

- Run the project:
  ```bash
  bash run_stream_service.sh
  ```
---
Alternatively
- Build the project:
  ```bash
  mkdir build && cd build
  cmake -G Ninja .. && ninja
  ```
- Run the project:
  ```bash
  ./stream-service
  ```
