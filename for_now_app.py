from utils.sec_fetcher import download_10k
from utils.extractor import extract_sections
from utils.nlp_processor import split_into_sentences
from utils.finbert_model import analyze_sentiment
from utils.red_flag_detector import detect_red_flags
from utils.risk_scoring import calculate_risk_score

filepath = download_10k("AAPL")

sections = extract_sections(filepath)

risk_text = sections['risk_factors']

sentences = split_into_sentences(risk_text)

analysis_results = []

print("\n===== RED FLAG ANALYSIS =====\n")

for sentence in sentences[:15]:

    sentiment = analyze_sentiment(sentence)

    flags = detect_red_flags(sentence)

    analysis_results.append({
        "sentence": sentence,
        "sentiment": sentiment,
        "flags": flags
    })

    print(f"Sentence: {sentence}\n")

    print(f"Sentiment: {sentiment['label']}")
    print(f"Confidence: {sentiment['score']}")

    if flags:
        print(f"Red Flags Detected: {flags}")
    else:
        print("Red Flags Detected: None")

    print("\n" + "-" * 80 + "\n")

overall_risk_score = calculate_risk_score(analysis_results)

print("\n===== OVERALL COMPANY RISK SCORE =====\n")

print(f"Risk Score: {overall_risk_score}/100")