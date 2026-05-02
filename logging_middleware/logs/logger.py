import requests

# Replace this with your actual access token from Auth API
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJzaXZhc2FpamF5YW50aF9pbGx1cnVAc3JtYXAuZWR1LmluIiwiZXhwIjoxNzc3NzA0NDk5LCJpYXQiOjE3Nzc3MDM1OTksImlzcyI6IkFmZm9yZCBNZWRpY2FsIFRlY2hub2xvZ2llcyBQcml2YXRlIExpbWl0ZWQiLCJqdGkiOiI3NjZlYTMwYS1lMDcyLTRhYTgtOWFiMS0yNTc3Zjc2MjRjNmIiLCJsb2NhbGUiOiJlbi1JTiIsIm5hbWUiOiJpbGx1cnUgc2l2YSBzYWkgamF5YW50aCIsInN1YiI6IjE0YzVmYThlLTQ2OTgtNDQ1Zi05Y2Y5LTQ5MmU0YWJjNjk3NCJ9LCJlbWFpbCI6InNpdmFzYWlqYXlhbnRoX2lsbHVydUBzcm1hcC5lZHUuaW4iLCJuYW1lIjoiaWxsdXJ1IHNpdmEgc2FpIGpheWFudGgiLCJyb2xsTm8iOiJhcDIzMTEwMDExNDcyIiwiYWNjZXNzQ29kZSI6IlFrYnB4SCIsImNsaWVudElEIjoiMTRjNWZhOGUtNDY5OC00NDVmLTljZjktNDkyZTRhYmM2OTc0IiwiY2xpZW50U2VjcmV0IjoiVFZQR1VFR1VIZ1JBeWJWTSJ9.YzNgy6p33X-Gp1ujKD-DXWN33fvVy0bDRzfesbwLK8I"

LOG_API_URL = "http://20.207.122.201/evaluation-service/logs"


def Log(stack, level, package, message):
    """
    Reusable logging middleware function

    Parameters:
    stack   -> backend / frontend
    level   -> debug / info / warn / error / fatal
    package -> handler / route / service / db / middleware etc.
    message -> actual log message
    """

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "stack": stack,
        "level": level,
        "package": package,
        "message": message
    }

    try:
        response = requests.post(
            LOG_API_URL,
            json=payload,
            headers=headers
        )

        print("Status Code:", response.status_code)
        print("Response:", response.text)

    except Exception as e:
        print("Logging failed:", str(e))


# Example usage
if __name__ == "__main__":
    Log(
        "backend",
        "error",
        "handler",
        "Received string, expected bool"
    )