ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHON_VERSION=${PYTHON_VERSION}

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app/PythonProject

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock pyproject.toml .

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root

# Копирование в контейнер папок и файлов.
COPY . .

ENTRYPOINT ["python3"]
CMD ["./json_context_manager_decorator.py"]
# CMD ["./unit_tests/test_additional_functions.py"]