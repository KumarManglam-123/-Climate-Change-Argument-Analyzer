from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import Base
from .config import settings
from .services import (
    analyze_debate,
    get_analysis,
    get_all_analyses
)
from .schemas import DebateAnalysisCreate, DebateAnalysis
import sqlalchemy
from sqlalchemy.orm import sessionmaker

app = FastAPI(title=settings.app_name)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = settings.database_url
engine = sqlalchemy.create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@app.post("/analyze/", response_model=DebateAnalysis)
async def analyze_debate_text(debate: DebateAnalysisCreate):
    db = SessionLocal()
    try:
        return analyze_debate(db, debate.original_text)
    finally:
        db.close()

@app.get("/analysis/{analysis_id}", response_model=DebateAnalysis)
async def get_analysis_by_id(analysis_id: int):
    db = SessionLocal()
    try:
        analysis = get_analysis(db, analysis_id)
        if analysis is None:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return analysis
    finally:
        db.close()

@app.get("/analyses/", response_model=List[DebateAnalysis])
async def list_analyses(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    try:
        analyses = get_all_analyses(db, skip=skip, limit=limit)
        return analyses
    finally:
        db.close()