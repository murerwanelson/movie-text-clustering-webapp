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

The TMDB 5000 movies dataset and credits dataset were first merged using the movie ID. The main clustering text was created by combining each movie’s overview, tagline, genres, keywords, top cast members, and director. Missing text values were cleaned before feature extraction.

The combined text was converted into numerical form using TF-IDF vectorisation with unigrams and bigrams. Since TF-IDF produces a high-dimensional sparse matrix, Non-negative Matrix Factorisation (NMF) was applied to reduce the text representation into cleaner topic-style features.

K-Means clustering was then used to group movies into 8 clusters based on similarity of their text descriptions. Each cluster was given a descriptive theme name by inspecting the top keywords and movie examples within that cluster.

The clustering quality was evaluated using the cosine silhouette score. Cosine similarity was selected because it is suitable for text-based vector representations. The final cosine silhouette score was 0.612, suggesting that the movie descriptions were separated into reasonably meaningful groups.

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

This project demonstrates how clustering can be applied in web mining to group movies based on the similarity of text descriptions. The system transforms unstructured movie descriptions into numerical TF-IDF features, reduces them into topic-style components using NMF, and applies K-Means clustering to create meaningful movie groups.

The final web page presents the clustered movies in a clear and user-friendly way, using descriptive cluster names, top keywords, and movie examples. This supports the Lecture 3 concept that clustering partitions data objects into meaningful sub-classes based on similarity.
