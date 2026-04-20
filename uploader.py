import json
import os
import time
from datetime import datetime, timedelta, timezone

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

with open("config.json") as f:
    config = json.load(f)

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = "youtube_token.json"
CLIENT_SECRET_FILE = config.get("youtube_client_secret_file", "client_secret.json")
CATEGORY_ID = config.get("youtube_category_id", "20")
PRIVACY = config.get("youtube_privacy", "public")


def get_youtube_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def upload_to_youtube(
    video_path: str,
    title: str,
    description: str,
    tags: list,
    publish_at: str = None
) -> str:
    youtube = get_youtube_service()

    if len(title) > 100:
        title = title[:97] + "..."

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": CATEGORY_ID,
            "defaultLanguage": "hi"
        },
        "status": {
            "privacyStatus": PRIVACY if not publish_at else "private",
            "selfDeclaredMadeForKids": False
        }
    }

    if publish_at:
        body["status"]["publishAt"] = publish_at
        body["status"]["privacyStatus"] = "private"

    media = MediaFileUpload(
        video_path,
        mimetype="video/mp4",
        resumable=True,
        chunksize=1024 * 1024
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    print(f"Uploading: {title}")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")

    video_id = response.get("id")
    print(f"Uploaded! https://youtu.be/{video_id}")
    return video_id


def schedule_uploads(video_files: list, titles: list, descriptions: list, tags_list: list):
    gap_hours = config.get("gap_hours", 3)
    now = datetime.now(timezone.utc)

    for i, (video_path, title, description, tags) in enumerate(
        zip(video_files, titles, descriptions, tags_list)
    ):
        publish_time = now + timedelta(hours=gap_hours * i)
        publish_at = publish_time.strftime("%Y-%m-%dT%H:%M:%S.0Z")
        print(f"Scheduling video {i+1} at {publish_at}")
        upload_to_youtube(video_path, title, description, tags, publish_at=publish_at)
        time.sleep(5)
