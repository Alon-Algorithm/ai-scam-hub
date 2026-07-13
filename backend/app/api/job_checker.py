from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

class JobAnalysisRequest(BaseModel):
    job_text: str
    company_name: Optional[str] = None

@router.post("/analyze")
async def analyze_job_ad(request: JobAnalysisRequest):
    try:
        if not request.job_text or len(request.job_text.strip()) < 20:
            raise HTTPException(
                status_code=400,
                detail="Job description must be at least 20 characters"
            )
        
        text_lower = request.job_text.lower()
        indicators = []
        
        if any(word in text_lower for word in ['pay', 'fee', 'deposit', 'registration']):
            indicators.append({
                'category': 'upfront_payment',
                'matches': ['pay', 'fee', 'deposit'],
                'score': 0.3
            })
        
        if any(word in text_lower for word in ['r100,000', 'r50,000', 'commission']):
            indicators.append({
                'category': 'unrealistic_salary',
                'matches': ['r100,000', 'r50,000'],
                'score': 0.2
            })
        
        if '@gmail.com' in text_lower or '@yahoo.com' in text_lower:
            indicators.append({
                'category': 'suspicious_email',
                'matches': ['gmail.com', 'yahoo.com'],
                'score': 0.2
            })
        
        risk_level = 'High' if len(indicators) >= 2 else 'Medium' if len(indicators) >= 1 else 'Low'
        
        return {
            'risk_level': risk_level,
            'is_suspicious': risk_level in ['High', 'Medium'],
            'indicators': indicators,
            'explanation': [
                f"This job advertisement shows {len(indicators)} suspicious indicators.",
                "Always research the company before applying."
            ],
            'recommendations': [
                "Research the company thoroughly",
                "Check the company's official website",
                "Be wary of jobs that ask for money upfront",
                "Trust your instincts"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
