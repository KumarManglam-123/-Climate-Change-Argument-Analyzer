import openai
import nltk
from typing import List, Dict, Any
from ..config import settings
from ..utils.helpers import clean_text

nltk.download('punkt')

openai.api_key = settings.openai_api_key

def extract_arguments(text: str) -> List[Dict[str, Any]]:
    """
    Extract individual arguments from debate text using LLM
    """
    cleaned_text = clean_text(text)
    
    prompt = f"""
    Analyze the following climate change debate text and extract individual arguments or claims.
    For each argument, identify the position (pro-climate action, neutral, or skeptical) and the main subject.
    Return the results in JSON format with the following keys for each argument:
    - "argument_text": the exact text of the argument
    - "position": one of "pro", "neutral", "skeptical"
    - "subject": the main topic (e.g., "temperature rise", "economic impact", "scientific consensus")
    
    Debate text:
    {cleaned_text}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a debate analyst."},
                 {"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2000
    )
    
    try:
        arguments = eval(response.choices[0].message.content)
        return arguments
    except:
        # Fallback to simpler extraction if JSON parsing fails
        sentences = nltk.sent_tokenize(cleaned_text)
        return [{"argument_text": s, "position": "neutral", "subject": "unknown"} for s in sentences]