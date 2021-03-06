# MAPOINTS
--------
The API for building a map of the points and finding the best way.

## Tech
- Python ^3.7 
    - [FastAPI](https://fastapi.tiangolo.com/)
- Poetry 1.1.4 + Docker


## Setup development environment
First you need to create the .env file with data that contains in .env.example
```
DEBUG=True
```
And then you going to create you own .env file in **project root directory**:
```
echo "DEGUG=True" > .env
```

## Run application with poetry
```
git clone https://github.com/AlexandrChikur/mapoints.git
cd mapoints/
poetry install poetry shell
```
To run the web application in debug use:
```
uvicorn app.main:app --reload
```
