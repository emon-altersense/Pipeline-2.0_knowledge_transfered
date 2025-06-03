## Model Service

The Model service is used to **Pull data** from Data WareHouse, run **Inference** and **Upload** the result to cloud.

### Language and Version

---
`Python 3.11`

### Project Structure

---
- [consumer](../model_service/consumer) : This folder contains the code to pull data from Data WareHouse.
- [inference](../model_service/inference) : This folder contains the code to run inference on the data.
- [postprocess](../model_service/postprocess) : This folder contains the code to apply postprocessing with business logic.
- [producer](../model_service/producer) : This folder contains the code to upload the result to cloud.
- [Dockerfile](../model_service/Dockerfile) : This file contains the code to build the docker image.
- [main.py](../model_service/main.py) : This file contains the code to run the service.
- [requirements.txt](../model_service/requirements.txt) : This file contains the required libraries to run the service.

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

### Note
This service is not fully completed due to unavailability of required device.
