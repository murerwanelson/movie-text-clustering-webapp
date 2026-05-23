"""Generate a standalone HTML page for the TMDB movie clustering assignment.
Run: python generate_static.py
Then open: index_static.html
"""

import html
from pathlib import Path

from tmdb_clustering import (
    CLUSTER_NAMES,
    DISPLAY_PER_CLUSTER,
    N_CLUSTERS,
    cluster_movies,
    sort_for_display,
)


movies, keywords, score, cluster_counts = cluster_movies()

sections = []
for cid, group in movies.groupby("cluster"):
    cards = []
    for _, row in sort_for_display(group).head(DISPLAY_PER_CLUSTER).iterrows():
        cards.append(f"""
        <article class="movie-card">
            <div class="poster-frame">
                <img
                    class="movie-poster"
                    src="static/{html.escape(row['poster_path'])}"
                    alt="{html.escape(row['title'])} movie poster"
                    loading="lazy"
                />
                <span class="poster-fallback">{html.escape(row['title'])}</span>
                <span class="poster-year">{html.escape(str(row['year']))}</span>
            </div>
            <div class="movie-content">
                <div class="movie-meta">{html.escape(str(row['genre']))}</div>
                <h3>{html.escape(row['title'])}</h3>
                <p>{html.escape(row['description'])}</p>
                <a class="movie-link" href="{html.escape(row['link'])}" target="_blank" rel="noopener">View on TMDB</a>
            </div>
        </article>
        """)

    shown = min(DISPLAY_PER_CLUSTER, int(cluster_counts[cid]))
    sections.append(f"""
    <section class="cluster-section" id="cluster-{cid}">
        <div class="cluster-header">
            <div>
                <p class="cluster-id">Cluster {cid}</p>
                <h2>{html.escape(CLUSTER_NAMES[cid])}</h2>
                <p><span>Keywords</span>{html.escape(keywords[cid])}</p>
            </div>
            <span class="count-badge">Showing {shown} of {int(cluster_counts[cid])}</span>
        </div>
        <div class="movie-grid">
            {''.join(cards)}
        </div>
    </section>
    """)


html_output = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CineCluster | Movie Similarity Explorer</title>
    <link rel="stylesheet" href="static/style.css" />
</head>
<body>
    <nav class="topbar">
        <a class="brand" href="index_static.html">
            <span class="brand-mark">C</span>
            <span>CineCluster</span>
        </a>
        <span class="topbar-meta">Similarity Explorer</span>
    </nav>

    <header class="hero">
        <div class="hero-content">
            <div class="hero-copy">
                <p class="eyebrow">TMDB Movie Text Clustering</p>
                <h1>Discover movies by story similarity.</h1>
                <p>Browse TMDB movies organized into theme-based clusters using overviews, genres, keywords, cast, and crew metadata.</p>
                <div class="stats">
                    <div><strong>{sum(cluster_counts.values())}</strong><span>Movies</span></div>
                    <div><strong>{N_CLUSTERS}</strong><span>Clusters</span></div>
                    <div><strong>{score}</strong><span>Score</span></div>
                </div>
            </div>
            <div class="hero-posters" aria-hidden="true">
                <img src="static/posters/tmdb/inception-27205.svg" alt="" />
                <img src="static/posters/tmdb/avatar-19995.svg" alt="" />
                <img src="static/posters/tmdb/the-dark-knight-155.svg" alt="" />
            </div>
        </div>
    </header>
    <main class="container">
        <section class="control-panel">
            <div>
                <h2>Cluster Browser</h2>
                <p>Each group is formed from similar TMDB overviews, genres, keywords, cast, and director metadata. The page shows top examples from each cluster to keep browsing fast.</p>
            </div>
        </section>
        <nav class="cluster-tabs" aria-label="Cluster filters">
            <a href="index_static.html" class="active">All</a>
            {''.join(f'<a href="#cluster-{cid}">{html.escape(CLUSTER_NAMES[cid])}</a>' for cid in range(N_CLUSTERS))}
        </nav>
        {''.join(sections)}
    </main>
    <footer>
        <p>Created for Lecture 3 clustering assignment: TMDB movies clustered according to similarity of text description and metadata.</p>
    </footer>
</body>
</html>
"""

Path("index_static.html").write_text(html_output, encoding="utf-8")
print("Generated index_static.html")
