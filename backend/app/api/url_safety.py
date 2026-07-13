from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from urllib.parse import urlparse
import re

router = APIRouter()

class URLRequest(BaseModel):
    url: str

# Known safe domains (whitelist)
SAFE_DOMAINS = {
    'google.com', 'www.google.com', 'youtube.com', 'www.youtube.com',
    'github.com', 'www.github.com', 'linkedin.com', 'www.linkedin.com',
    'stackoverflow.com', 'www.stackoverflow.com', 'python.org', 'www.python.org',
    'reactjs.org', 'www.reactjs.org', 'tailwindcss.com', 'www.tailwindcss.com',
    'render.com', 'www.render.com', 'netlify.com', 'www.netlify.com',
    'vercel.com', 'www.vercel.com', 'amazon.com', 'www.amazon.com',
    'microsoft.com', 'www.microsoft.com', 'apple.com', 'www.apple.com',
    'facebook.com', 'www.facebook.com', 'twitter.com', 'www.twitter.com',
    'instagram.com', 'www.instagram.com', 'whatsapp.com', 'www.whatsapp.com',
    'fnb.co.za', 'www.fnb.co.za', 'absa.co.za', 'www.absa.co.za',
    'nedbank.co.za', 'www.nedbank.co.za', 'standardbank.co.za', 'www.standardbank.co.za'
}

# Suspicious TLDs
SUSPICIOUS_TLDS = {'.top', '.xyz', '.online', '.club', '.site', '.tk', '.ml', '.ga', '.cf', '.click', '.download', '.review', '.work', '.date', '.men', '.loan', '.win', '.bid', '.trade', '.webcam'}

# Popular brands for impersonation detection
BRANDS = {
    'fnb', 'absa', 'nedbank', 'standardbank', 'capitec', 'paypal', 'google', 'facebook',
    'instagram', 'twitter', 'amazon', 'apple', 'microsoft', 'netflix', 'spotify',
    'whatsapp', 'linkedin', 'github', 'stackoverflow', 'python', 'react', 'tailwind',
    'render', 'vercel', 'netlify', 'youtube', 'gmail', 'hotmail', 'outlook',
    'discovery', 'sanlam', 'oldmutual', 'kingprice', 'vodacom', 'mtn', 'telkom'
}

def get_tld(domain: str) -> str:
    """Extract TLD from domain"""
    parts = domain.split('.')
    if len(parts) >= 2:
        return '.' + parts[-1]
    return ''

def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate Levenshtein distance between two strings"""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def check_brand_impersonation(domain: str) -> list:
    """Check if domain is impersonating a known brand"""
    indicators = []
    domain_lower = domain.lower()
    
    for brand in BRANDS:
        # Check if brand name appears in domain
        if brand in domain_lower:
            # Calculate distance between domain and brand
            dist = levenshtein_distance(domain_lower, brand)
            if dist > 0 and dist <= 3:
                indicators.append(f"Brand impersonation: '{brand}' appears in domain (similarity score: {dist})")
            elif brand in domain_lower and len(domain_lower) > len(brand) + 2:
                indicators.append(f"Brand impersonation: '{brand}' used in suspicious domain '{domain}'")
    
    return indicators

@router.post("/check")
async def check_url_safety(request: URLRequest):
    try:
        url = request.url.strip()
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        hostname = domain.split(':')[0]  # Remove port
        
        indicators = []
        risk_score = 0.0
        
        # 1. Check if domain is in safe whitelist
        if hostname in SAFE_DOMAINS:
            return {
                'safety_status': 'Safe',
                'risk_score': 0.0,
                'indicators': [],
                'explanation': ['This domain is on the safe list.'],
                'recommendations': ['Continue with caution as always.']
            }
        
        # 2. Check TLD reputation
        tld = get_tld(hostname)
        if tld in SUSPICIOUS_TLDS:
            indicators.append(f"Suspicious TLD: '{tld}' is commonly used in phishing attacks")
            risk_score += 0.35
        
        # 3. Check for brand impersonation
        brand_indicators = check_brand_impersonation(hostname)
        if brand_indicators:
            indicators.extend(brand_indicators)
            risk_score += 0.30 * min(len(brand_indicators), 2)
        
        # 4. Count hyphens (phishing domains often have many hyphens)
        hyphen_count = hostname.count('-')
        if hyphen_count >= 2:
            indicators.append(f"Excessive hyphens: {hyphen_count} hyphens found in domain (often used in phishing)")
            risk_score += 0.10 * min(hyphen_count, 3)
        
        # 5. Check for IP address instead of domain
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', hostname):
            indicators.append("IP address used instead of domain name (suspicious)")
            risk_score += 0.25
        
        # 6. Check domain length (legitimate domains are usually shorter)
        if len(hostname) > 30:
            indicators.append(f"Unusually long domain name ({len(hostname)} characters)")
            risk_score += 0.10
        
        # 7. Check if URL uses HTTP (not HTTPS)
        if parsed_url.scheme == 'http':
            indicators.append("No HTTPS - connection is not secure")
            risk_score += 0.20
        
        # 8. Check for common phishing keywords in URL
        phishing_keywords = ['login', 'verify', 'secure', 'update', 'confirm', 'account', 'banking', 'payment']
        url_lower = url.lower()
        found_keywords = [kw for kw in phishing_keywords if kw in url_lower]
        if found_keywords:
            indicators.append(f"Contains phishing keywords: {', '.join(found_keywords)}")
            risk_score += 0.10 * min(len(found_keywords), 2)
        
        # Determine safety status
        if risk_score >= 0.7:
            safety_status = 'Dangerous'
        elif risk_score >= 0.35:
            safety_status = 'Suspicious'
        else:
            safety_status = 'Safe'
        
        # Generate explanations
        explanations = []
        if safety_status == 'Dangerous':
            explanations.append("This URL shows multiple indicators of being a phishing or scam website.")
        elif safety_status == 'Suspicious':
            explanations.append("This URL shows some suspicious characteristics. Proceed with caution.")
        else:
            explanations.append("This URL appears safe based on current checks.")
        
        if indicators:
            explanations.append(f"Found {len(indicators)} suspicious indicator(s).")
        explanations.append("Always verify URLs before clicking, especially if they ask for personal information.")
        
        # Generate recommendations
        recommendations = []
        if safety_status in ['Dangerous', 'Suspicious']:
            recommendations.append("Do not click on this link")
            recommendations.append("Do not enter any personal information")
            recommendations.append("Verify the URL by typing the official domain directly into your browser")
            if 'No HTTPS' in str(indicators):
                recommendations.append("Avoid submitting any data on non-HTTPS websites")
            if any('brand impersonation' in i for i in indicators):
                recommendations.append("This domain appears to be impersonating a legitimate brand")
            recommendations.append("Report suspicious URLs to the relevant authorities")
        
        recommendations.append("If you need to access a service, type the official URL directly")
        recommendations.append("Use a URL scanner like VirusTotal for additional verification")
        
        return {
            'safety_status': safety_status,
            'risk_score': round(risk_score, 2),
            'indicators': indicators,
            'explanation': explanations,
            'recommendations': recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
