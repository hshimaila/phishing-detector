"""
Text preprocessing pipeline using SpaCy.

What this does step by step:
1. Lowercases everything
2. Removes punctuation and numbers
3. Removes stopwords (common words like "the", "is", "at" that add no signal)
4. Lemmatizes words (running → run, accounts → account)
   This helps the model treat similar words as the same thing.
"""

import spacy
import re
import nltk

# Download required NLTK data (only needed once)
nltk.download("stopwords", quiet=True)

# Load the SpaCy English model
# en_core_web_sm is small but good enough for our use case
nlp = spacy.load("en_core_web_sm")


def clean_text(text: str) -> str:
    """
    Takes raw email text and returns a cleaned, normalized string.
    
    Example:
        Input:  "URGENT!! Click HERE to verify your Account NOW!!!"
        Output: "urgent click verify account"
    """
    if not text or not isinstance(text, str):
        return ""

    # Step 1: Lowercase
    text = text.lower()

    # Step 2: Remove URLs (we handle URLs separately)
    text = re.sub(r'http\S+|www\S+', ' urltoken ', text)

    # Step 3: Remove email addresses
    text = re.sub(r'\S+@\S+', ' emailtoken ', text)

    # Step 4: Remove special characters and digits, keep only letters
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # Step 5: SpaCy processing - lemmatize and remove stopwords
    doc = nlp(text)
    tokens = [
        token.lemma_          # lemmatized form
        for token in doc
        if not token.is_stop   # remove stopwords
        and not token.is_punct # remove punctuation
        and len(token.text) > 2 # remove very short tokens
    ]

    # Step 6: Join back into a string
    cleaned = " ".join(tokens)

    return cleaned


def extract_phishing_signals(text: str) -> dict:
    """
    Rule-based extraction of known phishing signals.
    These become additional features for the ML model.
    
    Returns a dict of binary flags (1 = signal present, 0 = not).
    """
    text_lower = text.lower()

    signals = {
        # Urgency language
        "has_urgency":        int(any(w in text_lower for w in ["urgent", "immediately", "expires", "limited time", "act now"])),
        # Threat language
        "has_threat":         int(any(w in text_lower for w in ["suspended", "deleted", "terminated", "legal action", "banned"])),
        # Money/prize bait
        "has_money_bait":     int(any(w in text_lower for w in ["won", "prize", "gift card", "free", "reward", "cash"])),
        # Credential harvesting
        "has_credential_ask": int(any(w in text_lower for w in ["password", "ssn", "social security", "credit card", "verify identity"])),
        # Impersonation clues
        "has_impersonation":  int(any(w in text_lower for w in ["paypal", "netflix", "amazon", "irs", "bank", "apple", "microsoft"])),
        # URL in text
        "has_url":            int("http" in text_lower or "www" in text_lower or "click here" in text_lower),
        # Excessive punctuation (common in phishing)
        "exclamation_count":  min(text.count("!"), 10),  # cap at 10
        "caps_ratio":         round(sum(1 for c in text if c.isupper()) / max(len(text), 1), 2),
    }

    return signals