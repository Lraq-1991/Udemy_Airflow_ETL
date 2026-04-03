import requests
import os 
from dotenv import load_dotenv

# import env variables
load_dotenv(dotenv_path = "./.env")
API_KEY = os.getenv("API_KEY")

BASE_URL = 'https://youtube.googleapis.com/youtube/v3'
channel_handle = 'MrBeast'
max_results = 50

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
    global max_results
    
    page_token = None
    videos_ids = []
    
    # Playlist items path
    playlist_items_url = f'{BASE_URL}/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={API_KEY}'

    try:

        while True:

            url = playlist_items_url

            if page_token:
                url += f"&pageToken={page_token}"

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for item in data.get('items',[]):
                video_id = item['contentDetails']['videoId']
                videos_ids.append(video_id)

            page_token = data.get('nextPageToken')

            if not page_token:
                break
            
        return videos_ids

    except requests.exceptions.RequestException as e:
        raise e


def extract_video_data(video_ids):

    global max_results
    extracted_data = []

    def batch_list(video_id_list, batch_size):
        for video_id in range(0, len(video_id_list), batch_size):
            yield video_id_list[video_id: video_id + batch_size]

    try:
       
        for batch in batch_list(video_ids, max_results):
            video_ids_str = ','.join(batch)

            video_list_url = f"{BASE_URL}/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"

            response = requests.get(video_list_url)

            response.raise_for_status()

            data = response.json()

            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                content_detalis = item['contentDetails']
                statistics = item['statistics']

                video = {
                    "video_id":video_id,
                    "title":snippet['title'],
                    "published_at":snippet['publishedAt'],
                    "view_count":statistics.get('viewCount', None),
                    "like_count":statistics.get('likeCount', None),
                    "comment_count":statistics.get('commentCount', None),
                }

                extracted_data.append(video)
            
        return extracted_data

    except requests.exceptions.RequestException as e:
       
        raise e




if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_ids = get_videos_ids(playlist_id)
    print(extract_video_data(video_ids))