from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class MisinfoRequest(BaseModel):
    text: str

# Emotional language patterns
EMOTIONAL_PATTERNS = {
    'high': [
        'shocking', 'breaking', 'exposed', 'truth', 'conspiracy', 'revealed',
        'horrible', 'terrifying', 'incredible', 'unbelievable', 'mind-blowing',
        'devastating', 'catastrophic', 'huge', 'massive', 'explosive',
        'never seen before', 'first time', 'exclusive', 'secret', 'hidden'
    ],
    'medium': [
        'amazing', 'incredible', 'surprising', 'shocking', 'frightening',
        'scary', 'alarming', 'concerned', 'worried', 'angry', 'furious',
        'outraged', 'upset', 'terrible', 'awful', 'dreadful'
    ],
    'sensational': [
        'you won\'t believe', 'what they don\'t want you to know',
        'the truth about', 'they are hiding', 'media won\'t tell you',
        'breaking news', 'exclusive report', 'leaked', 'whistleblower',
        'we must warn you', 'important message', 'urgent news'
    ]
}

# Misinformation claim patterns
CLAIM_PATTERNS = {
    'unsupported': [
        'according to anonymous', 'sources say', 'rumor has it',
        'people are saying', 'everyone knows', 'it\'s common knowledge',
        'they say', 'they don\'t want you to know'
    ],
    'conspiracy': [
        'cover-up', 'conspiracy', 'hidden agenda', 'the truth is',
        'they are lying', 'they are hiding', 'government hiding',
        'big pharma', 'mainstream media', 'the establishment'
    ]
}

@router.post("/analyze")
async def analyze_misinformation(request: MisinfoRequest):
    try:
        if not request.text or len(request.text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Text must be at least 10 characters long"
            )
        
        text_lower = request.text.lower()
        suspicious_elements = []
        risk_score = 0.0
        
        # Check for emotional language
        emotional_matches = []
        for category, patterns in EMOTIONAL_PATTERNS.items():
            for pattern in patterns:
                if pattern in text_lower:
                    emotional_matches.append({
                        'word': pattern,
                        'category': f"Emotional language ({category})"
                    })
                    if category == 'high':
                        risk_score += 0.20
                    elif category == 'medium':
                        risk_score += 0.10
                    else:
                        risk_score += 0.15
        
        # Check for sensationalism
        sensational_matches = []
        for pattern in EMOTIONAL_PATTERNS['sensational']:
            if pattern in text_lower:
                sensational_matches.append({
                    'word': pattern,
                    'category': 'Sensationalism'
                })
                risk_score += 0.15
        
        # Check for unsupported claims
        unsupported_matches = []
        for pattern in CLAIM_PATTERNS['unsupported']:
            if pattern in text_lower:
                unsupported_matches.append({
                    'word': pattern,
                    'category': 'Unsupported claim'
                })
                risk_score += 0.15
        
        # Check for conspiracy language
        conspiracy_matches = []
        for pattern in CLAIM_PATTERNS['conspiracy']:
            if pattern in text_lower:
                conspiracy_matches.append({
                    'word': pattern,
                    'category': 'Conspiracy language'
                })
                risk_score += 0.20
        
        # Combine all suspicious elements
        suspicious_elements = emotional_matches + sensational_matches + unsupported_matches + conspiracy_matches
        
        # Cap risk score at 0.95
        risk_score = min(0.95, risk_score)
        
        # Determine risk level
        if risk_score >= 0.6:
            risk_level = 'High'
        elif risk_score >= 0.3:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        # Generate explanations
        explanations = []
        if risk_level == 'High':
            explanations.append("This content contains strong indicators of misinformation.")
        elif risk_level == 'Medium':
            explanations.append("This content shows some suspicious patterns that require verification.")
        else:
            explanations.append("No significant misinformation indicators were detected.")
        
        if emotional_matches:
            explanations.append(f"Contains emotionally charged language: {len(emotional_matches)} instances found")
        if sensational_matches:
            explanations.append("Uses sensationalism to grab attention")
        if unsupported_matches:
            explanations.append("Makes claims without providing credible sources")
        if conspiracy_matches:
            explanations.append("Uses conspiracy-related language")
        
        if risk_level in ['High', 'Medium']:
            explanations.append("Always verify information from multiple trusted sources before sharing.")
        
        # Generate recommendations
        recommendations = []
        if risk_level in ['High', 'Medium']:
            recommendations.append("Verify this information with official sources")
            recommendations.append("Check the credibility of the source")
            recommendations.append("Look for supporting evidence from multiple reliable sources")
            recommendations.append("Use fact-checking websites like Snopes, FactCheck.org, or AfricaCheck")
            recommendations.append("Do not share content without verification")
            if conspiracy_matches:
                recommendations.append("Be skeptical of conspiracy theories - they often lack evidence")
            if unsupported_matches:
                recommendations.append("Look for specific sources and evidence, not anonymous claims")
        
        recommendations.append("Think critically about emotional language designed to trigger a reaction")
        recommendations.append("Check the date of the information - old news may be out of context")
        
        return {
            'risk_level': risk_level,
            'confidence_score': round(risk_score, 2),
            'scam_probability': round(risk_score, 2),
            'suspicious_elements': suspicious_elements[:10],
            'explanation': explanations,
            'recommendations': recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
