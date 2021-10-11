FROM python:3.8-slim

EXPOSE 8000
WORKDIR /app

ENV \
  #python
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONOPTIMIZE=1 \
  #poetry
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_VERSION=1.1.4

RUN apt-get update \
    && python -m pip install --upgrade pip \
    && pip install "poetry==$POETRY_VERSION"

COPY ./poetry.lock ./pyproject.toml ./.env /app/

RUN poetry install --no-dev

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

COPY ./app /app