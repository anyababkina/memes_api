FROM python:3.10-slim

WORKDIR /src

COPY . .

# RUN apt update && apt install -y libsm6 libxext6 libglib2.0-0
# RUN apt-get install -y libxrender-dev
# RUN apt-get install -y libgl1-mesa-glx

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY src /src

ARG API_MEMES_HOST
ARG API_MEMES_PORT
ENV API_MEMES_HOST=${API_MEMES_HOST}
ENV API_MEMES_PORT=${API_MEMES_PORT}

CMD ["sh", "-c", "alembic upgrade head && poetry run uvicorn main:app --host ${API_MEMES_HOST} --port ${API_MEMES_PORT} --reload"]