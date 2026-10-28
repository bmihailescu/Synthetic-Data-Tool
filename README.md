# Synthetic Data Tool
This Synthetic Data tool allows the user to generate datasets filled with random test data of a specific format. This allows for realistic test data to be generated on mass, quickly. This may be particularly useful in Performance Testing and Database Testing.

## 1.1 Prerequisites
The below is required to run the tool locally:

1. Python 3
2. Docker (with docker compose)


## 1.2 Running Locally in Docker

In the command terminal:

1 - In the root directory, run this to build the container  `docker-compose build`

2 - Run docker compose to start up app in container  `docker-compose up`

3 - Once the app has finished building, you will see "Watching for file changes with StatReloader". Now you can open the application in a browser where URL = http://127.0.0.1:8000/


## 1.3 Running Locally without Docker

`pip install -r ./requirements.txt`

`cd SyntheticData/`

`python manage.py collectstatic`

`python manage.py runserver`

## 1.4 Stopping the application

To stop running the application, press Ctrl+C in the command prompt


## 1.5 Running in Production (Work in progress)

docker-compose -f docker-compose-deploy.yml up --build
