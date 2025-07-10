# Movie Script Analyzer

A Python-based ETL and analytics pipeline that transforms unstructured film scripts into structured data, performs sentiment analysis, and generates interactive visualizations in Tableau Public.

---

## Project Overview

**Movie Script Analyzer** follows a multi-step process:

1. **Parsing & Structuring**

   * Reads raw screenplay text (e.g., `PulpFiction.txt`) and uses **Python + regex** to extract:

     * **Scenes** (via `INT.`/`EXT.` headers)
     * **Character lines** (uppercase name followed by dialogue)
   * Ensures deterministic, reproducible parsing and gives full control over edge cases.

2. **Sentiment Analysis**

   * Applies **VADER** to score each line from **–1 (negative)** to **+1 (positive)**.
   * Runs locally to avoid API costs and maintain low latency, while offering transparent, auditable scores.

3. **Data Storage & Modeling**

   * Uses **SQLite** with this schema:

     ```sql
     scripts(id, name)
     scenes(id, script_id, scene_number, header)
     dialogues(id, scene_id, character, line, sentiment_score)
     ```
   * Tracks multiple scripts, scene metadata, and linked dialogue entries for easy querying.

4. **Visualization**

   * Exports three key views as CSVs:

     * **`scene_sentiment.csv`**: average sentiment & line count per scene
     * **`character_summary.csv`**: total lines & avg sentiment per character
     * **`sentiment_distribution.csv`**: counts of negative/neutral/positive lines
   * Uses **Tableau Public** to build:

     * **Emotional Arc** line chart
     * **Speaker Activity** bar chart
     * **Tone Breakdown** pie chart

---

## Tech Stack

| Step                   | Technology       | Rationale                                                      |
| ---------------------- | ---------------- | -------------------------------------------------------------- |
| Parsing & ETL          | Python 3, `re`   | Powerful scripting with regex flexibility and reproducibility. |
| Sentiment Analysis     | `vaderSentiment` | Lexicon-based, offline, optimized for conversational text.     |
| Storage & Modeling     | SQLite, SQL      | Zero-config, file-based RDBMS ideal for rapid prototyping.     |
| Visualization          | Tableau Public   | Industry-standard, drag-and-drop BI with free public hosting.  |
| Orchestration (future) | Apache Airflow   | Scalable DAGs for scheduled, idempotent ETL runs.              |

---

## Installation & Usage

```bash
# 1. Clone & enter project
git clone https://github.com/suryansh204/Movie-Script-Analyzer.git
cd Movie-Script-Analyzer

# 2. Create virtualenv & install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Initialize database schema
sqlite3 movie_scripts.db < models/schema.sql

# 4. Parse & load script
python3 etl/parse_script.py      # Parses and loads raw scenes to DB
python3 etl/db_loader.py         # Scores sentiment, populates scenes & dialogues

# 5. Export views for Tableau
bash scripts/export_views.sh      # Dumps CSVs into exports/

# 6. Build & publish dashboard
#    - Import CSVs in Tableau Public
#    - Create Emotional Arc, Speaker Activity, Tone Breakdown
#    - Save workbook to Tableau Public
```

---

## Repository Structure

```text
Movie-Script-Analyzer/
├── analysis/             # Sentiment analysis (VADER)
│   └── sentiment.py
├── data/                 # Raw screenplays
│   └── PulpFiction.txt
├── etl/                  # ETL scripts
│   ├── __init__.py
│   ├── parse_script.py   # Parses scenes & dialogues
│   └── db_loader.py      # Sentiment + DB loader
├── models/               # SQL schema & views
│   ├── schema.sql
│   └── views.sql
├── scripts/              # Utility scripts (e.g., export_views.sh)
├── exports/              # CSV outputs for Tableau
├── movie_scripts.db      # SQLite database file
├── requirements.txt      # Python deps
├── README.md
└── LICENSE
```

---

## 🧩 Challenges & Lessons

* **Regex Complexity**: Hand-rolling patterns for scene headers and dialogue lines required iterative refinement to handle quirks (multiline blocks, parentheticals).
* **Sentiment Granularity**: Short lines often scored neutral by VADER; considered transformer-based models but prioritized speed and transparency.
* **Import Paths**: Packaging `etl/` and `analysis/` for CLI execution led to `__init__.py` modules and `sys.path` adjustments for consistent imports.
* **Data Duplication**: Running loaders risked duplicate rows; solved via `scripts` table + `INSERT OR IGNORE` and optional row-level deletes for idempotency.
* **Visualization Connectivity**: Tableau Public’s lack of SQLite support prompted CSV export scripts for seamless BI integration.

---

## 🚀 Next Steps

1. **Airflow Orchestration**: Automate ETL per-script with DAGs and cleanup tasks.
2. **Advanced NLP**: Incorporate transformer models for nuanced emotion detection.
3. **Interactive Web UI**: Streamlit or Dash front-end to upload scripts, run analysis, and view dashboards dynamically.
4. **Comparative Analysis**: Load multiple films to compare arcs, pacing, and character sentiment profiles.

---
