#Debugging the sentiment.py code because it isnt printing the desired reults

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

sample = [
    {"character": "NEO",      "line": "I know kung fu."},
    {"character": "MORPHEUS","line": "This is amazing! I love it."},
    {"character": "AGENT",    "line": "You’re under arrest, punk."}
]

print("Running sentiment test on", len(sample), "entries\n")

for idx, entry in enumerate(sample, start=1):
    text = entry["line"]
    print(f"Entry {idx}: '{text}'")               
    scores = analyzer.polarity_scores(text)       
    print("  Full scores:", scores)               
    compound = scores["compound"]
    print("  Compound score:", compound, "\n")    # debug the one we care about

print("Test complete.")