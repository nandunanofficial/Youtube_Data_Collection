import requests
import pandas as pd
from datetime import datetime

API_KEY = "AIzaSyCbE9LwgnK_lGlMTpQpItxi58WCkhfwit4"
REGION = "IN"
MAX_RESULTS = 50
CSV_FILE = "youtube_trending_data.csv"

def fetch_trending_videos():
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode={REGION}&maxResults={MAX_RESULTS}&key={API_KEY}"
    response = requests.get(url).json()

    videos = []
    for video in response.get("items", []):
        videos.append({
            "Title": video["snippet"]["title"],
            "Description": video["snippet"]["description"],
            "Tags": ",".join(video["snippet"].get("tags", [])) if "tags" in video["snippet"] else "",
            "Trending_Date": datetime.now().strftime("%Y-%m-%d")
        })

    return videos

def save_data():
    videos = fetch_trending_videos()
    df = pd.DataFrame(videos)
    df.to_csv(CSV_FILE, mode='a', index=False, header=not pd.io.common.file_exists(CSV_FILE))

if __name__ == "__main__":
    save_data()
    print("Trending videos data saved!")
