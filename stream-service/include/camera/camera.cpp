#include "camera.h"

using system_clock = std::chrono::system_clock;
using time_point = std::chrono::time_point<system_clock>;
using milliseconds = std::chrono::milliseconds;


Camera::Camera(
    std::string rtsp_link, int frame_rate, int resolution_width, int resolution_height,
    time_point start_time, time_point end_time
) : rtsp_link(std::move(rtsp_link)), frame_rate(frame_rate), resolution_width(resolution_width),
    resolution_height(resolution_height), start_time(start_time), end_time(end_time) {}

Camera::~Camera() {
    // Ensure the camera thread is properly joined
    if (camera_thread && camera_thread->joinable()) camera_thread->join();
    this->stop_camera();
    // Flush the Kafka producer to ensure all messages are sent
    KafkaProducer::get_instance().flush();
}

void Camera::create_camera_instance() {
    const std::string pipeline =
        "gst-launch-1.0 rtspsrc location=" + this->rtsp_link +
        " ! queue ! rtph265depay ! h265parse ! avdec_h265 ! videorate ! video/x-raw,framerate=" +
        std::to_string(this->frame_rate) + "/1 ! videoscale ! video/x-raw,width=" +
        std::to_string(this->resolution_width) + ",height=" +
        std::to_string(this->resolution_height) + " ! videoconvert ! appsink";

    this->cap.open(pipeline, cv::CAP_GSTREAMER);
    if (!this->cap.isOpened()) {
        std::cerr << "Error opening video stream or file" << std::endl;
    }
}

void Camera::start_camera() {
    if (system_clock::now() < this->start_time) std::this_thread::sleep_until(this->start_time);
    this->camera_thread = std::make_shared<std::thread>(&Camera::run_camera, this);
}

void Camera::stop_camera() {
    if (this->cap.isOpened()) this->cap.release();
}

bool Camera::is_it_end_time() const {
    return system_clock::now() >= this->end_time;
}

void Camera::process_camera_stream() {
    KafkaProducer& producer = KafkaProducer::get_instance();
    std::vector<unsigned char> buffer;
    int count = 0;

    while (this->cap.read(this->frame)) {
        if (is_it_end_time()) {
            this->stop_camera();
            break;
        }
        cv::imencode(".jpg", frame, buffer);
        std::string message(buffer.begin(), buffer.end());
        producer.produce_message(this->rtsp_link.substr(this->rtsp_link.find_last_of('/') + 1), message);
        count++;
    }
    std::cerr << " Total data: " << count << " for " << this->rtsp_link.substr(this->rtsp_link.find_last_of('/') + 1) << std::endl;
}


void Camera::run_camera() {
    auto now = system_clock::now();
    auto remaining_time = std::chrono::duration_cast<milliseconds>(this->end_time - now);

    while (remaining_time.count() > 0) {
        if (!this->cap.isOpened()) this->create_camera_instance();

        this->process_camera_stream();

        // Avoid busy-waiting
        std::this_thread::sleep_for(
            milliseconds(remaining_time.count() > 1000 ? 250 : remaining_time.count())
        );
        remaining_time = std::chrono::duration_cast<milliseconds>(this->end_time - system_clock::now());
    }

    this->stop_camera();
}

void Camera::restart_camera() {
    this->stop_camera();
    this->start_camera();
}
