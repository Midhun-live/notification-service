# Design Document

## Overview

This document describes the design of a scalable Notification Service that supports multi-channel delivery, asynchronous processing, and reliability through retries and prioritization.

The system is designed to handle high throughput while maintaining clean separation of concerns.

---

## Architecture

The service follows a layered architecture with asynchronous processing:

API Layer → Service Layer → Repository Layer → Database
↓
Redis Queue
↓
Worker
↓
Channel Handlers

### Components

* **API Layer**: Handles HTTP requests and validation
* **Service Layer**: Contains business logic
* **Repository Layer**: Handles database interactions
* **Worker**: Processes queued jobs asynchronously
* **Redis**: Acts as a message queue
* **PostgreSQL**: Persistent storage

---

## Database Design

### notifications

Stores all notification records.

Fields:

* id (UUID)
* user_id (string)
* message (text)
* channels (JSON)
* priority (critical/high/normal/low)
* status (pending/sent/delivered/failed)
* idempotency_key (optional)
* batch_id (optional)
* metadata (JSON)
* retry_count (int)
* max_retries (int)
* next_retry_at (timestamp)
* created_at
* updated_at

---

### user_preferences

Stores user channel preferences.

Fields:

* user_id (unique)
* email_enabled (boolean)
* sms_enabled (boolean)
* push_enabled (boolean)

---

### webhooks

Stores webhook configuration.

Fields:

* id
* user_id
* url

---

## Queue Design

Redis is used as a message queue.

Separate queues are maintained for each priority level:

* notification_queue:critical
* notification_queue:high
* notification_queue:normal
* notification_queue:low

The worker consumes jobs using priority order:

BRPOP critical → high → normal → low

This ensures higher priority notifications are processed first.

---

## Notification Flow

1. Client sends request to API
2. Notification is stored in database with status "pending"
3. Job is pushed to Redis queue based on priority
4. Worker consumes job from queue
5. Channels are filtered using user preferences
6. Notification is processed using channel handlers
7. Status is updated to "sent"
8. Delivery is simulated:

   * success → "delivered"
   * failure → retry or "failed"
9. Webhook is triggered for final status

---

## Retry Mechanism

Retries are applied for failed notifications.

* retry_count is incremented on failure

* Exponential backoff is used:

  delay = 2 ^ retry_count

* Maximum retries = 3

* After max retries, status is set to "failed"

Retries are re-enqueued into the queue.

---

## Rate Limiting

Rate limiting is implemented per user using Redis.

* Key format: rate_limit:{user_id}
* Limit: 100 requests per hour

If limit is exceeded:

* Notification is not created
* API returns rate limit response

---

## Idempotency

Idempotency is implemented using idempotency_key.

* Duplicate requests with same key return existing notification
* Prevents duplicate inserts and processing

---

## Batch Processing

Batch API allows sending notifications to multiple users.

* Each user is processed independently
* Separate notification records are created
* Partial success is supported
* Rate limiting and idempotency are applied per user

---

## Channel Handlers

Channel-specific logic is abstracted into handlers:

* EmailHandler
* SMSHandler
* PushHandler

This improves modularity and allows easy extension for new channels.

Each handler implements a send method and returns success/failure.

---

## Template System

Templates are used to generate dynamic messages.

* Stored in-memory for simplicity
* Variables are replaced at creation time
* Final message is stored in database

Example:
"Hello {{name}}" → "Hello John"

---

## Webhook Design

Webhooks allow external systems to receive status updates.

* Triggered on:

  * delivered
  * failed

* Sends HTTP POST request with notification details

Failures in webhook calls do not affect worker execution.

---

## Scalability

The system is designed to scale horizontally:

* Multiple workers can consume from Redis
* Redis supports high throughput
* Database can be scaled with indexing and replication

---

## Failure Handling

* Retry mechanism ensures delivery attempts
* Database failures handled via session management
* Worker continues processing even if individual jobs fail
* Webhook failures are logged but do not interrupt flow

---

## Trade-offs

* Redis used as queue instead of more durable systems (e.g., Kafka)
* Templates stored in-memory instead of database
* Single worker for simplicity (can be scaled)
* Simulated delivery instead of real integrations

These choices reduce complexity while demonstrating system design clearly.
