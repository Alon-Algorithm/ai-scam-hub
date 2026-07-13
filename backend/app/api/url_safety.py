from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from urllib.parse import urlparse

router = APIRouter()

class URLRequest(BaseModel):
    url: str

@router.post("/check")
async def check_url_safety(request: URLRequest):
    try:
        url = request.url.strip()
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        parsed_url = urlparse(url)
        indicators = []
        risk_score = 0.0
        
        shortening_services = ['bit.ly', 'tinyurl', 'goo.gl', 'shorturl']
        if any(service in url for service in shortening_services):
            indicators.append('URL shortened')
            risk_score += 0.3
        
        if not parsed_url.scheme == 'https':
            indicators.append('No HTTPS - insecure connection')
            risk_score += 0.3
        
        suspicious_tlds = ['.top', '.xyz', '.online', '.club', '.site']
        if any(parsed_url.netloc.endswith(tld) for tld in suspicious_tlds):
            indicators.append('Suspicious domain extension')
            risk_score += 0.2
        
        if risk_score >= 0.7:
            safety_status = 'Dangerous'
        elif risk_score >= 0.4:
            safety_status = 'Suspicious'
        else:
            safety_status = 'Safe'
        
        return {
            'safety_status': safety_status,
            'risk_score': round(risk_score, 2),
            'indicators': indicators,
            'explanation': [
                f"This URL is {safety_status.lower()}.",
                "Always verify links before clicking."
            ],
            'recommendations': [
                "Don't click on suspicious links",
                "Check the URL carefully for typos",
                "Use a URL scanner for verification"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
