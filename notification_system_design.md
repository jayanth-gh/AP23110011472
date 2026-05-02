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
