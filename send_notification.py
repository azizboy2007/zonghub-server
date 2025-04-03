import os
import requests
import jwt
import time

# Get Firebase private key from environment variable
PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC5vWCOOM81larA\nEtCqmWZtOOAWh0WeDlgFjUNd5IYw9dqcVZGgiXxJPMTT9i7qbnZPZhjvTH0oR85r\nWQySRuiqh9k1QOf/MAxDQsOO1nNZ9ZEkwUtWInXbIQCPopOyGsaF+y3sn4lyTP4l\nWP9NmWfWsU5wT+ex20M3fyH4wjAbsJi7yqmZPuUmJg66Tr1mDEMzH7fXcJoRTLld\nPpAaJGg6PrwDb4hRAaty3uWfodYu0u76Q1gSRjuyUKIfdv2ozvKNrE5okH8t0DeC\n6nGN5OZHD04Cx0M8dxVJzqAEYDgiLVraZTYc4ihOw2yiWFQuu6l4DaHrSgxiBMDv\n35egQLqhAgMBAAECggEAHaAi/FGmXJh54DdVY2iiqY2BUfE96EHHG2JBRQLJaUTF\nm4WbJpKB/u0mQzKzSqmCIxRDVOPhMKFnahWNh5qvdgfDXEGf322f/xhxOGFki7bl\n8YldL/4WHfSrx2fki+txD8y/sfbDsGCvHBuPuSZcpXtUFLOXXqB886dKWV2hLmvc\n+R3IRDp/fpkEKwk+nvpqxuF8OglOGpOvibcSC7hj6qQGvImPQlKcb92lOQOwJ/ag\nkDZNKgBHpEdx6Tvn4lrZu/yk39HIrxlUwyx3v4FBHPzFi8xfrtn7Op82Rt0HSXWB\ndikSkO/f5/x4uJgheav+EzQ97dcuYc7Z0iNT7TOJSwKBgQDneMS4KkguJ8lCQU/T\nMlbXHHZ51w0U8NwmlL+VJRlNMGqExNpZDW36JD2me9LW6iU3u2Cy3CA1GrIu18ZC\nVQzAfP6nhpTPW/asDzLcD8Iffivpc3YbgcM+44KrLXs8B8aROmMzwsyUMp2Y/7Qy\nwubE+kZCRKyhOBBaba+dW3847wKBgQDNbASCW6JuMsFBSh+pnKC2rrKrFI0y6oJk\nKQ7j905jmRTluz0cU+k1xm8QZ5RGDrpZFsHkjEgqaGAQqGLcv/mXFkogjhJikXwx\nCL0Ew7mCvbDeZZRcXY3a9uibNSQ9P1FAG8rrzvYI8qf9tTVUxyPVrqQmP3awqcie\n/ckmX+ulbwKBgEML6TdLEANGhPZLArsy/pJqbSrXjrN9HNeUCHZD+7MvDfuNJY3b\n5Poqmyzo+uZDhipBfT3xouae5/PHjmbSSdJLoluWEO6LPcUS1fGGIv2KR1/kkNZg\n3NQPhF7e2q5Ftk+EsQ1iJG3cx2d00ZZOfBecQtOZHsPIAHyg/tg+k3hDAoGATtzR\nPlp/mV7S4oXacfs3l+qpnRRewNVXCazZkps29PWoGCox49YzCfoMWXfqbJrq35jl\nByDz85PujXaXvbfV0jM0chsY486Gpyx7pICfj5nTdQ36Txt7gjyYQD2+k+TjBIGm\n/bCOtBC0fao7tzhcgYRycFyc7GXCJ4e22YypovECgYEAv0PCUR4/r5l2lS7MWJOU\nPHnge6BlNEcgy3Qzj+E3bQQ96IqDpyG7ZRtdUi4T5QTK0eHdtBZW/FI5I+We8ojZ\n8z8pO+2m3HJTIyFHUfv0P9kpk6q2bT0vz7J/+/QPXJTYxteQPnL3X7QXWLGm86se\nPVlE9IQ1po59JOVcVejhgWA=
-----END PRIVATE KEY-----"""
SERVICE_ACCOUNT_EMAIL = "firebase-adminsdk-rl7mn@zonghub-gfx.iam.gserviceaccount.com"
TOKEN_URI = "https://oauth2.googleapis.com/token"

# Generate an OAuth token manually
def get_access_token():
    now = int(time.time())
    payload = {
        "iss": SERVICE_ACCOUNT_EMAIL,
        "scope": "https://www.googleapis.com/auth/firebase.messaging",
        "aud": TOKEN_URI,
        "exp": now + 3600,  # Token valid for 1 hour
        "iat": now
    }
    headers = {"alg": "RS256", "typ": "JWT"}
    assertion = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256", headers=headers)
    response = requests.post(TOKEN_URI, data={"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": assertion})
    return response.json().get("access_token")

# Send notification
def send_fcm_notification(title, body, token):
    url = "https://fcm.googleapis.com/v1/projects/zonghub-gfx/messages:send"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Example usage
DEVICE_TOKEN = "update-notification"
response = send_fcm_notification("Update!", "New skin available.", DEVICE_TOKEN)
print(response)
