## Preprocessor Service

The Preprocessor service is used to **Pull data** from Producer, **Preprocess** the data and **Upload** the result to Data Warehouse.

### Language and Version

---
`Python 3.11`

### Project Structure

---
- [consumer](../preprocessor_service/consumer) : This folder contains the code to pull data from Producer.
- [preprocess](../preprocessor_service/preprocess) : This folder contains the code to preprocess the data.
- [producer](../preprocessor_service/producer) : This folder contains the code to upload the result to Data Warehouse.
- [Dockerfile](../preprocessor_service/Dockerfile) : This file contains the code to build the docker image.
- [main.py](../preprocessor_service/main.py) : This file contains the code to run the service.
- [pipeline.py](../preprocessor_service/pipeline.py) : This file contains the code to run the preprocessing pipeline.
- [requirements.txt](../preprocessor_service/requirements.txt) : This file contains the required libraries to run the service.

### Running the project

---
- Install dependencies:
  ```bash 
  pip install -r requirements.txt
  ```
- Run the project:
  ```bash
    python main.py
  ```
