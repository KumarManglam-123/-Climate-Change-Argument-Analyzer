from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ClaimBase(BaseModel):
    claim_text: str
    category: Optional[str] = None
    verification_status: Optional[str] = None
    confidence_score: Optional[float] = None
    supporting_evidence: Optional[List[Dict[str, Any]]] = []
    contradicting_evidence: Optional[List[Dict[str, Any]]] = []

class DebateAnalysisCreate(BaseModel):
    original_text: str

class DebateAnalysis(DebateAnalysisCreate):
    id: int
    analysis_results: List[ClaimBase]
    summary: Optional[str] = None
    
    class Config:
        orm_mode = True