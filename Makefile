DOCKER_CMD := docker
IMG_NAME := remote-cmder
CONTAINER_NAME := remote-cmder
CURRENT_PATH := $(PWD)
PROJECT_PATH := $(CURRENT_PATH)/../

all: build run

build:
	$(DOCKER_CMD) build -t $(IMG_NAME) -f docker/Dockerfile .

run:
	$(DOCKER_CMD) run --name $(CONTAINER_NAME) -it -p 8888:8888 $(IMG_NAME) python3 main.py

attach:
	$(DOCKER_CMD) exec -it $(CONTAINER_NAME) /bin/bash

start:
	$(DOCKER_CMD) start $(CONTAINER_NAME)

stop:
	$(DOCKER_CMD) stop $(CONTAINER_NAME)

.PHONY: clean

clean: stop clear

clear:
	$(DOCKER_CMD) rm $(CONTAINER_NAME)
	$(DOCKER_CMD) rmi $(IMG_NAME)
