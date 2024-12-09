FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-22.04

RUN apt-get update && apt-get install -y curl git && apt-get clean

# Install Docker
RUN curl -fsSL https://get.docker.com | sh -

# Install Python 3.12
RUN apt-get update && apt-get -y install software-properties-common && apt-get clean
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get -y install python3-launchpadlib python3-pip && apt-get clean
RUN apt-get update && apt-get -y install python3.12 python3.12-dev python3.12-venv python-is-python3 && apt-get clean
RUN export PATH="$HOME/.local/bin:$PATH"
RUN pip install poetry
