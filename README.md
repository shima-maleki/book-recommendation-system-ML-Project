# 📚 Book Recommendation System (Built from Scratch)

---

## 🚀 Project Overview

This project implements a **Book Recommendation System** built **entirely from scratch** using **Collaborative Filtering** techniques.

The primary objective is to design an **end-to-end machine learning system** that reflects how recommender systems are built in real-world production environments — not just as a notebook experiment, but as a structured, extensible ML pipeline.

This project intentionally focuses on:

* System design and modular ML pipelines
* Real-world data challenges such as sparsity and cold start
* Reproducibility and evaluation
* Transparent progress tracking
* Explicit demonstration of technical skills

---

## 🎯 Problem Statement

Given historical user–book rating interactions, predict which books a user is most likely to enjoy next.

Key challenges addressed:

* Highly sparse user–item interaction data
* Cold-start users and books
* Similarity computation at scale
* Meaningful evaluation beyond simple accuracy metrics

---

## 🧠 Recommendation Approach

The system is based on **Collaborative Filtering**, where recommendations are generated from patterns in user behavior rather than book metadata.

Approaches implemented / planned:

* **User–User Collaborative Filtering**
* **Item–Item Collaborative Filtering**

This mirrors real-world recommender systems used by platforms such as e-commerce, media streaming, and content discovery services.

---

## 🛠 How This System Is Built (Technical Approach)

This project is developed incrementally using a production-style workflow.

### 1. Data Ingestion

* Loaded raw CSV datasets into a structured raw data layer
* Performed schema validation and basic sanity checks

### 2. Data Preprocessing

* Removed invalid and missing ratings
* Normalized rating values
* Filtered inactive users and low-frequency books to reduce noise

### 3. Feature Engineering

* Constructed sparse user–item matrices
* Applied normalization techniques to stabilize similarity calculations

### 4. Modeling

* Implemented User–User and Item–Item Collaborative Filtering
* Experimented with cosine similarity and Pearson correlation
* Tuned neighbor selection to balance recommendation quality and performance

### 5. Evaluation

* Used RMSE and MAE to evaluate rating prediction accuracy
* Used Precision@K and Recall@K to evaluate recommendation relevance

### 6. Inference

* Built reusable functions for Top-N recommendation generation
* Designed logic to handle unseen users and books (cold start handling)

Each component is implemented modularly to support future production deployment.

---

## 📊 Dataset

The project uses the **Book-Crossing Dataset**, a publicly available dataset containing explicit user ratings for books.

Dataset components:

* Users (`User-ID`)
* Books (`ISBN`)
* Ratings (`Book-Rating`, scale 0–10)

Directory structure:

```
data/
├── raw/
│   ├── books.csv
│   ├── users.csv
│   └── ratings.csv
└── processed/
```

---

## 🏗️ System Architecture (Planned)

```
Data Ingestion
     ↓
Data Validation & Cleaning
     ↓
Exploratory Data Analysis
     ↓
User–Item Matrix Construction
     ↓
Collaborative Filtering Models
     ↓
Model Evaluation
     ↓
Recommendation Engine
     ↓
API / Dashboard (Phase 2)
```

---

## 🛠 Tech Stack

| Layer                | Tools                                  |
| -------------------- | -------------------------------------- |
| Language             | Python                                 |
| Data Processing      | Pandas, NumPy                          |
| Modeling             | Scikit-learn, SciPy                    |
| Similarity Metrics   | Cosine Similarity, Pearson Correlation |
| Evaluation           | RMSE, MAE, Precision@K, Recall@K       |
| Visualization        | Matplotlib, Seaborn                    |
| API (Planned)        | FastAPI                                |
| Deployment (Planned) | Docker                                 |

---

## 🧩 Skills Demonstrated

* Data ingestion and preprocessing (Pandas, NumPy)
* Handling sparse real-world datasets
* Similarity-based machine learning algorithms
* Feature engineering for recommender systems
* Model evaluation using ranking-based metrics
* Modular ML pipeline design
* Clear technical documentation and progress tracking

---

## 📌 Project Progress Tracker

### Phase 1: Foundation & Data

* [x] Project scoping and system design
* [x] Repository structure setup
* [ ] Download and store raw dataset
* [ ] Data schema inspection
* [ ] Data cleaning and preprocessing
* [ ] Handle missing and invalid ratings
* [ ] Save processed datasets

---

### Phase 2: Exploratory Data Analysis

* [ ] User activity distribution analysis
* [ ] Book popularity distribution analysis
* [ ] Dataset sparsity analysis
* [ ] Rating distribution visualization
* [ ] Cold-start scenario identification

---

### Phase 3: Feature Engineering

* [ ] User–item rating matrix creation
* [ ] Rating normalization
* [ ] Sparse matrix optimization
* [ ] Train–test split strategy

---

### Phase 4: Collaborative Filtering Models

* [ ] User–User collaborative filtering
* [ ] Item–Item collaborative filtering
* [ ] Similarity metric comparison
* [ ] Nearest-neighbor optimization
* [ ] Rating prediction logic

---

### Phase 5: Evaluation Framework

* [ ] RMSE and MAE calculation
* [ ] Precision@K and Recall@K
* [ ] Offline validation strategy
* [ ] Error analysis and tuning

---

### Phase 6: Recommendation Engine

* [ ] Top-N recommendation generation
* [ ] User-specific inference
* [ ] Handling unseen users and books
* [ ] Recommendation explainability

---

### Phase 7: Productionization (Planned – Level 2)

* [ ] Modular pipeline refactoring
* [ ] Model versioning
* [ ] FastAPI prediction service
* [ ] Batch inference pipeline
* [ ] Logging and monitoring
* [ ] Dockerization

---

### Phase 8: Visualization & Dashboard (Optional)

* [ ] Recommendation exploration dashboard
* [ ] Similarity analysis visualizations
* [ ] Popularity vs personalization insights

---

## 🧪 Evaluation Metrics

| Metric      | Purpose                            |
| ----------- | ---------------------------------- |
| RMSE        | Accuracy of rating predictions     |
| MAE         | Robustness to outliers             |
| Precision@K | Relevance of top-K recommendations |
| Recall@K    | Coverage of relevant items         |

---

## ▶️ How to Run (Initial Setup)

```bash
git clone <your-repository-url>
cd book-recommendation-system
python -m venv venv
source venv/bin/activate    # macOS / Linux
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

---

## 📁 Repository Structure

```
.
├── data/
├── notebooks/
├── src/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── features/
│   ├── models/
│   ├── evaluation/
│   └── inference/
├── README.md
└── requirements.txt
```

---

## ✨ What Makes This Project Different

* Built completely from scratch without starter templates
* Focused on ML system design, not just model accuracy
* Uses ranking-based evaluation metrics
* Tracks development progress transparently
* Designed to evolve into a production ML system

---

## 🧠 Interview Talking Points

* Built an end-to-end recommender system from scratch
* Designed for sparse, real-world user interaction data
* Evaluated recommendations using both accuracy and ranking metrics
* Structured the project for scalability and production deployment
* Demonstrated ML engineering decision-making

---

## 👤 Author

**Your Name**
Machine Learning Engineer / Applied Machine Learning
LinkedIn | GitHub

---

## ⭐ Project Status

🚧 **Actively in Development — progress tracked in this README**
