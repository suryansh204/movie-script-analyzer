DROP TABLE IF EXISTS dialogues;
DROP TABLE IF EXISTS scenes;

CREATE TABLE scenes (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  scene_number  INTEGER NOT NULL,
  header        TEXT NOT NULL
);

CREATE TABLE dialogues (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  scene_id        INTEGER NOT NULL,
  character       TEXT  NOT NULL,
  line            TEXT  NOT NULL,
  sentiment_score REAL  NOT NULL,
  FOREIGN KEY(scene_id) REFERENCES scenes(id)
);