import requests
import json
import difflib
# Enter the API key here
api_key = 'AIzaSyCygSGzGJ8gMH0Op1GlIzql9-Yx84yCFyE'

# Enter the video ID here
video_id = '2kKsNUA_Suc'

# Make a request to the YouTube API to get the video data
response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet')
json_data = json.loads(response.text)

# Get the tags from the video data
tags = json_data['items'][0]['snippet']['tags']

# Get the tags from the top performing videos
related_tags = []
for video_id in related_videos:
    response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet')
    json_data = json.loads(response.text)
    if 'tags' in json_data['items'][0]['snippet']:
        related_tags += json_data['items'][0]['snippet']['tags']

related_videos = list(set(related_videos))
related_tags = []
for video_id in related_videos:
    response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet')
    json_data = json.loads(response.text)
    if 'tags' in json_data['items'][0]['snippet']:
        related_tags += json_data['items'][0]['snippet']['tags']

related_tags = list(set(related_tags))

# Compare the tags of the given video with the tags of the top performing videos
diff = difflib.ndiff(tags, related_tags)
# Print the differences
print('Differences in tags:')
for line in diff:
    if line.startswith('- '):
        print(line)