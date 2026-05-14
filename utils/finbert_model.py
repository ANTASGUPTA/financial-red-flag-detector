from transformers import pipeline

# Load FinBERT model only once
finbert = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert",
    truncation=True,
    max_length=512
)


def analyze_sentiment(sentence):

    try:

        result = finbert(
            sentence,
            truncation=True,
            max_length=512
        )[0]

        return {
            "label": result['label'],
            "score": round(result['score'], 4)
        }

    except Exception:

        return {
            "label": "neutral",
            "score": 0.0
        }