import requests
import pandas as pd
import os
from datetime import datetime

# YouTube API Key (Replace with your actual key)
API_KEY = "AIzaSyCbE9LwgnK_lGlMTpQpItxi58WCkhfwit4"
REGION = "IN"
MAX_RESULTS = 50
CSV_FILE = "trending_videos.csv"

def fetch_trending_videos():
    """Fetch trending YouTube videos and return as a list."""
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode={REGION}&maxResults={MAX_RESULTS}&key={API_KEY}"
    response = requests.get(url).json()

    videos = []
    for idx, video in enumerate(response.get("items", []), start=1):
        videos.append({
            "Trending_Date": datetime.now().strftime("%Y-%m-%d"),
            "Rank": idx,
            "Video_ID": video["id"],
            "Title": video["snippet"]["title"],
            "Views": int(video["statistics"].get("viewCount", 0)),
            "Likes": int(video["statistics"].get("likeCount", 0)),
            "Comments": int(video["statistics"].get("commentCount", 0))
        })

    return videos

def save_data():
    """Fetch data and append to CSV file."""
    videos = fetch_trending_videos()
    df = pd.DataFrame(videos)

    # Append data if file exists, otherwise create a new file
    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode='a', index=False, header=False)
    else:
        df.to_csv(CSV_FILE, index=False)

    print("Trending videos data saved!")

if __name__ == "__main__":
    save_data()
