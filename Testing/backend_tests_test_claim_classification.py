import pytest
from app.services.claim_classification import classify_claim, CATEGORIES

def test_claim_classification():
    test_claims = [
        ("Global temperatures are rising due to greenhouse gas emissions", "scientific"),
        ("Climate policies will hurt economic growth", "economic"),
        ("We need international cooperation to address climate change", "political")
    ]
    
    for claim_text, expected_category in test_claims:
        result = classify_claim(claim_text)
        assert result["category"] in CATEGORIES
        if expected_category in CATEGORIES:
            assert result["category"] == expected_category