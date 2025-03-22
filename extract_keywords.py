import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob

# Load dataset
df = pd.read_csv("youtube_trending_data.csv")

# Ensure correct date parsing
if "Trending_Date" in df.columns:
    df["Trending_Date"] = pd.to_datetime(df["Trending_Date"], errors='coerce')

df = df.dropna(subset=["Trending_Date"])

# Convert to string (if not already)
df["Trending_Date"] = df["Trending_Date"].astype(str)

# Filter videos from the last 7 days
recent_days = 7
latest_date = df["Trending_Date"].max()
df_filtered = df[df["Trending_Date"] >= (pd.to_datetime(latest_date) - pd.Timedelta(days=recent_days)).strftime("%Y-%m-%d")]

# Extract keywords from titles & descriptions using TextBlob
all_text = " ".join(df_filtered["Title"].astype(str) + " " + df_filtered["Description"].astype(str))
blob = TextBlob(all_text)

# Get top keywords (nouns only)
words = [word.lower() for word, tag in blob.tags if tag.startswith("NN")]  # Nouns
word_freq = Counter(words)
top_keywords = dict(word_freq.most_common(50))

# Generate Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(top_keywords)
wordcloud.to_file("wordcloud.png")

# Show the word cloud (optional)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
