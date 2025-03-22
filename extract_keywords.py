import pandas as pd
import nltk
from nltk.corpus import stopwords
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Download stopwords
nltk.download("stopwords")

CSV_FILE = "youtube_trending_data.csv"
N_DAYS = 7  # Set the period for keyword analysis

def extract_keywords():
    df = pd.read_csv(CSV_FILE, names=["Title", "Description", "Tags", "Trending_Date"])
    df["Trending_Date"] = pd.to_datetime(df["Trending_Date"])
    
    # Filter last N days
    recent_data = df[df["Trending_Date"] >= pd.Timestamp.today() - pd.Timedelta(days=N_DAYS)]

    # Combine Titles, Descriptions, and Tags
    text_data = " ".join(recent_data["Title"].astype(str) + " " + recent_data["Description"].astype(str) + " " + recent_data["Tags"].astype(str))

    # Tokenization
    words = text_data.lower().split()

    # Remove Stopwords
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

    # Count Word Frequency
    word_counts = Counter(filtered_words)
    top_keywords = word_counts.most_common(20)

    print("Top Trending Keywords:")
    for word, count in top_keywords:
        print(f"{word}: {count}")

    # Generate Word Cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(filtered_words))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig("wordcloud.png")  # Save word cloud image
    plt.show()

if __name__ == "__main__":
    extract_keywords()
