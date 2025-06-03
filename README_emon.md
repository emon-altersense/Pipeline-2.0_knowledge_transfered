# Helios Pipeline 2.0

## The whole Pipeline-2.0 flow
## Realtime
```
Stream Service -> [Apache Kafka] -> Preprocessor Service -> [Data Warehouse]
```
## Scheduled
```
[Data Warehouse] -> Model Service -> [Apache Kafka] -> Data Engineering -> [MongoDB Atlas]
```

The Apache kafka brings frames from camera and the Preprocessor service saves the data into a data lake from where the Model service can take the data as it wishes to run model related services. `The Model service here is mearly a dummmy version to show developer how to integrate the Pipeline-2.0 inside the whole system as it is the developer who will build the service as per the requirents. Also it is not fully implemented neither other modules  as well, as device was not provided but the Stream & Preprocess services are made as good as it can be with all those limitations`

## Prerequisites
* [Docker](https://docs.docker.com/engine/install/)
* [Docker Compose](https://docs.docker.com/compose/install/linux/)
* [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

## Running the services
To start the associated services, go to root directory `Pipeline-2.0` and run the following command:
```bash
docker compose up -d
```

## Stopping the services
To stop the associated services, go to root directory `Pipeline-2.0` and run the following command:
```bash
docker compose down
```

## Stream Service
Go to Stream service by `cd stream-service` and execute the main file by `python main.py`

then go to `http://localhost:32000/ui/clusters/local/all-topics/activity_detection` from the browser will show that kafka has bought frames in the form of messages. The `message count` column will increase with time showing kafka is working

## Preprocessor Service
Go to Preprocessor service by `cd preprocessor_service` and execute the main file by `python main.py`

Then go to mongo compass and connnect to localhost which will show it downloaded data and inside `frame` it has the frame data in binary format.

## Model Serice
Go to Model service by `cd Model_service` and execute the main file by `python main.py`

it will start to collect the data from the lake and execute the model prediction and store the results to forward it to mongo to cloud. but for now it is not forwarding to annywhere as there are no end point to send

## Video Screen Recording
see the video files inside `../screen_recordings` for executing all this step by step in video.

## Implemented and not implemented tasks at birds eye view

the `Proposed Data Pipeline 2.0.drawio.pdf` file contains all the tasks that are implemented in black colored font annd that are not implemented in red colored font situated at the second page.