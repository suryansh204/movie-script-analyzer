import os
import sys
import sqlite3

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from etl.parse_script   import load_script, split_scenes, parse_scene
from analysis.sentiment import analyze_dialogues


SCRIPT_PATH = os.path.join(PROJECT_ROOT, "data", "PulpFiction.txt")
DB_PATH     = os.path.join(PROJECT_ROOT, "movie_scripts.db")

def load_data(script_filepath):
    text   = load_script(script_filepath)
    scenes = split_scenes(text)

    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    total_dialogues = 0

    for idx, scene in enumerate(scenes, start=1):
        header = scene.split("\n")[0]
        cur.execute(
            "INSERT INTO scenes(scene_number, header) VALUES (?, ?)",
            (idx, header)
        )
        scene_id = cur.lastrowid

        parsed = parse_scene(scene)
        scored = analyze_dialogues(parsed)
        for d in scored:
            cur.execute(
                "INSERT INTO dialogues(scene_id, character, line, sentiment_score)"
                " VALUES (?, ?, ?, ?)",
                (scene_id, d["character"], d["line"], d["sentiment_score"])
            )
            total_dialogues += 1

    conn.commit()
    conn.close()
    print("loaded data to database")

if __name__ == "__main__":
    load_data(SCRIPT_PATH)
