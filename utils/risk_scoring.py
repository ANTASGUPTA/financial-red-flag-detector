def calculate_risk_score(results):

    total_score = 0

    for item in results:

        sentiment = item['sentiment']
        flags = item['flags']

        sentence_score = 0

        confidence = sentiment['score']

        # Negative sentiment
        if sentiment['label'] == 'negative':
            sentence_score += 10 * confidence

        # Neutral but uncertain
        elif sentiment['label'] == 'neutral':
            sentence_score += 3 * confidence

        # Red flag contribution
        unique_flags = len(set(flags))

        sentence_score += unique_flags * 2

        total_score += sentence_score

    # Normalize by sentence count
    avg_score = total_score / len(results)

    # Scale to 0–100
    normalized_score = min(round(avg_score * 5, 2), 100)

    return normalized_score