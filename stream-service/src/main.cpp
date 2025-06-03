#include "camera/camera.cpp"
#include "camera/camera_builder.hpp"
#include "producer/kafka_producer.cpp"

using system_clock = std::chrono::system_clock;
using seconds = std::chrono::seconds;


int main() {

    std::vector<std::shared_ptr<Camera>> cameras;

    auto start_time = system_clock::now() + seconds(1);
    auto end_time = system_clock::now() + seconds(30+2+1);

    for (int i = 1; i <=6; ++i) {

        std::string rtsp_link = "rtsp://admin:altrsns007@119.148.31.44:554/Streaming/channels/" + std::to_string(i) + "02";
        auto camera = std::make_shared<Camera>(CameraBuilder()
            .set_rtsp_link(rtsp_link)
            .set_frame_rate(5)
            .set_resolution(1280, 720)
            .set_start_time(start_time)
            .set_end_time(end_time)
            .build());

        camera->start_camera();
        cameras.push_back(camera);
    }

    return 0;
}
