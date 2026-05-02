# Stage 1 - Notification System Design

## API Endpoints

GET /api/notifications
GET /api/notifications/unread
POST /api/notifications
PUT /api/notifications/{id}/read
DELETE /api/notifications/{id}

---

## Request (POST /api/notifications)

```json
{
  "title": "Placement Drive",
  "message": "TCS hiring tomorrow",
  "type": "placement",
  "userId": "123"
}
```

## Response

```json
{
  "id": "n101",
  "title": "Placement Drive",
  "message": "TCS hiring tomorrow",
  "type": "placement",
  "isRead": false,
  "createdAt": "2026-05-02T10:00:00Z"
}
```

---

## Headers

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJzaXZhc2FpamF5YW50aF9pbGx1cnVAc3JtYXAuZWR1LmluIiwiZXhwIjoxNzc3NzAyNDMxLCJpYXQiOjE3Nzc3MDE1MzEsImlzcyI6IkFmZm9yZCBNZWRpY2FsIFRlY2hub2xvZ2llcyBQcml2YXRlIExpbWl0ZWQiLCJqdGkiOiJiYmMwZDdmOS1mM2UwLTQ2YTMtYTlhZC1mMGZkNzBiOWIxMDkiLCJsb2NhbGUiOiJlbi1JTiIsIm5hbWUiOiJpbGx1cnUgc2l2YSBzYWkgamF5YW50aCIsInN1YiI6IjE0YzVmYThlLTQ2OTgtNDQ1Zi05Y2Y5LTQ5MmU0YWJjNjk3NCJ9LCJlbWFpbCI6InNpdmFzYWlqYXlhbnRoX2lsbHVydUBzcm1hcC5lZHUuaW4iLCJuYW1lIjoiaWxsdXJ1IHNpdmEgc2FpIGpheWFudGgiLCJyb2xsTm8iOiJhcDIzMTEwMDExNDcyIiwiYWNjZXNzQ29kZSI6IlFrYnB4SCIsImNsaWVudElEIjoiMTRjNWZhOGUtNDY5OC00NDVmLTljZjktNDkyZTRhYmM2OTc0IiwiY2xpZW50U2VjcmV0IjoiVFZQR1VFR1VIZ1JBeWJWTSJ9._0NBv9dRHYj5nKEKmowH3Z4gYr_rE9oodQHNKXIP0hs 
Content-Type: application/json

---

## JSON Schema

```json
{
  "id": "string",
  "title": "string",
  "message": "string",
  "type": "string",
  "isRead": "boolean",
  "createdAt": "datetime"
}
```


## Stage 2

### Database Choice

PostgreSQL (relational database)

---

### Table Schema

```sql
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    userId INT,
    title TEXT,
    message TEXT,
    type VARCHAR(20),
    isRead BOOLEAN DEFAULT FALSE,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Problems with Large Data

* Slow queries
* High latency due to full table scans

---

### Solutions

* Add indexes on userId, isRead, createdAt
* Use pagination (LIMIT, OFFSET)
* Table partitioning for large datasets

---

### Queries

```sql
-- Get all notifications
SELECT * FROM notifications WHERE userId = 123;

-- Get unread notifications
SELECT * FROM notifications 
WHERE userId = 123 AND isRead = FALSE 
ORDER BY createdAt DESC;

-- Mark notification as read
UPDATE notifications 
SET isRead = TRUE 
WHERE id = 101;
```

## Stage 3

### Given Query

```sql
SELECT * FROM notifications
WHERE studentID = 1042 AND isRead = false
ORDER BY createdAt DESC;
```

---

### Is it correct?

Yes, it correctly fetches unread notifications for a student.

---

### Why is it slow?

* No index on studentID, isRead, createdAt
* Causes full table scan

---

### Optimization (Index)

```sql
CREATE INDEX idx_notifications 
ON notifications(studentID, isRead, createdAt DESC);
```

---

### Computation Cost

* Without index: O(n)
* With index: O(log n)

---

### Should we index every column?

No:

* Increases storage
* Slows insert/update operations
* Only index frequently queried columns

---

### Query (Placement notifications in last 7 days)

```sql
SELECT DISTINCT userId
FROM notifications
WHERE type = 'Placement'
AND createdAt >= NOW() - INTERVAL '7 days';
```

## Stage 4

### Problem

Fetching notifications on every page load causes high database load and slow response time.

---

### Solutions

* **Caching (Redis)**
  Store frequently accessed notifications in cache to reduce database queries.

* **Pagination**
  Fetch limited records using LIMIT and OFFSET instead of all data.

* **Lazy Loading**
  Load notifications only when the user opens the notifications section.

* **Real-time Updates**
  Use WebSockets or SSE to push new notifications instead of polling.

---

### Trade-offs

* Caching → Faster reads, but possible stale data
* Pagination → Reduces load, but shows partial data
* Real-time → Efficient, but increases system complexity


## Stage 5

### Issues in Current Implementation

* Sequential processing → slow for large users (50,000)
* No retry mechanism for failed emails
* Email failure causes inconsistency
* Tight coupling of DB and email operations

---

### Improved Approach

* Use asynchronous processing (queue system)
* Save to DB first (reliable)
* Send emails via background workers
* Add retry mechanism for failures

---

### Revised Pseudocode

```python
def notify_all(student_ids, message):
    for student_id in student_ids:
        save_to_db(student_id, message)     # store notification
        queue_email(student_id, message)    # async email sending
        push_to_app(student_id, message)    # real-time notification
```

---

### Failure Handling

* Track failed emails
* Retry using background workers

---

### DB and Email Together?

No:

* DB write should be immediate and reliable
* Email should be asynchronous and retryable


## Stage 6

### Approach

* Fetch notifications from API
* Assign priority: Placement > Result > Event
* Sort by priority and latest time
* Return top 10 notifications

---

### Code

import requests
from datetime import datetime

API_URL = "http://20.207.122.201/evaluation-service/notifications"

priority_map = {
    "Placement": 3,
    "Result": 2,
    "Event": 1
}

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJzaXZhc2FpamF5YW50aF9pbGx1cnVAc3JtYXAuZWR1LmluIiwiZXhwIjoxNzc3NzA0NDk5LCJpYXQiOjE3Nzc3MDM1OTksImlzcyI6IkFmZm9yZCBNZWRpY2FsIFRlY2hub2xvZ2llcyBQcml2YXRlIExpbWl0ZWQiLCJqdGkiOiI3NjZlYTMwYS1lMDcyLTRhYTgtOWFiMS0yNTc3Zjc2MjRjNmIiLCJsb2NhbGUiOiJlbi1JTiIsIm5hbWUiOiJpbGx1cnUgc2l2YSBzYWkgamF5YW50aCIsInN1YiI6IjE0YzVmYThlLTQ2OTgtNDQ1Zi05Y2Y5LTQ5MmU0YWJjNjk3NCJ9LCJlbWFpbCI6InNpdmFzYWlqYXlhbnRoX2lsbHVydUBzcm1hcC5lZHUuaW4iLCJuYW1lIjoiaWxsdXJ1IHNpdmEgc2FpIGpheWFudGgiLCJyb2xsTm8iOiJhcDIzMTEwMDExNDcyIiwiYWNjZXNzQ29kZSI6IlFrYnB4SCIsImNsaWVudElEIjoiMTRjNWZhOGUtNDY5OC00NDVmLTljZjktNDkyZTRhYmM2OTc0IiwiY2xpZW50U2VjcmV0IjoiVFZQR1VFR1VIZ1JBeWJWTSJ9.YzNgy6p33X-Gp1ujKD-DXWN33fvVy0bDRzfesbwLK8I"
}

response = requests.get(API_URL, headers=headers)
data = response.json()
print(data)
notifications = data["notifications"]

for n in notifications:
    n["priority"] = priority_map.get(n["Type"], 0)
    n["time"] = datetime.strptime(n["Timestamp"], "%Y-%m-%d %H:%M:%S")

notifications.sort(key=lambda x: (-x["priority"], -x["time"].timestamp()))

top_10 = notifications[:10]

for n in top_10:
    print(n)
---

### Output

![Output](Stage6_output.png)


git add .
git commit -m "Final submission"
git push