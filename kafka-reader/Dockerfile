FROM python:3.8

WORKDIR /code

# System deps:
RUN pip install poetry==1.4.0
COPY pyproject.toml poetry.lock* ./

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-root

COPY ./kafka_reader /code/app

CMD ["python", "-u", "app/main.py"]