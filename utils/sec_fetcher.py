import requests
import os

HEADERS = {
    "User-Agent": "Antas Gupta agupta16@binghamton.edu",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "application/json",
    "Connection": "keep-alive"
}


def get_cik_from_ticker(ticker):

    url = "https://www.sec.gov/files/company_tickers.json"

    response = requests.get(url, headers=HEADERS)

    data = response.json()

    ticker = ticker.upper().strip()

    for company in data.values():

        company_ticker = company['ticker'].upper()
        company_name = company['title'].upper()

        if (
            company_ticker == ticker
            or company_name == ticker
        ):

            cik = str(company['cik_str']).zfill(10)

            return cik

    return None


def get_latest_10k_url(ticker):

    cik = get_cik_from_ticker(ticker)

    if not cik:
        return None

    submissions_url = (
        f"https://data.sec.gov/submissions/"
        f"CIK{str(cik).zfill(10)}.json"
    )

    response = requests.get(
        submissions_url,
        headers=HEADERS
    )

    filings = response.json()

    recent = filings['filings']['recent']

    forms = recent['form']
    accession_numbers = recent['accessionNumber']
    primary_documents = recent['primaryDocument']

    for i in range(len(forms)):

        if forms[i] == '10-K':

            accession = accession_numbers[i].replace("-", "")
            document = primary_documents[i]

            filing_url = (
                f"https://www.sec.gov/Archives/edgar/data/"
                f"{int(cik)}/{accession}/{document}"
            )

            return filing_url

    return None


def download_10k(ticker):

    url = get_latest_10k_url(ticker)

    if not url:
        return None

    response = requests.get(url, headers=HEADERS)

    os.makedirs("data/filings", exist_ok=True)

    filepath = f"data/filings/{ticker}.html"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(response.text)

    return filepath


def get_multiple_10k_urls(ticker, limit=3):

    cik = get_cik_from_ticker(ticker)

    if not cik:
        print("CIK not found")
        return []

    submissions_url = (
        f"https://data.sec.gov/submissions/"
        f"CIK{str(cik).zfill(10)}.json"
    )

    print(submissions_url)

    try:

        response = requests.get(
            submissions_url,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code != 200:
            print("SEC request failed:", response.status_code)
            return []

        filings = response.json()

    except Exception as e:

        print("Error fetching SEC filings:", e)

        return []

    recent = filings['filings']['recent']

    forms = recent['form']
    accession_numbers = recent['accessionNumber']
    primary_documents = recent['primaryDocument']
    filing_dates = recent['filingDate']

    urls = []

    for i in range(len(forms)):

        if forms[i] == '10-K':

            accession = accession_numbers[i].replace("-", "")
            document = primary_documents[i]

            filing_url = (
                f"https://www.sec.gov/Archives/edgar/data/"
                f"{int(cik)}/{accession}/{document}"
            )

            urls.append({
                "date": filing_dates[i],
                "url": filing_url
            })

        if len(urls) >= limit:
            break

    return urls


def get_company_name(ticker):

    url = "https://www.sec.gov/files/company_tickers.json"

    response = requests.get(url, headers=HEADERS)

    data = response.json()

    ticker = ticker.upper().strip()

    for company in data.values():

        company_ticker = company['ticker'].upper()
        company_name = company['title'].upper()

        if (
            company_ticker == ticker
            or company_name == ticker
        ):

            return company['title']

    return ticker
