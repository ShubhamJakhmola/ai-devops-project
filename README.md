# #################################### AI DevOps Project ########################################################

## Overview
This project demonstrates deployment and productionization of a containerized FastAPI backend application using Docker, Docker Compose, NGINX reverse proxy, PostgreSQL, Redis, GitHub Actions CI/CD, and AWS EC2 infrastructure.

The objective of this project is to showcase practical DevOps, infrastructure management, deployment automation, and production troubleshooting skills.

---

# Tech Stack

- FastAPI
- PostgreSQL
- Redis
- Docker
- Docker Compose
- NGINX
- GitHub Actions
- AWS EC2 (Ubuntu 24.04)

---

# Architecture

Client → NGINX → FastAPI → PostgreSQL  
                         └→ Redis

---

# Features

- Dockerized FastAPI application
- Multi-container orchestration using Docker Compose
- NGINX reverse proxy setup
- PostgreSQL database integration
- Redis integration
- Health check endpoint
- Environment variable configuration
- GitHub Actions CI/CD deployment pipeline
- AWS EC2 deployment
- fail2ban security setup
- Basic production logging
- Restart policies for containers

---