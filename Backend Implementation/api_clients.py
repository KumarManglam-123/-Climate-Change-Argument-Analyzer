import requests
from typing import List, Dict
from ..config import settings
from crossref_commons.retrieval import get_publication_as_json
from crossref_commons.iterators import iterate_publications_as_json

def query_ipcc(query: str) -> List[Dict]:
    """
    Query IPCC reports for relevant information
    (Mock implementation - in a real system, this would use IPCC API or reports)
    """
    # This is a simplified mock - real implementation would parse actual IPCC reports
    mock_responses = {
        "temperature rise": [
            {
                "excerpt": "Global surface temperature has increased faster since 1970 than in any other 50-year period over at least the last 2000 years.",
                "reference": "IPCC AR6 WG1, Chapter 2",
                "relevance": 0.9,
                "alignment": "supporting"
            }
        ],
        "human influence": [
            {
                "excerpt": "It is unequivocal that human influence has warmed the atmosphere, ocean and land.",
                "reference": "IPCC AR6 WG1, Summary for Policymakers",
                "relevance": 0.95,
                "alignment": "supporting"
            }
        ]
    }
    
    # Simple keyword matching for the mock
    results = []
    for keyword, responses in mock_responses.items():
        if keyword in query.lower():
            results.extend(responses)
    
    return results[:3]  # Return max 3 results

def query_nasa(query: str) -> List[Dict]:
    """
    Query NASA climate data APIs
    """
    # NASA API endpoint for climate data
    base_url = "https://api.nasa.gov/insight_weather/"
    
    # This is a simplified mock - real implementation would use actual NASA APIs
    mock_responses = {
        "co2 levels": [
            {
                "excerpt": "Carbon dioxide levels in the air are at their highest in 650,000 years.",
                "reference": "NASA Global Climate Change: Vital Signs of the Planet",
                "relevance": 0.85,
                "alignment": "supporting"
            }
        ],
        "sea level": [
            {
                "excerpt": "Global sea level rose about 8 inches in the last century, and the rate has doubled in the last two decades.",
                "reference": "NASA Sea Level Change Portal",
                "relevance": 0.88,
                "alignment": "supporting"
            }
        ]
    }
    
    # Simple keyword matching for the mock
    results = []
    for keyword, responses in mock_responses.items():
        if keyword in query.lower():
            results.extend(responses)
    
    return results[:3]  # Return max 3 results

def query_scholarly_articles(query: str, limit: int = 3) -> List[Dict]:
    """
    Query scholarly articles using CrossRef API
    """
    try:
        results = []
        filters = {"from-pub-date": "2010", "type": "journal-article"}
        
        for item in iterate_publications_as_json(query, filter=filters, rows=limit):
            title = item.get("title", [""])[0]
            authors = ", ".join([a.get("given", "") + " " + a.get("family", "") 
                               for a in item.get("author", [])[:3]])
            journal = item.get("container-title", [""])[0]
            year = item.get("published", {}).get("date-parts", [[None]])[0][0]
            doi = item.get("DOI", "")
            
            # Mock relevance and alignment for the demo
            results.append({
                "citation": f"{authors} ({year}). {title}. {journal}",
                "excerpt": f"This study provides evidence supporting that {query}",
                "relevance": 0.8,
                "alignment": "supporting",
                "doi": doi
            })
        
        return results
    except Exception as e:
        print(f"Error querying scholarly articles: {e}")
        return []