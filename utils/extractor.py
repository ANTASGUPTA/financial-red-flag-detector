from bs4 import BeautifulSoup
import re
import warnings
from bs4 import XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_real_section(text, start_pattern, end_pattern):
    matches = list(
        re.finditer(start_pattern, text, re.IGNORECASE)
    )

    if len(matches) < 2:
        return "Not found"

    # Usually second occurrence is real section after TOC
    start = matches[1].start()

    end_match = re.search(
        end_pattern,
        text[start:],
        re.IGNORECASE
    )

    if not end_match:
        return "Not found"

    end = start + end_match.start()

    section = text[start:end]

    return section[:15000]


def extract_sections(filepath):

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")

    text = soup.get_text(separator=" ")

    text = clean_text(text)

    risk_text = extract_real_section(
        text,
        r"Item\s+1A\.?\s+Risk Factors",
        r"Item\s+1B|Item\s+2"
    )

    mdna_text = extract_real_section(
        text,
        r"Item\s+7\.?\s+Management.?s Discussion and Analysis",
        r"Item\s+7A|Item\s+8"
    )

    return {
        "risk_factors": risk_text,
        "mdna": mdna_text
    }