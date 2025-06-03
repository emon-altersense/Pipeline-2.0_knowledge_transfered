#ifndef STREAM_SERVICE_CAMERA_BUILDER_H
#define STREAM_SERVICE_CAMERA_BUILDER_H

#include <string>
#include "camera.h"


using time_point = std::chrono::time_point<std::chrono::system_clock>;

class CameraBuilder {
private:
    std::string rtsp_link;
    int frame_rate = 1;
    int resolution_width = 1280;
    int resolution_height = 720;

    time_point start_time;
    time_point end_time;

public:
    CameraBuilder &set_rtsp_link(const std::string &link) {
        this->rtsp_link = link;
        return *this;
    }

    CameraBuilder &set_frame_rate(int rate) {
        this->frame_rate = rate;
        return *this;
    }

    CameraBuilder &set_resolution(int width, int height) {
        this->resolution_width = width;
        this->resolution_height = height;
        return *this;
    }

    CameraBuilder &set_start_time(const time_point &starttime) {
        this->start_time = starttime;
        return *this;
    }

    CameraBuilder &set_end_time(const time_point &endtime) {
        this->end_time = endtime;
        return *this;
    }

    // Method to build a Camera object
    Camera build() const {
        return {
            this->rtsp_link,
            this->frame_rate,
            this->resolution_width, this->resolution_height,
            this->start_time, this->end_time,
        };
    }
};


#endif //STREAM_SERVICE_CAMERA_BUILDER_H
