import httplib2
import os
import random
import sys
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
# Removed the import for argparser since we're not using command-line arguments

# Configuration and retry parameters remain unchanged
httplib2.RETRIES = 1
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
CLIENT_SECRETS_FILE = "C:\DogTube\AutoTube\client_secrets.json"
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MISSING_CLIENT_SECRETS_MESSAGE = """..."""  # Keep the existing message as is

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope=YOUTUBE_UPLOAD_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)
    print("A")
    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()
    print(credentials)
    print("B")
    if credentials is None or credentials.invalid:
        raise Exception("Failed to obtain valid credentials. Please check your OAuth setup.")

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                 http=credentials.authorize(httplib2.Http()))

def initialize_upload(youtube, options):
    tags = options.get("keywords", "").split(",") if "keywords" in options else None

    body = {
        "snippet": {
            "title": options["title"],
            "description": options["description"],
            "tags": tags,
        },
        "status": {
            "privacyStatus": options["privacyStatus"]
        }
    }

    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(options["file"], chunksize=-1, resumable=True)
    )

    resumable_upload(insert_request)

def resumable_upload(insert_request):
    # This function remains unchanged
    ...

def upload_video(video_data):
    if not os.path.exists(video_data['file']):
        exit("Please specify a valid file using the --file= parameter.")

    youtube = get_authenticated_service()
    try:
        initialize_upload(youtube, video_data)
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")

if __name__ == '__main__':
    video_data = {
        "file": "C:\\DogTube\\AutoTube\\video.mp4",  # Update this path to your video file's path
        "title": "Best of memes!",
        "description": "#shorts \n Giving you the hottest memes of the day with funny comments!",
        "keywords": "meme,reddit",
        "privacyStatus": "private"
    }
    upload_video(video_data)
