import requests
import os 
from dotenv import load_dotenv

# import env variables
load_dotenv(dotenv_path = "./.env")
API_KEY = os.getenv("API_KEY")

BASE_URL = 'https://youtube.googleapis.com/youtube/v3'
channel_handle = 'MrBeast'

# Fetch playlist id
def get_playlist_id():
    try:
        url = f'{BASE_URL}/channels?part=contentDetails&forHandle={channel_handle}&key={API_KEY}'

        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        playlist_id = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        return playlist_id

    except requests.exceptions.RequestException as e:
        raise e 

#Fecth playlist items
def get_videos_ids( playlist_id ):
    global API_KEY
    max_results = 50
    page_token = None
    videos_ids = []
    
    # Playlist items call
    playlist_items_url = f'{BASE_URL}/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={API_KEY}'

    try:

        url = playlist_items_url

        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        for item in data.get('items',[]):
            video_id = item['contentDetails']['videoId']
            videos_ids.append(video_id)
            
        return videos_ids

    except requests.exceptions.RequestException as e:
        raise e

    return 0


if __name__ == "__main__":
    playlist_id = get_playlist_id()
    print(get_videos_ids(playlist_id))