"""
Ek baar apne PC pe run karo — YouTube OAuth token banane ke liye.
Token ban jayega aur GitHub Secret mein daal do.

Steps:
1. pip install google-auth-oauthlib google-api-python-client
2. client_secret.json apne folder mein rakho
3. python setup_youtube_token.py
4. Browser mein login karo
5. youtube_token.json copy karke GitHub Secret YOUTUBE_TOKEN_JSON mein daal do
"""

import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
creds = flow.run_local_server(port=0)

with open("youtube_token.json", "w") as f:
    f.write(creds.to_json())

print("\nDone! youtube_token.json ban gaya.")
print("Ab is file ka content copy karo aur GitHub Secret mein daal do:")
print("Secret name: YOUTUBE_TOKEN_JSON")
print("\nToken content:")
print(open("youtube_token.json").read())
