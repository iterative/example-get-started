FROM mcr.microsoft.com/vscode/devcontainers/python

ENV DEBIAN_FRONTEND=noninteractive

# Install DVC
RUN cd /etc/apt/sources.list.d \
 && wget https://dvc.org/deb/dvc.list \
 && apt-get update \
 && apt-get install --yes dvc \
 && apt-get clean \
 && rm --recursive --force /var/lib/apt/lists/*

