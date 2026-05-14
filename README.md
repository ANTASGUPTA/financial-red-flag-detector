# 📊 Financial Red Flag Detector

AI-powered SEC filing risk analysis system using NLP, FinBERT, and market reaction validation.

---

# 📌 Project Overview

Financial Red Flag Detector is an AI-driven financial analysis platform that automatically retrieves SEC 10-K filings, extracts risk-related disclosures, performs sentiment analysis using FinBERT, detects financial warning signals, and validates whether market reactions aligned with the detected risks.

The system helps identify:
- financial distress signals
- regulatory risks
- macroeconomic concerns
- litigation exposure
- operational uncertainties
- boilerplate disclosure patterns

The application provides explainable AI outputs through highlighted risky disclosures and historical risk comparisons.

---

# 🚀 Features

✅ SEC EDGAR 10-K Filing Retrieval  
✅ Company Name + Stock Ticker Support  
✅ FinBERT Financial Sentiment Analysis  
✅ Red Flag Keyword Detection  
✅ Historical Filing Comparison  
✅ Boilerplate Similarity Analysis  
✅ Risk Severity Scoring  
✅ Explainable AI Risk Highlights  
✅ Stock Market Reaction Validation  
✅ Prediction Accuracy Tracking  
✅ Interactive Streamlit Dashboard  
✅ CSV Report Export

---

# 🏗️ System Architecture

```text
User Input
   ↓
SEC EDGAR Fetcher
   ↓
10-K Filing Downloader
   ↓
Risk Extraction
   ↓
NLP Processing
   ↓
FinBERT Sentiment Analysis
   ↓
Red Flag Detection
   ↓
Risk Scoring Engine
   ↓
Historical Comparison
   ↓
Market Reaction Validation
   ↓
Streamlit Dashboard
```
---

# 🛠️ Technology Stack

## Programming & Backend
- Python 3
- Pandas
- NumPy

## NLP & AI
- FinBERT
- HuggingFace Transformers
- NLTK

## Financial Data Sources
- SEC EDGAR API
- yFinance

## Machine Learning & Analytics
- Scikit-learn
- Cosine Similarity
- Sentiment Analysis

## Visualization & Dashboard
- Streamlit
- Plotly

## Other Libraries
- BeautifulSoup
- Requests

---

# 📂 Project Structure

```text
financial_red_flag_detector/
│
├── app.py
├── requirements.txt
├── README.md
│
├── utils/
│   ├── sec_fetcher.py
│   ├── historical_analysis.py
│   ├── stock_analysis.py
│   ├── similarity_analysis.py
│   ├── red_flag_detector.py
│   ├── finbert_model.py
│
├── data/
│   ├── filings/
│   ├── historical/
│
├── assets/
│   ├── architecture.png
│   ├── screenshots/
```
---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/financial_red_flag_detector.git
```

## 2. Navigate Into Project Folder

```bash
cd financial_red_flag_detector
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Application

```bash
streamlit run app.py
```

---

# 📈 Example Supported Companies

- AAPL
- GOOGL
- META
- TSLA
- AMZN
- MSFT
- NVDA
- PFG

---

# 📊 Dashboard Components

- Historical Risk Score Trends
- Boilerplate Similarity Analysis
- Critical Risk Detection
- Market Reaction Validation
- Prediction Accuracy
- Explainable AI Risk Highlights
- CSV Report Export

---

# 📉 Market Reaction Validation

The application compares:
- AI-predicted financial risk interpretation
vs
- actual stock market movement after SEC filing release.

This enables evaluation of whether filing-based risk signals aligned with real investor behavior.

---

# 🔮 Future Improvements

- Earnings call transcript analysis
- News sentiment integration
- Advanced ML forecasting
- Real-time SEC monitoring
- Portfolio-level risk scoring
- Multi-company comparison dashboard

---

# 👨‍💻 Author

Antas Gupta  
MS Computer Science (AI Specialization)  
Binghamton University

---

# 📜 License

This project is intended for academic and educational purposes.