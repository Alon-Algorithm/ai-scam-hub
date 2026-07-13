from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from app.services.nlp_service import ScamDetectionService

router = APIRouter()
scam_service = ScamDetectionService()

class TextAnalysisRequest(BaseModel):
    text: str
    context: Optional[str] = None

@router.post("/analyze")
async def analyze_text(request: TextAnalysisRequest):
    try:
        if not request.text or len(request.text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Text must be at least 10 characters long"
            )
        
        results = scam_service.analyze_text(request.text)
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
