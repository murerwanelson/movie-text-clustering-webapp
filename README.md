# CineCluster

CineCluster is a Flask web app that clusters TMDB movies by similarity of text description and metadata.

The project uses:

- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`
- TF-IDF text features
- NMF topic-style feature reduction
- K-Means clustering
- cosine silhouette score

Current result:

- Movies clustered: 4,797
- Clusters: 8
- Cosine silhouette score: 0.612

## Run Locally

Use Python 3.10 to 3.12 for the smoothest package installation.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Generate Static HTML

```bash
python generate_static.py
```

Then open `index_static.html` in a browser.

## Files

- `app.py` - Flask routes and web app entry point.
- `tmdb_clustering.py` - dataset loading, text feature extraction, NMF, K-Means, scoring, and generated cover artwork.
- `generate_static.py` - creates a standalone static HTML version.
- `templates/index.html` - Flask page template.
- `static/style.css` - UI styling.
- `Submission_Notes.md` - assignment explanation.

Generated cover-style artwork is created in `static/posters/tmdb/` when the model runs. These are local generated placeholders, not official movie posters.
