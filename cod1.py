import openpyxl
from datetime import datetime, timezone
import os
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Load the Excel sheet
workbook = openpyxl.load_workbook('bleh.xlsx')
worksheet = workbook.active

# Set up the YouTube API client
def get_authenticated_service():
    # Set up the OAuth2.0 credentials
    creds = Credentials.from_authorized_user_file('client_secret_397498834734-b4or58u9452gbo95e6ktcfr71vc9m3pq.apps.googleusercontent.com.json', [r'C:\Users\Rajpu\Downloads\client_secret_397498834734-b4or58u9452gbo95e6ktcfr71vc9m3pq.apps.googleusercontent.com.json'])
    # Build the YouTube API client
    service = build('youtube', 'v3', credentials=creds)
    return service
youtube = get_authenticated_service()

# Set up the LinkedIn API client
linkedin = Linkedin()

# Set up the Facebook API client
fb_access_token = 'your-access-token'
fb_api = facebook.GraphAPI(access_token=fb_access_token)

# Loop through each row in the Excel sheet and upload the videos/posts
for row in worksheet.iter_rows(min_row=2, values_only=True):
    title = row[0]
    description = row[1]
    file_path = row[2]
    platform = row[3].lower()
    date_time = row[4]
    tags = row[5]
    thumbnail_path = row[6]
    privacy = row[7]
    comments = row[8]

    # Format the date and time
    date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)

    # Upload the video/post to the respective platform
    if platform == 'youtube':
        # Upload the video to YouTube
        try:
            # Create a new video resource
            video = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags.split(','),
                    'categoryId': '22'
                },
                'status': {
                    'privacyStatus': privacy
                }
            }
            # Upload the video
            insert_request = youtube.videos().insert(part='snippet,status', body=video, media_body=file_path)
            insert_request.execute()

            # Set the thumbnail image for the video
            if thumbnail_path:
                video_id = insert_request.execute()['id']
                youtube.thumbnails().set(videoId=video_id, media_body=thumbnail_path).execute()

            # Enable/disable comments for the video
            if comments.lower() == 'no':
                youtube.commentThreads().setModerationStatus(
                    id=video_id, moderationStatus='heldForReview').execute()

            print('Video uploaded to YouTube: ' + title)
        except HttpError as e:
            print('An error occurred: %s' % e)
            print('Video not uploaded: ' + title)