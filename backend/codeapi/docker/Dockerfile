FROM ubuntu:rolling

# Set the working directory
WORKDIR /codeapi

COPY core-packages.txt ./
RUN apt update && apt upgrade -y && xargs apt-get -y install < core-packages.txt

COPY requirements.txt ./
COPY apt-packages.txt ./
RUN xargs apt-get -y install < apt-packages.txt
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

WORKDIR /home

COPY . .