from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def analyze_dialogues(dialogues):
    
    analyzer = SentimentIntensityAnalyzer()
    results = []
    
    for entry in dialogues:
        text = entry["line"]
        # Compute a compound sentiment score between -1 (negative) and +1 (positive)
        scores = analyzer.polarity_scores(text)
        compound = scores["compound"]
        
        enriched = {
            "character": entry["character"],
            "line":      text,
            "sentiment_score": compound,
        }
        results.append(enriched)
        
    return results
    
    
if __name__ == "__main__":
    # ---- Sample data to test your function ----
    sample = [
        {"character": "NEO",      "line": "I know kung fu."},
        {"character": "MORPHEUS","line": "Welcome to the real world."}
    ]

   
    scored = analyze_dialogues(sample)


    for s in scored:
        print(s)