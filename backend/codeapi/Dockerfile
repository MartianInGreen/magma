FROM python:3.12

# Set the working directory
WORKDIR /codeapi

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update && apt upgrade -y && xargs apt -y install < apt-packages.txt

COPY . .