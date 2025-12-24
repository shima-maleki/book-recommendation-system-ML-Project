"""
Streamlit UI for interacting with the FastAPI recommendation service.

Set API_URL env var to point at the FastAPI endpoint (default http://localhost:18000/recommend).
"""
import os
from typing import List, Optional

import requests
import streamlit as st

# Config
# Default to local Docker host mapping (compose maps 18000:8000).
API_URL = os.environ.get("API_URL", "http://localhost:18000/recommend")


def render_header():
    st.set_page_config(page_title="Book Recommender", page_icon="📚", layout="wide")
    st.markdown(
        """
        <style>
        .hero {
            padding: 2.5rem;
            border-radius: 24px;
            background: linear-gradient(135deg, #1f2937 0%, #0f172a 40%, #0b1625 100%);
            color: #e2e8f0;
            box-shadow: 0 10px 40px rgba(0,0,0,0.25);
        }
        .hero h1 { font-size: 2.2rem; margin-bottom: 0.25rem; }
        .hero p { color: #cbd5e1; margin: 0.2rem 0 0; }
        .result-card {
            padding: 1rem 1.25rem;
            border-radius: 16px;
            background: #0b1625;
            border: 1px solid #1f2937;
            color: #e2e8f0;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
        }
        .result-card h3 { margin: 0; color: #e2e8f0; }
        .poster { color: #94a3b8; font-size: 0.9rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="hero">
            <h1>📚 Book Recommender</h1>
            <p>Type a title, get similar reads instantly. Powered by item-based collaborative filtering.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_results(book: str, recs: List[str], posters: List[Optional[str]]):
    st.subheader(f"Recommendations for “{book}”")
    for idx, rec in enumerate(recs):
        poster = posters[idx] if idx < len(posters) else None
        with st.container():
            st.markdown(
                f"""
                <div class="result-card">
                    <h3>{idx+1}. {rec}</h3>
                    {"<div class='poster'>Cover: " + poster + "</div>" if poster else ""}
                </div>
                """,
                unsafe_allow_html=True,
            )


def main():
    render_header()
    st.write("")

    with st.form("recommend_form"):
        book_title = st.text_input(
            "Book title",
            placeholder="e.g., A Bend in the Road",
            help="Use an exact title from the catalog.",
        )
        submitted = st.form_submit_button("Recommend", use_container_width=True)

    if submitted:
        if not book_title:
            st.warning("Please enter a book title.")
            return
        try:
            with st.spinner("Fetching recommendations..."):
                resp = requests.post(API_URL, json={"book": book_title}, timeout=30)
        except Exception as exc:  # broad for UI
            st.error(f"Failed to reach API at {API_URL}: {exc}")
            return

        if resp.status_code == 200:
            data = resp.json()
            recs = data.get("recommendations", [])
            posters = data.get("poster_urls", [])
            if not recs:
                st.info(f"No recommendations found for “{book_title}”.")
            else:
                render_results(data["book"], recs, posters)
        else:
            detail = resp.json().get("detail", "Unknown error")
            if resp.status_code == 404:
                st.warning(detail)
            else:
                st.error(f"API error ({resp.status_code}): {detail}")

    st.markdown("---")
    st.caption(f"API endpoint: {API_URL}")


if __name__ == "__main__":
    main()
