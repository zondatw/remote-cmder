FROM python:3.10 as requirements_creater
ENV PYTHONUNBUFFERED 1

# Create work directory
RUN mkdir /project
WORKDIR /project

# Copy poetry files
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

# Create requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry export -f requirements.txt --without-hashes --output requirements.txt

FROM ubuntu:22.04

# Create work directory
RUN mkdir /project
WORKDIR /project

# Install python3.10
RUN apt update && apt upgrade -y
RUN apt install -y python3.10 python3-pip libpython3.10-dev
RUN python3.10 -m pip install pip

# Copy requirements.txt from requirements_creater stage to work directory of current stage
COPY --from=requirements_creater /project/requirements.txt requirements.txt

# Install requirements
RUN python3.10 -m pip install -r requirements.txt

# Copy project files
COPY ./main.py main.py
COPY ./remote_cmder remote_cmder
