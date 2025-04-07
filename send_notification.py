import os
import requests
import jwt
import time

# Get Firebase private key from environment variable
PRIVATE_KEY = os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n")
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
def send_fcm_notification(title, body, token, action_data=None):
    url = "https://fcm.googleapis.com/v1/projects/zonghub-gfx/messages:send"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": {
            "topic": token,
            "notification": {
                "title": title,
                "body": body
            },
	    "data": {
                "action": action_data
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Example usage
DEVICE_TOKEN = "news"
action_data = "update_data"
response = send_fcm_notification("Update!", "New skin available.", DEVICE_TOKEN, action_data) 
print(response)
