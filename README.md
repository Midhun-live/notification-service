# Notification Service

## Overview

This project implements a scalable backend Notification Service capable of delivering messages across multiple channels such as Email, SMS, and Push. The system is designed with asynchronous processing, prioritization, and reliability in mind.

It supports high throughput using a queue-based architecture and ensures delivery guarantees through retries and tracking.

---

## Tech Stack

* **Backend**: FastAPI
* **Language**: Python
* **Database**: PostgreSQL
* **Queue**: Redis
* **ORM**: SQLAlchemy
* **Containerization**: Docker, docker-compose

### Rationale

* **FastAPI** provides high performance and built-in API documentation
* **PostgreSQL** ensures reliable and structured data storage
* **Redis** enables lightweight and fast queue processing
* **SQLAlchemy** offers clean database abstraction

---

## Features

### Core Features

* Multi-channel notifications (Email, SMS, Push)
* User preference enforcement per channel
* Priority-based processing (critical, high, normal, low)
* Delivery tracking (pending, sent, delivered, failed)
* Retry mechanism with exponential backoff
* Idempotency support
* Rate limiting per user

### Additional Features

* Batch notification API
* Webhook support for delivery updates
* Channel handler abstraction
* Template-based messaging

---

## System Flow

API → Database → Redis Queue → Worker → Channel Handlers → Status Update → Webhook

---

## API Endpoints

### Notifications

* `POST /notifications`
* `GET /notifications/{id}`
* `POST /notifications/batch`

### User

* `GET /users/{userId}/notifications`
* `POST /users/{userId}/preferences`
* `GET /users/{userId}/preferences`

### Webhooks

* `POST /webhooks`

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository_url>
cd notification-service
```

---

### 2. Start dependencies

```bash
docker-compose up -d
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the API server

```bash
uvicorn app.main:app --reload
```

---

### 5. Run the worker

```bash
python -m app.workers.notification_worker
```

---

## API Documentation

Interactive API documentation is available at:

http://localhost:8000/docs

---

## Assumptions

* Authentication is not included
* User data is managed externally; only user_id is stored
* External providers (Email, SMS, Push) are simulated
* Templates are stored in-memory

---

## Future Improvements

* Analytics API for reporting
* Circuit breaker for external integrations
* Persistent template storage
* Horizontal scaling with multiple workers
* Structured logging and monitoring
