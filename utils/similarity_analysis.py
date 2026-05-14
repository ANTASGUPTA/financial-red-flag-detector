from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(text1, text2):

    try:

        if not text1.strip() or not text2.strip():
            return None

        vectorizer = TfidfVectorizer(
            stop_words='english'
        )

        tfidf_matrix = vectorizer.fit_transform(
            [text1, text2]
        )

        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )[0][0]

        return round(similarity * 100, 2)

    except Exception:
        return None