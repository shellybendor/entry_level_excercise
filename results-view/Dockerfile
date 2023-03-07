FROM python:3.8

WORKDIR /code

# System deps:
RUN pip install poetry==1.4.0
COPY pyproject.toml poetry.lock* ./

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-root

COPY ./results_view /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]