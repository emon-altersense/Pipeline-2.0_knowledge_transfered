cmake_minimum_required(VERSION 3.22)

# <-- Project Definition -->
project(
        stream-service
        VERSION 0.1.0
        LANGUAGES CXX
)

# <-- C++ 17 -->
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O0")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O0")

# <-- Project Definition -->
include_directories(include)

add_executable(${CMAKE_PROJECT_NAME} src/main.cpp)

# <-- OpenCV -->
find_package(OpenCV REQUIRED)

# <-- librdKafka -->
find_package(RdKafka REQUIRED)

# <-- boost/beast -->

target_link_libraries(${CMAKE_PROJECT_NAME} ${OpenCV_LIBS} RdKafka::rdkafka++)
