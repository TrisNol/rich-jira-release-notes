FROM mcr.microsoft.com/vscode/devcontainers/base:trixie

RUN apt-get update && apt-get install -y curl git && apt-get clean

RUN apt-get update && apt-get install -y python-is-python3 && apt-get clean
# Install Poetry
ENV POETRY_HOME=/opt/poetry
RUN mkdir -p "$POETRY_HOME" \
 && curl -sSL https://install.python-poetry.org | POETRY_HOME="$POETRY_HOME" python3 - \
 && ln -sf "$POETRY_HOME/bin/poetry" /usr/local/bin/poetry
ENV PATH="$POETRY_HOME/bin:/root/.local/bin:/home/vscode/.local/bin:${PATH}"

# Install Node
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install -y nodejs && apt-get clean
