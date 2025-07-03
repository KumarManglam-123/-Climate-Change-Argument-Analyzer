import re
from typing import List, Dict

def clean_text(text: str) -> str:
    """
    Clean and preprocess text for analysis
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove special characters except basic punctuation
    text = re.sub(r'[^\w\s.,;?!-]', '', text)
    return text

def format_verdict(status: str) -> str:
    """
    Convert status codes to human-readable format
    """
    status_map = {
        "verified": "Verified by evidence",
        "partially_verified": "Partially verified",
        "unverified": "Not verified",
        "debunked": "Debunked by evidence"
    }
    return status_map.get(status, "Unknown verification status")