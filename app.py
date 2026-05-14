import streamlit as st
import pandas as pd
import plotly.express as px
import os

os.environ["TRANSFORMERS_VERBOSITY"] = "error"

from utils.sec_fetcher import (
    get_multiple_10k_urls,
    get_company_name
)

from utils.historical_analysis import (
    download_filing,
    analyze_filing
)

from utils.similarity_analysis import compute_similarity
from utils.stock_analysis import get_stock_reaction

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Financial Red Flag Detector",
    layout="wide"
)

# =========================
# TITLE
# =========================

st.title("📊 Financial Red Flag Detector")

st.write(
    "AI-powered SEC filing risk analysis using NLP and FinBERT"
)

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.header("📌 Project Overview")

    st.write(
        """
        AI-powered SEC filing analysis system
        using FinBERT and NLP techniques.
        """
    )

    st.subheader("🔧 Technologies Used")

    st.markdown("""
    - FinBERT
    - SEC EDGAR API
    - Streamlit
    - Plotly
    - yFinance
    - NLP & Sentiment Analysis
    """)

    st.subheader("📈 Supported Inputs")

    st.write(
        "Stock tickers or company names"
    )

    st.code(
        "AAPL\nGOOGL\nMETA\nTSLA\nPFG"
    )

# =========================
# INPUT
# =========================

ticker = st.text_input(
    "Enter Stock Ticker or Company Name",
    value="AAPL"
)

company_name = get_company_name(ticker)

st.markdown(
    f"### 🏢 {company_name} ({ticker.upper()})"
)

# =========================
# ANALYZE BUTTON
# =========================

if st.button("Analyze"):

    with st.spinner(
        "Fetching SEC filings and running AI analysis..."
    ):

        filings = get_multiple_10k_urls(ticker)

    # =========================
    # INVALID TICKER HANDLING
    # =========================

    if not filings:

        st.error(
            f"""
    ❌ Unable to find SEC 10-K filings for:
    {ticker.upper()}

    Possible reasons:
    - Company may not be publicly traded
    - SEC filings may not exist
    - Invalid ticker/company name entered
            """
        )

        st.info(
            """
    💡 Example supported companies:

    AAPL, GOOGL, META, TSLA, AMZN, MSFT, NVDA
            """
        )

        st.stop()

    analysis_results = []

    progress_text = st.empty()

    # =========================
    # PROCESS FILINGS
    # =========================

    for filing in filings:

        date = filing['date']

        progress_text.info(
            f"Processing filing: {date}"
        )

        filepath = download_filing(
            filing['url'],
            date
        )

        result = analyze_filing(filepath)

        stock_reaction = get_stock_reaction(
            ticker,
            date
        )

        analysis_results.append({
            "date": date,
            "risk_score": result['score'],
            "risk_text": result['risk_text'],
            "risky_sentences": result['risky_sentences'],
            "stock_reaction": stock_reaction
        })

    progress_text.success(
        "✅ Analysis completed successfully!"
    )

    # =========================
    # HISTORICAL RISK SCORES
    # =========================

    st.divider()

    st.subheader("📈 Historical Risk Scores")

    df = pd.DataFrame(analysis_results)

    fig = px.line(
        df,
        x="date",
        y="risk_score",
        markers=True,
        title=f"{ticker.upper()} Historical Risk Scores"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.dataframe(
        df[['date', 'risk_score']],
        width="stretch"
    )

    # =========================
    # BOILERPLATE SIMILARITY
    # =========================

    st.divider()

    st.subheader("📄 Boilerplate Similarity")

    similarity_results = []

    for i in range(len(analysis_results) - 1):

        current = analysis_results[i]
        previous = analysis_results[i + 1]

        similarity = compute_similarity(
            current['risk_text'],
            previous['risk_text']
        )

        if similarity is not None:

            similarity_results.append({
                "comparison":
                    f"{current['date']} vs {previous['date']}",
                "similarity": similarity
            })

        else:

            similarity_results.append({
                "comparison":
                    f"{current['date']} vs {previous['date']}",
                "similarity": "Unavailable"
            })

    similarity_df = pd.DataFrame(similarity_results)

    st.dataframe(
        similarity_df,
        width="stretch"
    )

    valid_similarity = similarity_df[
        similarity_df['similarity'] != 'Unavailable'
    ]

    if not valid_similarity.empty:

        similarity_fig = px.bar(
            valid_similarity,
            x="comparison",
            y="similarity",
            title="Boilerplate Similarity Across Years"
        )

        st.plotly_chart(
            similarity_fig,
            width="stretch"
        )

    # =========================
    # MARKET REACTION VALIDATION
    # =========================

    st.divider()

    st.subheader("📉 Market Reaction Validation")

    validation_rows = []

    correct_predictions = 0
    total_predictions = 0

    for row in analysis_results:

        reaction = row['stock_reaction']

        if reaction is not None:

            actual_change = reaction['change_percent']

            risk_score = row['risk_score']

            # AI Prediction Logic

            if risk_score >= 25:
                predicted = "Negative"

            elif risk_score >= 15:
                predicted = "Neutral"

            else:
                predicted = "Positive"

            # Actual Market Reaction

            if actual_change <= -2:
                actual = "Negative"

            elif actual_change < 2:
                actual = "Neutral"

            else:
                actual = "Positive"

            correct = predicted == actual

            if correct:
                correct_predictions += 1

            total_predictions += 1

            validation_rows.append({
                "date": row['date'],
                "risk_score": round(risk_score, 2),
                "predicted_reaction": predicted,
                "actual_change_percent":
                    f"{round(actual_change, 2)}%",
                "actual_reaction": actual,
                "correct_prediction": correct
            })

    validation_df = pd.DataFrame(validation_rows)

    st.dataframe(
        validation_df,
        width="stretch"
    )

    accuracy = 0

    if total_predictions > 0:

        accuracy = (
            correct_predictions
            / total_predictions
        ) * 100

    # =========================
    # CURRENT RISK SCORE
    # =========================

    st.divider()

    latest_score = analysis_results[0]['risk_score']

    st.subheader("🚨 Current Overall Risk Score")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            label=f"{ticker.upper()} Risk Score",
            value=f"{round(latest_score, 2)}/100"
        )

    with col2:

        st.metric(
            "Prediction Accuracy",
            f"{round(accuracy, 2)}%"
        )

    if latest_score > 70:

        st.error("🔴 High Risk Detected")

    elif latest_score > 40:

        st.warning("🟡 Moderate Risk Detected")

    else:

        st.success("🟢 Low to Moderate Risk")

    # =========================
    # TOP CRITICAL RISKS
    # =========================

    st.divider()

    st.subheader("🚨 Top Critical Risks Detected")

    latest_risky = analysis_results[0]['risky_sentences']

    if latest_risky:

        for item in latest_risky:

            st.warning(
                f"""
Sentence:
{item['sentence']}

Sentiment:
{item['sentiment']}

Risk Flags:
{', '.join(item['flags'])}

Severity Score:
{item['severity']}
"""
            )

    else:

        st.success(
            "No major risky disclosures detected."
        )

    # =========================
    # DOWNLOAD REPORT
    # =========================

    st.divider()

    st.subheader("⬇️ Download Analysis Report")

    report_rows = []

    for row in analysis_results:

        report_rows.append({
            "date": row['date'],
            "risk_score": row['risk_score']
        })

    report_df = pd.DataFrame(report_rows)

    csv = report_df.to_csv(index=False)

    st.download_button(
        label="📥 Download Risk Report CSV",
        data=csv,
        file_name=f"{ticker.upper()}_risk_report.csv",
        mime="text/csv"
    )

# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    "Built using FinBERT, SEC EDGAR API, "
    "Streamlit, Plotly, and yFinance"
)
