from textblob import TextBlob

def analyze_sentiment(title: str) -> str:
    analysis = TextBlob(title)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'