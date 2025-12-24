
import argparse
import os
from pathlib import Path

import numpy as np
from src.logger import logging
from src.utils import load_object


def _load_with_fallback(primary: Path, fallback: Path | None = None):
    """
    Load an artifact, optionally falling back to an alternate path.
    Raises the underlying exception if both are missing.
    """
    try:
        return load_object(primary)
    except Exception as exc:
        if fallback is None:
            raise
        logging.warning(
            "Primary artifact %s missing, trying fallback %s", primary, fallback
        )
        return load_object(fallback)

# Allow overriding artifact location (defaults to ./artifacts)
ARTIFACT_DIR = Path(os.environ.get("ARTIFACT_DIR", "artifacts"))

logging.info("Loading trained model")
model = load_object(ARTIFACT_DIR / "model.pkl")

logging.info("Load books title object")
books_title = _load_with_fallback(
    ARTIFACT_DIR / "books_title.pkl", ARTIFACT_DIR / "books_name.pkl"
)

logging.info("Loading book matrix")
book_pivot = load_object(ARTIFACT_DIR / "book_pivot.pkl")

logging.info("Loading ratings")
final_rating = load_object(ARTIFACT_DIR / "ratings.pkl")


def fetch_poster(suggestion, query_title):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]:
        if name == query_title:
            continue  # Skip the queried title itself
        ids = np.where(final_rating["title"] == name)[0]
        if ids.size == 0:
            logging.warning("Poster not found for title '%s'", name)
            continue
        ids_index.append(ids[0])

    for idx in ids_index:
        url = final_rating.iloc[idx]['url']
        poster_url.append(url)

    return poster_url


def recommend_book(book_name):
    if book_name not in book_pivot.index:
        raise ValueError(f"Book '{book_name}' not found in catalog.")

    books_list = []
    book_id_arr = np.where(book_pivot.index == book_name)[0]
    if book_id_arr.size == 0:
        raise ValueError(f"Book '{book_name}' not found in catalog.")
    book_id = book_id_arr[0]
    distance, suggestion = model.kneighbors(
        book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6
    )

    poster_url = fetch_poster(suggestion, book_name)
    
    for i in range(len(suggestion)):
            books = book_pivot.index[suggestion[i]]
            for j in books:
                if j != book_name:
                    books_list.append(j)
    return books_list , poster_url   


def _cli():
    parser = argparse.ArgumentParser(
        description="Query similar books using the trained recommendation model."
    )
    parser.add_argument(
        "--book",
        required=True,
        help="Exact book title to search for (must exist in the pivot table).",
    )
    args = parser.parse_args()

    try:
        recommendations, poster_urls = recommend_book(args.book)
    except Exception as exc:  # broad on purpose for CLI use
        logging.exception("Failed to generate recommendations")
        raise SystemExit(f"Error generating recommendations: {exc}") from exc

    if not recommendations:
        print(f"No recommendations found for '{args.book}'.")
        return

    print(f"Recommendations for '{args.book}':")
    for idx, title in enumerate(recommendations, start=1):
        poster = poster_urls[idx - 1] if idx - 1 < len(poster_urls) else ""
        line = f"{idx}. {title}"
        if poster:
            line += f" | cover: {poster}"
        print(line)


if __name__ == "__main__":
    _cli()
