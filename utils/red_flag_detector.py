HEDGING_WORDS = [

    # Financial risks
    "risk",
    "risks",
    "loss",
    "decline",
    "debt",
    "recession",
    "inflation",
    "fluctuation",
    "uncertainty",
    "volatility",

    # Legal / regulatory risks
    "lawsuit",
    "litigation",
    "regulation",
    "regulatory",
    "compliance",
    "penalty",
    "investigation",
    "antitrust",

    # Technology / cyber risks
    "cybersecurity",
    "data breach",
    "privacy",
    "security incident",
    "ai regulation",

    # Business risks
    "competition",
    "market pressure",
    "supply chain",
    "operational disruption",

    # Warning language
    "may",
    "might",
    "could",
    "uncertain",
    "possibly",
    "subject to",
    "adversely",
    "material adverse effect",
    "cannot guarantee",
    "not be able to"
]


def detect_red_flags(sentence):

    sentence_lower = sentence.lower()

    detected_flags = []

    for word in HEDGING_WORDS:

        if word in sentence_lower:
            detected_flags.append(word)

    return detected_flags