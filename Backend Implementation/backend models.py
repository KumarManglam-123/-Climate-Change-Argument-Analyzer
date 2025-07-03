from sqlalchemy import Column, Integer, String, Float, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DebateAnalysis(Base):
    __tablename__ = "debate_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(String)
    analysis_results = Column(JSON)
    summary = Column(String)
    created_at = Column(String)

class Claim(Base):
    __tablename__ = "claims"
    
    id = Column(Integer, primary_key=True, index=True)
    debate_id = Column(Integer, index=True)
    claim_text = Column(String)
    category = Column(String)
    verification_status = Column(String)
    confidence_score = Column(Float)
    supporting_evidence = Column(JSON)
    contradicting_evidence = Column(JSON)