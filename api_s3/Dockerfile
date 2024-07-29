FROM python:3.10-slim

WORKDIR /src

COPY . .
#
# RUN apt update && apt install -y libsm6 libxext6 libglib2.0-0
# RUN apt-get install -y libxrender-dev
# RUN apt-get install -y libgl1-mesa-glx

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY src /src

ARG S3_API_HOST
ARG S3_API_PORT
ENV S3_API_HOST=${S3_API_HOST}
ENV S3_API_PORT=${S3_API_PORT}

CMD ["sh", "-c", "poetry run uvicorn main:app --host ${S3_API_HOST} --port ${S3_API_PORT} --reload"]