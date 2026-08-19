import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies_df = pd.read_csv("ml-latest-small/movies.csv")
tags_df = pd.read_csv("ml-latest-small/tags.csv")

movies_df["clean_genres"] = movies_df["genres"].str.replace("|", " ")

user_tags = (
    tags_df.groupby("movieId")["tag"]
    .apply(lambda tag_list: " ".join(str(item) for item in tag_list if pd.notnull(item)))
    .reset_index()
)

merged_data = pd.merge(movies_df, user_tags, on="movieId", how="left")
merged_data["tag"] = merged_data["tag"].fillna("")

merged_data["combined_text"] = (
    merged_data["clean_genres"] + " " + merged_data["tag"]
).str.lower()

final_movies = merged_data[["movieId", "title", "combined_text"]].copy()

vectorizer = CountVectorizer(max_features=5000, stop_words="english")
feature_vectors = vectorizer.fit_transform(final_movies["combined_text"]).toarray()

similarity_scores = cosine_similarity(feature_vectors)

pickle.dump(final_movies, open("movies_list.pkl", "wb"))
pickle.dump(similarity_scores, open("similarity.pkl", "wb"))