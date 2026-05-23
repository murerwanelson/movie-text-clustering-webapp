import os
from flask import Flask, render_template, request

from tmdb_clustering import (
    CLUSTER_NAMES,
    DISPLAY_PER_CLUSTER,
    N_CLUSTERS,
    SELECTED_CLUSTER_LIMIT,
    cluster_movies,
    sort_for_display,
)

app = Flask(__name__)


@app.route("/")
def index():
    movies, cluster_keywords, silhouette, cluster_counts = cluster_movies()
    selected_cluster = request.args.get("cluster", "all")
    display_limit = DISPLAY_PER_CLUSTER

    if selected_cluster != "all":
        try:
            selected_cluster_id = int(selected_cluster)
        except ValueError:
            selected_cluster = "all"
        else:
            if selected_cluster_id in CLUSTER_NAMES:
                movies = movies[movies["cluster"] == selected_cluster_id]
                display_limit = SELECTED_CLUSTER_LIMIT
            else:
                selected_cluster = "all"

    grouped = {
        cluster_id: sort_for_display(group).head(display_limit).to_dict(orient="records")
        for cluster_id, group in movies.groupby("cluster")
    }

    return render_template(
        "index.html",
        grouped=grouped,
        keywords=cluster_keywords,
        cluster_names=CLUSTER_NAMES,
        cluster_counts=cluster_counts,
        silhouette=silhouette,
        total_movies=sum(cluster_counts.values()),
        n_clusters=N_CLUSTERS,
        selected_cluster=selected_cluster,
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
