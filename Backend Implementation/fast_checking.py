import openai
import requests
from typing import Dict, List, Tuple
from ..config import settings
from ..utils.api_clients import (
    query_ipcc,
    query_nasa,
    query_scholarly_articles
)

openai.api_key = settings.openai_api_key

def verify_claim(claim_text: str) -> Dict[str, any]:
    """
    Verify a climate-related claim using multiple sources
    Returns a dictionary with verification results
    """
    # Step 1: Check IPCC reports
    ipcc_results = query_ipcc(claim_text)
    
    # Step 2: Check NASA climate data
    nasa_results = query_nasa(claim_text)
    
    # Step 3: Check scholarly articles
    scholarly_results = query_scholarly_articles(claim_text)
    
    # Step 4: Use LLM to synthesize results
    evidence = {
        "supporting": [],
        "contradicting": []
    }
    
    # Process IPCC results
    if ipcc_results:
        for result in ipcc_results:
            if result["relevance"] > 0.7:
                if result["alignment"] == "supporting":
                    evidence["supporting"].append({
                        "source": "IPCC",
                        "reference": result["reference"],
                        "excerpt": result["excerpt"]
                    })
                else:
                    evidence["contradicting"].append({
                        "source": "IPCC",
                        "reference": result["reference"],
                        "excerpt": result["excerpt"]
                    })
    
    # Process NASA results
    if nasa_results:
        for result in nasa_results:
            if result["relevance"] > 0.7:
                if result["alignment"] == "supporting":
                    evidence["supporting"].append({
                        "source": "NASA",
                        "reference": result["reference"],
                        "excerpt": result["excerpt"]
                    })
                else:
                    evidence["contradicting"].append({
                        "source": "NASA",
                        "reference": result["reference"],
                        "excerpt": result["excerpt"]
                    })
    
    # Process scholarly articles
    if scholarly_results:
        for result in scholarly_results:
            if result["relevance"] > 0.7:
                if result["alignment"] == "supporting":
                    evidence["supporting"].append({
                        "source": "Scholarly Article",
                        "reference": result["citation"],
                        "excerpt": result["excerpt"]
                    })
                else:
                    evidence["contradicting"].append({
                        "source": "Scholarly Article",
                        "reference": result["citation"],
                        "excerpt": result["excerpt"]
                    })
    
    # Determine overall status and confidence
    status, confidence = determine_verdict(claim_text, evidence)
    
    return {
        "verification_status": status,
        "confidence_score": confidence,
        "supporting_evidence": evidence["supporting"],
        "contradicting_evidence": evidence["contradicting"]
    }

def determine_verdict(claim_text: str, evidence: Dict) -> Tuple[str, float]:
    """
    Use LLM to determine overall verdict based on collected evidence
    """
    supporting_count = len(evidence["supporting"])
    contradicting_count = len(evidence["contradicting"])
    
    prompt = f"""
    Based on the following evidence, determine if the climate claim is:
    - "verified" (strong supporting evidence)
    - "partially_verified" (some supporting evidence but with caveats)
    - "unverified" (insufficient evidence)
    - "debunked" (strong contradicting evidence)
    Also provide a confidence score between 0 and 1.
    
    Claim: "{claim_text}"
    
    Supporting Evidence ({supporting_count} items):
    {evidence["supporting"]}
    
    Contradicting Evidence ({contradicting_count} items):
    {evidence["contradicting"]}
    
    Return your response in JSON format with keys "verdict" and "confidence".
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a fact-checker."},
                 {"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=200
    )
    
    try:
        result = eval(response.choices[0].message.content)
        return result["verdict"], float(result["confidence"])
    except:
        # Default response if parsing fails
        if supporting_count > contradicting_count:
            return "partially_verified", 0.7
        elif supporting_count == 0 and contradicting_count == 0:
            return "unverified", 0.5
        else:
            return "debunked", 0.8