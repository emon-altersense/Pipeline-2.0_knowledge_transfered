#include "kafka_producer.h"


KafkaProducer::KafkaProducer() {
    std::shared_ptr<RdKafka::Conf> configuration(RdKafka::Conf::create(RdKafka::Conf::CONF_GLOBAL));

    if (configuration->set("dr_cb", &delivery_report, this->error_str) != RdKafka::Conf::CONF_OK) {
        std::cerr << this->error_str << std::endl;
        exit(169);
    }

    const std::unordered_map<std::string, std::string> config_map = {
        {"bootstrap.servers", "127.0.0.1:9094"},

        // Core Configuration
        {"batch.size",        "5242880"},
        {"batch.num.messages", "100"},
        {"linger.ms",         "1000"},
        {"compression.type",  "lz4"},
        {"message.max.bytes", "4194304"},
        {"enable.idempotence", "true"},
        {"max.in.flight",     "5"},
        {"acks", "all"},

        // Retry and Timeout
        {"retries", "5"},
        {"retry.backoff.ms", "100"},

        // Buffer and Networking
        {"queue.buffering.max.messages", "100000"},
        {"socket.send.buffer.bytes", "1048576"},
        {"socket.receive.buffer.bytes", "1048576"},
    };

    for (const auto & [config_key, config_value]: config_map) {
        if (configuration->set(config_key, config_value, this->error_str) != RdKafka::Conf::CONF_OK) {
            std::cerr << this->error_str << std::endl;
            exit(170);
        }
    }

    this->producer = std::shared_ptr<RdKafka::Producer>(RdKafka::Producer::create(configuration.get(), this->error_str));
    if (!this->producer) {
        std::cerr << "Failed to create producer: " << this->error_str << std::endl;
        exit(171);
    }
}

KafkaProducer::~KafkaProducer() {
    if (this->producer) {
        this->producer->flush(10 * 1000); // wait for max 10 seconds
    }
}

KafkaProducer& KafkaProducer::get_instance() {
    static std::unique_ptr<KafkaProducer> instance;
    static std::once_flag flag;

    std::call_once(flag, []() {
        instance.reset(new KafkaProducer());
    });

    return *instance;
}

void KafkaProducer::produce_message(const std::string &camera_key, const std::string &message) {
    std::unique_lock<std::mutex> lock(producerMutex, std::defer_lock);
    lock.lock();

    retry:
        RdKafka::ErrorCode resp = this->producer->produce(
            /* topic_name */
            "activity_detection",
            /* partition */
            RdKafka::Topic::PARTITION_UA,
            /* Copy the value of reference */
            RdKafka::Producer::RK_MSG_COPY,
            /* Value: Message in C-string format */
            const_cast<char *>(message.data()), message.size(),
            /* Key */
            camera_key.c_str(), camera_key.size(),
            /* Timestamp (defaults to current time) */
            0,
            /* Message headers, if any */
            nullptr,
            /* Per-message opaque value passed to delivery report */
            nullptr
        );

        if (resp != RdKafka::ERR_NO_ERROR) {
            if (resp == RdKafka::ERR__QUEUE_FULL) {
                this->producer->poll(10 * 1000); // block for max 1000ms
                goto retry;
            } else {
                std::cerr << "Failed to produce to " << camera_key << ": " << RdKafka::err2str(resp) << std::endl;
            }
        }
        this->producer->poll(0);
}

void KafkaProducer::flush() const {
    if (producer) {
        producer->flush(10 * 1000); // Wait for max 10 seconds to flush all messages
    }
}
