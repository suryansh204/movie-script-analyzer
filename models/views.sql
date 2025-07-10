-- 1) Average sentiment & dialogue count per scene

DROP VIEW IF EXISTS scene_sentiment;
CREATE VIEW scene_sentiment AS
SELECT
  s.scene_number,
  s.header,
  ROUND(AVG(d.sentiment_score), 3) AS avg_sentiment,
  COUNT(d.id)               AS line_count
FROM scenes s
JOIN dialogues d ON s.id = d.scene_id
GROUP BY s.id;

-- 2) Total lines & average sentiment per character
DROP VIEW IF EXISTS character_summary;
CREATE VIEW character_summary AS
SELECT
  d.character,
  COUNT(*)                  AS total_lines,
  ROUND(AVG(d.sentiment_score), 3) AS avg_sentiment
FROM dialogues d
GROUP BY d.character
ORDER BY total_lines DESC;

-- 3) Distribution of sentiment categories
DROP VIEW IF EXISTS sentiment_distribution;
CREATE VIEW sentiment_distribution AS
SELECT
  CASE
    WHEN sentiment_score >  0.05 THEN 'positive'
    WHEN sentiment_score < -0.05 THEN 'negative'
    ELSE 'neutral'
  END AS sentiment_category,
  COUNT(*) AS count_lines
FROM dialogues
GROUP BY sentiment_category;