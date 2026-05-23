import ast
import html
import re
from functools import lru_cache
from pathlib import Path

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import Normalizer

MOVIES_PATH = "tmdb_5000_movies.csv"
CREDITS_PATH = "tmdb_5000_credits.csv"
STATIC_DIR = Path("static")
POSTER_DIR = STATIC_DIR / "posters" / "tmdb"
N_CLUSTERS = 8
DISPLAY_PER_CLUSTER = 24
SELECTED_CLUSTER_LIMIT = 72

CLUSTER_NAMES = {
    0: "Crime, Action & Dark Thrillers",
    1: "Romance, Comedy & Life Stories",
    2: "Family, Relationships & Survival",
    3: "New York, Fame & Urban Stories",
    4: "Sci-Fi, Space & Future Worlds",
    5: "Fantasy, Family & Adventure",
    6: "School, Youth & Coming of Age",
    7: "War, History & Political Conflict",
}


def _parse_names(value, limit=None):
    try:
        items = ast.literal_eval(value) if isinstance(value, str) else []
    except (ValueError, SyntaxError):
        return []

    names = [item.get("name", "") for item in items if isinstance(item, dict) and item.get("name")]
    return names[:limit] if limit else names


def _director(value):
    try:
        items = ast.literal_eval(value) if isinstance(value, str) else []
    except (ValueError, SyntaxError):
        return ""

    for item in items:
        if isinstance(item, dict) and item.get("job") == "Director":
            return item.get("name", "")
    return ""


def _slugify(value):
    slug = re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")
    return slug or "movie"


def _prepare_movies():
    movies = pd.read_csv(MOVIES_PATH)
    credits = pd.read_csv(CREDITS_PATH)
    data = movies.merge(credits, left_on="id", right_on="movie_id", suffixes=("", "_credits"))

    data["description"] = data["overview"].fillna("")
    data = data[data["description"].str.len() > 40].copy()

    data["genre"] = data["genres"].apply(lambda value: ", ".join(_parse_names(value, limit=3)) or "Movie")
    data["genre_terms"] = data["genres"].apply(lambda value: " ".join(_parse_names(value)))
    data["keywords_text"] = data["keywords"].apply(lambda value: " ".join(_parse_names(value, limit=12)))
    data["cast_text"] = data["cast"].apply(lambda value: " ".join(_parse_names(value, limit=5)))
    data["director_text"] = data["crew"].apply(_director)
    data["year"] = pd.to_datetime(data["release_date"], errors="coerce").dt.year.fillna(0).astype(int)
    data["link"] = "https://www.themoviedb.org/movie/" + data["id"].astype(str)
    data["poster_path"] = data.apply(
        lambda row: f"posters/tmdb/{_slugify(row['title'])}-{row['id']}.svg",
        axis=1,
    )
    data["cluster_text"] = (
        data["description"]
        + " "
        + data["tagline"].fillna("")
        + " "
        + data["genre_terms"]
        + " "
        + data["keywords_text"]
        + " "
        + data["cast_text"]
        + " "
        + data["director_text"]
    ).fillna("")

    return data


def _ensure_cover_files(data):
    POSTER_DIR.mkdir(parents=True, exist_ok=True)
    palette = [
        ("#231942", "#5e548e", "#e0b1cb"),
        ("#432818", "#99582a", "#ffe6a7"),
        ("#14213d", "#1d4ed8", "#bfdbf7"),
        ("#3d0c11", "#9d0208", "#ffba08"),
        ("#12372a", "#436850", "#fbfada"),
        ("#2f1b25", "#8a2846", "#f4acb7"),
    ]

    for index, row in data.iterrows():
        path = STATIC_DIR / row["poster_path"]
        if path.exists():
            continue

        bg, accent, highlight = palette[int(index) % len(palette)]
        title = str(row["title"])
        words = title.split()
        if len(words) > 4:
            midpoint = (len(words) + 1) // 2
            lines = [" ".join(words[:midpoint]), " ".join(words[midpoint:])]
        else:
            lines = [title]

        start_y = 205 if len(lines) > 1 else 230
        title_svg = "".join(
            f'<text x="40" y="{start_y + i * 48}" class="title">{html.escape(line)}</text>'
            for i, line in enumerate(lines)
        )
        cover = f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="740" viewBox="0 0 500 740" role="img" aria-label="{html.escape(title)} cover">
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="{bg}"/>
      <stop offset="1" stop-color="{accent}"/>
    </linearGradient>
    <style>
      .label {{ fill: {highlight}; font: 700 22px Arial, sans-serif; letter-spacing: 3px; }}
      .title {{ fill: #ffffff; font: 800 40px Arial, sans-serif; letter-spacing: 0; }}
      .meta {{ fill: rgba(255,255,255,0.86); font: 700 19px Arial, sans-serif; letter-spacing: 1px; }}
      .small {{ fill: rgba(255,255,255,0.72); font: 600 17px Arial, sans-serif; }}
    </style>
  </defs>
  <rect width="500" height="740" fill="url(#bg)"/>
  <circle cx="410" cy="115" r="118" fill="rgba(255,255,255,0.12)"/>
  <circle cx="80" cy="640" r="160" fill="rgba(0,0,0,0.16)"/>
  <rect x="34" y="34" width="432" height="672" rx="22" fill="none" stroke="rgba(255,255,255,0.28)" stroke-width="3"/>
  <text x="40" y="92" class="label">TMDB MOVIE</text>
  {title_svg}
  <text x="40" y="510" class="meta">{html.escape(str(row["genre"]).upper()[:34])}</text>
  <text x="40" y="550" class="meta">{html.escape(str(row["year"]))}</text>
  <rect x="40" y="610" width="160" height="6" rx="3" fill="{highlight}"/>
  <text x="40" y="660" class="small">Text similarity cluster</text>
</svg>
'''
        path.write_text(cover, encoding="utf-8")


@lru_cache(maxsize=1)
def cluster_movies():
    data = _prepare_movies()

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=3,
        max_features=10000,
    )
    X = vectorizer.fit_transform(data["cluster_text"])
    reducer = NMF(n_components=N_CLUSTERS, random_state=42, init="nndsvda", max_iter=500)
    reduced = reducer.fit_transform(X)
    reduced = Normalizer(copy=False).fit_transform(reduced)

    model = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=15)
    labels = model.fit_predict(reduced)
    data["cluster"] = labels

    terms = vectorizer.get_feature_names_out()
    cluster_keywords = {}
    for cluster_id in range(N_CLUSTERS):
        average_tfidf = X[labels == cluster_id].mean(axis=0).A1
        top_terms = [terms[index] for index in average_tfidf.argsort()[::-1][:6]]
        cluster_keywords[cluster_id] = ", ".join(top_terms)

    score = round(silhouette_score(reduced, data["cluster"], metric="cosine"), 3)
    cluster_counts = data["cluster"].value_counts().sort_index().to_dict()
    cover_rows = pd.concat(
        [
            sort_for_display(group).head(SELECTED_CLUSTER_LIMIT)
            for _, group in data.groupby("cluster")
        ]
    ).drop_duplicates(subset="id")
    _ensure_cover_files(cover_rows)

    return data, cluster_keywords, score, cluster_counts


def sort_for_display(data):
    return data.sort_values(["vote_count", "popularity"], ascending=False)
