#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic Movie Recommender (Very Simple)
-------------------------------------
- Content-based only: TF–IDF over genres (+ optional overview), cosine similarity.
- Two commands:
    1) --similar_by_title "Some Movie"
    2) --recommend_for_user <user_id>   (optional; needs ratings.csv)
- Computes everything in-memory, no caching, no complex models.
"""

import argparse
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Basic config (change if your CSV uses different column names)
MOVIE_ID = "movieId"
TITLE = "title"
GENRES = "genres"
OVERVIEW = "overview"  # optional
USER_ID = "userId"
RATING = "rating"


def clean_text(s):
    if pd.isna(s):
        return ""
    return str(s).lower().replace("|", " ")


def build_tfidf(movies_df):
    """Build TF-IDF matrix from genres (+ overview if present)."""
    text_cols = [GENRES] + ([OVERVIEW] if OVERVIEW in movies_df.columns else [])
    corpus = []
    for _, row in movies_df.iterrows():
        parts = [clean_text(row.get(col, "")) for col in text_cols]
        corpus.append(" ".join(parts).strip())

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,1), min_df=1)
    tfidf = vectorizer.fit_transform(corpus)
    return tfidf, vectorizer


def find_similar_by_title(movies_df, tfidf, query_title, top_k=10):
    """Return top_k movies similar to the given title."""
    # Locate the movie row
    matches = movies_df[movies_df[TITLE].str.lower() == query_title.lower()]
    if matches.empty:
        matches = movies_df[movies_df[TITLE].str.lower().str.contains(query_title.lower(), na=False)]
    if matches.empty:
        raise ValueError(f"Title '{query_title}' not found.")

    ref_idx = matches.index[0]
    # Compute similarities
    sims = cosine_similarity(tfidf[ref_idx], tfidf).flatten()
    # sort by similarity; ignore itself
    order = np.argsort(-sims)
    order = [i for i in order if i != ref_idx][:top_k]

    out = movies_df.loc[order, [MOVIE_ID, TITLE]].copy()
    out["similarity"] = sims[order]
    return out.reset_index(drop=True)


def recommend_for_user_simple(movies_df, tfidf, ratings_df, user_id, top_k=10):
    """
    Very simple 'user recs' based on content:
    1) Find movies the user liked (rating >= 4).
    2) Average their TF-IDF vectors to make a 'taste' vector.
    3) Recommend top_k nearest movies not already rated.
    """
    # Get liked movieIds
    liked = ratings_df[(ratings_df[USER_ID] == user_id) & (ratings_df[RATING] >= 4.0)][MOVIE_ID].tolist()
    if not liked:
        raise ValueError(f"User {user_id} has no liked movies (rating >= 4).")

    # Map from row index to movieId
    id_to_row = {mid: i for i, mid in enumerate(movies_df[MOVIE_ID].tolist())}
    like_rows = [id_to_row[m] for m in liked if m in id_to_row]
    if not like_rows:
        raise ValueError("None of the user's liked movies are present in movies.csv.")

    # Compute centroid of liked vectors
    centroid = tfidf[like_rows].mean(axis=0)  # 1 x D

    # Similarity to all movies
    sims = cosine_similarity(centroid, tfidf).flatten()

    # Exclude movies the user has already rated
    already = set(ratings_df[ratings_df[USER_ID] == user_id][MOVIE_ID].tolist())
    candidates = [(i, sims[i]) for i in range(len(movies_df)) if movies_df.iloc[i][MOVIE_ID] not in already]

    # Top-k
    candidates.sort(key=lambda x: x[1], reverse=True)
    top = candidates[:top_k]

    rows = [i for i, _ in top]
    out = movies_df.iloc[rows][[MOVIE_ID, TITLE]].copy()
    out["score"] = [s for _, s in top]
    return out.reset_index(drop=True)


def main():
    parser = argparse.ArgumentParser(description="Basic Movie Recommender (Very Simple)")
    parser.add_argument("--movies_csv", type=str, default="movies.csv", help="Path to movies.csv")
    parser.add_argument("--ratings_csv", type=str, default=None, help="Optional: path to ratings.csv")
    parser.add_argument("--similar_by_title", type=str, help="Find similar movies by this title")
    parser.add_argument("--recommend_for_user", type=int, help="User ID for simple content-based recs")
    parser.add_argument("--top_k", type=int, default=10, help="How many results to show")
    args = parser.parse_args()

    # Load CSV(s)
    movies_df = pd.read_csv(args.movies_csv)
    # Ensure titles are strings and index is row-order
    movies_df[TITLE] = movies_df[TITLE].astype(str)
    movies_df = movies_df.reset_index(drop=True)

    # Build TF-IDF in-memory
    tfidf, _ = build_tfidf(movies_df)

    # Option 1: similar by title
    if args.similar_by_title:
        res = find_similar_by_title(movies_df, tfidf, args.similar_by_title, top_k=args.top_k)
        print(res.to_string(index=False))

    # Option 2: user recs (needs ratings.csv)
    if args.recommend_for_user is not None:
        if not args.ratings_csv:
            raise SystemExit("Please provide --ratings_csv for user recommendations.")
        ratings_df = pd.read_csv(args.ratings_csv)
        res = recommend_for_user_simple(movies_df, tfidf, ratings_df, args.recommend_for_user, top_k=args.top_k)
        print(res.to_string(index=False))


if __name__ == "__main__":
    main()
