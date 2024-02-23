FROM ubuntu:rolling

# Set the working directory
WORKDIR /codeapi

COPY core-packages.txt ./
RUN apt update && apt upgrade -y && xargs apt-get -y install < core-packages.txt

COPY apt-packages.txt ./
COPY python.txt ./
RUN xargs apt-get -y install < apt-packages.txt
RUN pip install --no-cache-dir -r python.txt --break-system-packages

COPY nodejs.txt ./
RUN npm install -g $(cat nodejs.txt)

WORKDIR /home/codeapi