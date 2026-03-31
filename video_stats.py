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
def playlist_items():
    max_results = 50
    playlist_id = get_playlist_id()
    url = f'{BASE_URL}playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={API_KEY}'

    response = requests.get(url)

    data = response.json()

    return data 


if __name__ == "__main__":
    get_playlist_id()