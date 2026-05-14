from utils.sec_fetcher import HEADERS
from utils.extractor import extract_sections
from utils.nlp_processor import split_into_sentences
from utils.finbert_model import analyze_sentiment
from utils.red_flag_detector import detect_red_flags
from utils.risk_scoring import calculate_risk_score

import requests
import os


def download_filing(url, filename):

    response = requests.get(url, headers=HEADERS)

    os.makedirs("data/historical", exist_ok=True)

    filepath = f"data/historical/{filename}.html"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(response.text)

    return filepath


def analyze_filing(filepath):

    sections = extract_sections(filepath)

    risk_text = sections['risk_factors']

    sentences = split_into_sentences(risk_text)

    results = []

    risky_sentences = []

    for sentence in sentences[:15]:

        sentiment = analyze_sentiment(sentence)

        flags = detect_red_flags(sentence)

        results.append({
            "sentence": sentence,
            "sentiment": sentiment,
            "flags": flags
        })

        # =========================
        # SEVERITY SCORING
        # =========================

        severity = 0

        if sentiment['label'].lower() == 'negative':
            severity += 2

        severity += len(flags)

        if severity >= 2:

            risky_sentences.append({
                "sentence": sentence,
                "sentiment": sentiment['label'],
                "flags": flags,
                "severity": severity
            })

    score = calculate_risk_score(results)

    # =========================
    # SORT BY SEVERITY
    # =========================

    sorted_risks = sorted(
        risky_sentences,
        key=lambda x: x['severity'],
        reverse=True
    )

    return {
        "score": score,
        "risk_text": risk_text,
        "risky_sentences": sorted_risks[:3]
    }