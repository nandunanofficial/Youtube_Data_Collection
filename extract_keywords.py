import pandas as pd
import nltk
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("youtube_trending_data.csv")

# Ensure the dataset has the correct column
if "Trending_Date" in df.columns:
    df["Trending_Date"] = pd.to_datetime(df["Trending_Date"], errors='coerce')

# Drop rows where date parsing failed
df = df.dropna(subset=["Trending_Date"])

# Convert to string (if not already)
df["Trending_Date"] = df["Trending_Date"].astype(str)

# Filter videos from the last X days (e.g., last 7 days)
recent_days = 7
latest_date = df["Trending_Date"].max()
df_filtered = df[df["Trending_Date"] >= (pd.to_datetime(latest_date) - pd.Timedelta(days=recent_days)).strftime("%Y-%m-%d")]

# Extract keywords from titles & descriptions
nltk.download('punkt')

all_text = " ".join(df_filtered["Title"].astype(str) + " " + df_filtered["Description"].astype(str))
words = nltk.word_tokenize(all_text)
words = [word.lower() for word in words if word.isalpha()]  # Remove numbers & special chars

# Get top keywords
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
