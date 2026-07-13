from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class MisinfoRequest(BaseModel):
    text: str

@router.post("/analyze")
async def analyze_misinformation(request: MisinfoRequest):
    """
    Analyze text for misinformation
    """
    try:
        if not request.text or len(request.text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Text must be at least 10 characters long"
            )
        
        # Simple analysis
        text_lower = request.text.lower()
        emotional_indicators = []
        
        emotional_words = [
            ('shocking', 'Sensationalism'), 
            ('breaking', 'Sensationalism'),
            ('truth', 'Emotional language'),
            ('exposed', 'Emotional language'),
            ('conspiracy', 'Conspiracy indicator')
        ]
        
        for word, category in emotional_words:
            if word in text_lower:
                emotional_indicators.append({
                    'word': word,
                    'category': category
                })
        
        risk_level = 'High' if len(emotional_indicators) > 2 else 'Medium' if len(emotional_indicators) > 0 else 'Low'
        
        return {
            'risk_level': risk_level,
            'suspicious_elements': emotional_indicators,
            'explanation': [
                f"Found {len(emotional_indicators)} emotional indicators.",
                "Always verify information from multiple sources."
            ],
            'recommendations': [
                "Check the source of the information",
                "Verify with official sources",
                "Look for fact-checking websites"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
