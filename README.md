# Helios Pipeline 2.0

---

### Services

- [Model Service](./model_service/README.md)
- [Preprocessor Service](./preprocessor_service/README.md)
- [Stream Service](./stream-service/README.md)

### Deployment

---
#### Prerequisites
* [Docker](https://docs.docker.com/engine/install/)
* [Docker Compose](https://docs.docker.com/compose/install/linux/)
* [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

#### Running the services
To start the associated services, run the following command:
```bash
docker compose up -d
```

#### Stopping the services
To stop the associated services, run the following command:
```bash
docker compose down
```

### Service Flow

1. Stream Service: The Stream service is used to Pull data from Producer, Preprocess the data and Upload the result to Data Warehouse.
2. Preprocessor Service: The Preprocessor service is used to Pull data from Producer, Preprocess the data and Upload the result to Data Warehouse.
3. Model Service: The Model service is used to Pull data from Data WareHouse, run Inference and Upload the result to cloud.

#### Realtime
```
Stream Service -> [Apache Kafka] -> Preprocessor Service -> [Data Warehouse]
```
#### Scheduled
```
[Data Warehouse] -> Model Service -> [Apache Kafka] -> Data Engineering -> [MongoDB Atlas]
```
