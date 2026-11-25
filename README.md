# Financial Red Flag Detector

A Streamlit app that analyzes SEC 10-K filings for financial risk signals using FinBERT, keyword red-flag detection, and historical filing comparison.

**Stack:** Python, Streamlit, Plotly, Hugging Face Transformers (FinBERT), scikit-learn, SEC EDGAR, yFinance

## What it does

Given a company name or ticker, the app:

1. Resolves the company to a CIK and fetches its latest 10-K from SEC EDGAR.
2. Extracts the Risk Factors section.
3. Scores each sentence with FinBERT sentiment and a red-flag keyword list.
4. Produces an explainable 0–100 risk score with the top risky sentences highlighted.
5. Compares the filing against prior years with TF-IDF cosine similarity to surface boilerplate and year-over-year changes.
6. Optionally checks stock price movement around the filing date.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The first run downloads the FinBERT model from Hugging Face.

## Project layout

```
app.py                   Streamlit entry point
utils/
  sec_fetcher.py         SEC EDGAR company lookup and 10-K retrieval
  extractor.py           Risk Factors section extraction
  nlp_processor.py       Sentence splitting and cleaning
  finbert_model.py       FinBERT sentiment scoring
  red_flag_detector.py   Keyword and phrase detection
  risk_scoring.py        Risk score aggregation
  similarity_analysis.py TF-IDF boilerplate comparison
  stock_analysis.py      yFinance price checks
  historical_analysis.py Multi-year comparison
data/
  filings/               Cached filings
  historical/            Historical filings
```

## Risk score

Each sentence contributes:

- `10 × confidence` if FinBERT labels it negative
- `3 × confidence` if FinBERT labels it neutral
- `2` per unique red-flag keyword

The average sentence score is scaled by 5 and capped at 100. The score is a heuristic for triage, not a calibrated probability.

## Notes and limitations

- FinBERT is a sentiment model, not a financial-risk classifier; the score combines sentiment, keyword hits, and filing similarity.
- SEC EDGAR requires a descriptive `User-Agent`. Update `HEADERS` in `utils/sec_fetcher.py` with your own contact email before deploying.
- Filings are cached under `data/` to avoid repeated requests.
- This is a research and portfolio project, not investment advice.

## Next steps

- Add earnings-call transcript analysis.
- Add news sentiment.
- Add a multi-company comparison view.
- Replace the heuristic score with a supervised model trained on labeled risk disclosures.
