#ifndef STREAM_SERVICE_KAFKA_PRODUCER_H
#define STREAM_SERVICE_KAFKA_PRODUCER_H

#include <iostream>
#include <memory>
#include <mutex>
#include <librdkafka/rdkafkacpp.h>


class DeliveryReport final : public RdKafka::DeliveryReportCb {
public:
    void dr_cb(RdKafka::Message &message) override {
        if (message.err()) {
            std::cerr << "Message delivery failed: " << message.errstr() << std::endl;
        } else {
//            std::cerr << "Message delivered to topic " << message.topic_name()
//                      << " [" << message.partition() << "] at offset " << message.offset() << std::endl;
        }
    }
};


class KafkaProducer {
private:
    std::string error_str;
    std::mutex producerMutex;
    std::shared_ptr<RdKafka::Producer> producer = nullptr;
    DeliveryReport delivery_report;

    KafkaProducer();

public:
    static KafkaProducer &get_instance();
    ~KafkaProducer();
    void produce_message(const std::string &camera_key, const std::string &message);
    void flush() const;
};


#endif //STREAM_SERVICE_KAFKA_PRODUCER_H
