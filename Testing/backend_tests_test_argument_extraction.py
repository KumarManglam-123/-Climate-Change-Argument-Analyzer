import pytest
from app.services.argument_extraction import extract_arguments

def test_argument_extraction():
    test_text = "Climate change is real and caused by humans. The temperature has risen by 1.1°C since pre-industrial times."
    result = extract_arguments(test_text)
    
    assert isinstance(result, list)
    assert len(result) > 0
    assert "argument_text" in result[0]
    assert "position" in result[0]
    assert "subject" in result[0]