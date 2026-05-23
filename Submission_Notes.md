# Lecture 3 Clustering Assignment Submission Notes

## Chosen option
Option 2: Create a web page that displays movies which have been clustered according to similarity of text description.

## Project title
CineCluster | Movie Similarity Explorer

## Objective
The aim of this project is to demonstrate clustering in web mining by grouping movies into meaningful clusters based on the similarity of their textual descriptions.

## Dataset
The project uses the TMDB 5000 movie dataset:

- `tmdb_5000_movies.csv` - movie title, overview, genre, keywords, tagline, popularity, votes, and release data.
- `tmdb_5000_credits.csv` - cast and crew data linked to each movie.

After cleaning, 4,797 movies with usable overviews are clustered. The covers in `static/posters/tmdb/` are generated local cover-style images for the web page, not official movie posters.

## Methodology
1. TMDB movie and credit datasets are merged using the movie ID.
2. Text is built from movie overview, tagline, genres, keywords, top cast, and director.
3. Text features are converted into numerical vectors using TF-IDF.
4. Non-negative Matrix Factorization (NMF) is applied to learn cleaner topic-style features from the sparse TF-IDF matrix.
5. K-Means clustering groups similar movies into 8 theme-based clusters using the NMF feature representation.
6. The web page displays each cluster with a meaningful theme name, top keywords, generated cover images, and top movie examples.
7. The clustering quality is evaluated using cosine silhouette score, which is suitable for normalized text vectors.

## Cluster names
The clustered groups are shown with descriptive names instead of only numeric labels:

- `Crime, Action & Dark Thrillers`
- `Romance, Comedy & Life Stories`
- `Family, Relationships & Survival`
- `New York, Fame & Urban Stories`
- `Sci-Fi, Space & Future Worlds`
- `Fantasy, Family & Adventure`
- `School, Youth & Coming of Age`
- `War, History & Political Conflict`

The original cluster number is still displayed as a small technical label for clarity.
The current cosine silhouette score is 0.612, which indicates good separation for this movie text clustering task.

## Algorithm used
K-Means clustering was selected because it is simple, fast, and suitable for grouping text vectors when the number of desired clusters is known. The model uses TF-IDF with unigrams and bigrams, reduces the text matrix using NMF topic features, then reports cosine silhouette score because cosine similarity is appropriate for normalized text features.

## How to run
Use Python 3.10 to 3.12 for the smoothest package installation with the versions in `requirements.txt`.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Then open this address in the browser:

```text
http://127.0.0.1:5000
```

## Files included
- `app.py` - Flask application and clustering logic.
- `tmdb_clustering.py` - shared TMDB loading, feature extraction, clustering, scoring, and cover generation logic.
- `tmdb_5000_movies.csv` - TMDB movie metadata dataset.
- `tmdb_5000_credits.csv` - TMDB cast and crew dataset.
- `static/posters/tmdb/` - generated local cover-style images used by the web page.
- `templates/index.html` - web page layout.
- `static/style.css` - web page styling.
- `generate_static.py` - static HTML generator.
- `requirements.txt` - Python packages required.
- `Submission_Notes.md` - short explanation of the assignment.

## Conclusion
The project shows how text descriptions can be transformed into features and clustered into meaningful groups. This supports the lecture concept that clustering partitions data objects into meaningful sub-classes based on similarity.
