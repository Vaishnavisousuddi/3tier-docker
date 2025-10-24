# Backend
cd ~/3tier-docker-rds/backend
docker build -t backend-app .
docker run -d \
  --name backend-app \
  -p 5000:5000 \
  -e DB_HOST=mydb-instance.cbig0owqa8c2.ap-south-1.rds.amazonaws.com \
  -e DB_USER=admin \
  -e DB_PASS=Admin123! \
  -e DB_NAME=mydatabase \
  backend-app

# Frontend
cd ~/3tier-docker-rds/frontend
docker build -t frontend-app .
docker run -d -p 80:80 --name frontend-app frontend-app

# Check running containers
docker ps
docker logs backend-app
-----------------------------------------------------------
Project Overview

This project demonstrates a 3-tier application architecture deployed manually using Docker and Amazon RDS.

Frontend: Static HTML page served via Nginx Docker container

Backend: Python Flask application connecting to MySQL RDS

Database: Amazon RDS MySQL instance storing/retrieving data

Goal: Deploy a fully functional 3-tier application on an EC2 instance using Docker and RDS.

Architecture Diagram

Diagram illustrating:

Frontend container → Backend container → RDS

Ports and networking

[Frontend Container (Nginx)] ---> [Backend Container (Flask)] ---> [RDS MySQL]
Port 80                         Port 5000                       Port 3306

Step 1: EC2 Setup

Launch Ubuntu EC2 instance.

Update packages:

sudo apt update && sudo apt upgrade -y


Install Docker:

sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker


(Optional) Add user to Docker group:

sudo usermod -aG docker $USER
newgrp docker

Step 2: Project Structure
3tier-docker-rds/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── frontend/
    ├── index.html
    └── Dockerfile

Step 3: Backend Setup

backend/app.py

Connects to RDS using environment variables

Executes SELECT NOW() to fetch current database time

Returns the result as JSON

backend/requirements.txt

flask
mysql-connector-python
flask-cors


backend/Dockerfile

FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]

Step 4: Frontend Setup


Displays a static message: “Hello from Frontend!”

Fetches backend API response via JavaScript

frontend/Dockerfile


FROM nginx:alpine
COPY . /usr/share/nginx/html
EXPOSE 80

Step 5: Amazon RDS Setup

Engine: MySQL 8.0


Instance identifier: mydb-instance

Master username: admin

Public access: Yes

Security group: Allow inbound on port 3306 from EC2

Test RDS connection from EC2:


mysql -h mydb-instance.cbig0owqa8c2.ap-south-1.rds.amazonaws.com -u admin -p


At this stage, no tables were created manually — SELECT NOW(); returns the current timestamp only.

Step 6: Build Docker Images

# Backend
cd ~/3tier-docker-rds/backend
docker build -t backend-app .


# Frontend
cd ../frontend
docker build -t frontend-app .

Step 7: Run Docker Containers
# Backend

docker run -d \
  --name backend-app \
  -p 5000:5000 \
  -e DB_HOST=mydb-instance.cbig0owqa8c2.ap-south-1.rds.amazonaws.com \
  -e DB_USER=admin \
  -e DB_PASS=Admin123! \
  -e DB_NAME=mydatabase \
  backend-app


# Frontend
docker run -d -p 80:80 --name frontend-app frontend-app


Verify containers:

docker ps
docker logs backend-app

Step 8: Test the Application

Backend: http://<EC2_PUBLIC_IP>:5000/ → returns JSON like:

{"message":"Connected to RDS! Current time: 2025-10-24 11:34:49"}


Frontend: http://<EC2_PUBLIC_IP> → shows:


Hello from Frontend!
API response from backend: {"message":"Connected to RDS! Current time: 2025-10-24 11:34:49"}

