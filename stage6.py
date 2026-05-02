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