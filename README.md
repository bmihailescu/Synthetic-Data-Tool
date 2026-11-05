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

## Saved manual schemas

On the home page, save a completed manual schema by entering a name and selecting **Save**. Saved schemas are stored in the current browser for this site, can be selected to preview their columns and load them back into the editor, and can be removed with **Delete**. They are not shared across browsers or app instances.

For manually generated data, City and Address values use an offline curated list of 45 UK city and postcode pairs. The postcodes were checked against the Postcodes.io postcode directory; the list is intentionally limited, and City and postcode values remain paired when generated on the same row. The street line remains synthetic and is not verified to be assigned within that postcode. Country always returns `United Kingdom`. Phone Number and Mobile Number use Ofcom's reserved UK fictional mobile range (`+44 7700 900xxx`), so generated numbers are UK mobile-formatted but not live subscriber numbers.

## 1.4 Stopping the application

To stop running the application, press Ctrl+C in the command prompt


## 1.5 Running in Production (Work in progress)

docker-compose -f docker-compose-deploy.yml up --build
