#ifndef STREAM_SERVICE_CAMERA_H
#define STREAM_SERVICE_CAMERA_H

#include <chrono>
#include <memory>
#include <thread>
#include <opencv2/opencv.hpp>
#include "producer/kafka_producer.h"


using time_point = std::chrono::time_point<std::chrono::system_clock>;

class CameraBuilder;

class Camera {
private:
    std::string rtsp_link;
    int frame_rate;
    int resolution_width;
    int resolution_height;

    cv::VideoCapture cap;
    cv::Mat frame;
    std::shared_ptr<std::thread> camera_thread;

    time_point start_time;
    time_point end_time;

    void create_camera_instance();
    void process_camera_stream();
    bool is_it_end_time() const;

public:
    Camera(
        std::string rtsp_link, int frame_rate, int resolution_width, int resolution_height,
        time_point start_time, time_point end_time
    );

    ~Camera();

    void start_camera();
    void stop_camera();
    void run_camera();
    void restart_camera();

    friend class CameraBuilder; // Allow CameraBuilder to access private members
};


#endif //STREAM_SERVICE_CAMERA_H
