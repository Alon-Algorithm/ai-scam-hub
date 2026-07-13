from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import re

router = APIRouter()

class JobAnalysisRequest(BaseModel):
    job_text: str
    company_name: Optional[str] = None

# Suspicious patterns for job scams
SUSPICIOUS_PATTERNS = {
    'upfront_payment': [
        'pay', 'fee', 'deposit', 'registration', 'processing',
        'application fee', 'training fee', 'equipment fee',
        'admin fee', 'activation fee', 'membership fee',
        'send money', 'transfer', 'payment required',
        'paypal', 'western union', 'moneygram', 'bitcoin',
        'crypto', 'e-wallet', 'wallet', 'cashapp'
    ],
    'unrealistic_salary': [
        'r100,000', 'r50,000', 'r80,000', 'r200,000',
        '100,000', '50,000', '80,000', '200,000',
        'commission', 'bonus', 'uncapped earnings',
        'work from home', 'no experience', 'no degree',
        'get rich', 'quick money', 'fast cash'
    ],
    'suspicious_email': [
        '@gmail.com', '@yahoo.com', '@outlook.com',
        '@hotmail.com', '@protonmail.com', '@yandex.com',
        '@mail.com', '@icloud.com', '@aol.com'
    ],
    'urgency': [
        'urgent', 'immediately', 'asap', 'right now',
        'limited time', 'hurry', 'act now', 'today',
        'immediate start', 'needed now'
    ],
    'red_flags': [
        'confidential', 'discreet', 'hiring urgently',
        'no interview', 'start immediately',
        'must have whatsapp', 'must have smartphone',
        'own transport', 'home based'
    ]
}

# Salary ranges for different job levels (South African context)
LEGITIMATE_SALARY_RANGES = {
    'entry': (15000, 25000),
    'junior': (25000, 40000),
    'mid': (40000, 60000),
    'senior': (60000, 100000),
    'executive': (100000, 200000)
}

def extract_salary(text: str) -> Optional[int]:
    """Extract salary amount from text"""
    patterns = [
        r'R\s*(\d{1,3}(?:,\d{3})*)',
        r'R(\d{1,3}(?:,\d{3})*)',
        r'(\d{1,3}(?:,\d{3})*)\s*(?:per month|month|pm)',
        r'(\d{1,3}(?:,\d{3})*)\s*(?:per week|week|pw)'
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount = match.group(1).replace(',', '')
            return int(amount)
    return None

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
        total_score = 0.0
        
        # Check for upfront payment
        payment_matches = [p for p in SUSPICIOUS_PATTERNS['upfront_payment'] if p in text_lower]
        if payment_matches:
            score = min(0.35, len(payment_matches) * 0.08)
            indicators.append({
                'category': 'upfront_payment',
                'matches': payment_matches[:5],
                'score': round(score, 2)
            })
            total_score += score
        
        # Check for unrealistic salary
        salary_matches = [p for p in SUSPICIOUS_PATTERNS['unrealistic_salary'] if p in text_lower]
        if salary_matches:
            score = min(0.30, len(salary_matches) * 0.06)
            indicators.append({
                'category': 'unrealistic_salary',
                'matches': salary_matches[:5],
                'score': round(score, 2)
            })
            total_score += score
            
            # Check actual salary amount
            salary_amount = extract_salary(request.job_text)
            if salary_amount:
                if salary_amount > 80000 and any(word in text_lower for word in ['entry', 'junior', 'no experience']):
                    indicators.append({
                        'category': 'salary_inflated',
                        'matches': [f'R{salary_amount:,} for entry level position'],
                        'score': 0.20
                    })
                    total_score += 0.20
        
        # Check for suspicious email domains
        email_matches = [p for p in SUSPICIOUS_PATTERNS['suspicious_email'] if p in text_lower]
        if email_matches:
            score = min(0.25, len(email_matches) * 0.10)
            indicators.append({
                'category': 'suspicious_email',
                'matches': email_matches[:3],
                'score': round(score, 2)
            })
            total_score += score
        
        # Check for urgency
        urgency_matches = [p for p in SUSPICIOUS_PATTERNS['urgency'] if p in text_lower]
        if urgency_matches:
            score = min(0.20, len(urgency_matches) * 0.05)
            indicators.append({
                'category': 'urgency',
                'matches': urgency_matches[:5],
                'score': round(score, 2)
            })
            total_score += score
        
        # Check for red flags
        red_flag_matches = [p for p in SUSPICIOUS_PATTERNS['red_flags'] if p in text_lower]
        if red_flag_matches:
            score = min(0.30, len(red_flag_matches) * 0.08)
            indicators.append({
                'category': 'red_flags',
                'matches': red_flag_matches[:5],
                'score': round(score, 2)
            })
            total_score += score
        
        # Cap total score
        total_score = min(0.95, total_score)
        
        # Determine risk level
        if total_score >= 0.6:
            risk_level = 'High'
        elif total_score >= 0.3:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        # Generate explanations
        explanations = []
        if risk_level == 'High':
            explanations.append("This job advertisement shows multiple strong scam indicators.")
        elif risk_level == 'Medium':
            explanations.append("This job advertisement requires careful verification.")
        else:
            explanations.append("No major scam indicators detected, but always verify.")
        
        for indicator in indicators[:3]:
            category = indicator['category'].replace('_', ' ').title()
            matches = ', '.join(indicator['matches'][:2])
            explanations.append(f"• {category}: Found '{matches}'")
        
        if any(i['category'] == 'upfront_payment' for i in indicators):
            explanations.append("⚠️ Legitimate employers never ask for money upfront.")
        
        if any(i['category'] == 'unrealistic_salary' for i in indicators):
            explanations.append("⚠️ Extremely high salaries with no experience are a red flag.")
        
        if any(i['category'] == 'suspicious_email' for i in indicators):
            explanations.append("⚠️ Free email domains (Gmail, Yahoo) are common in job scams.")
        
        if risk_level in ['High', 'Medium']:
            explanations.append("Always research the company before applying.")
        
        # Generate recommendations
        recommendations = []
        if risk_level in ['High', 'Medium']:
            recommendations.append("Do not send money or payment of any kind")
            recommendations.append("Research the company thoroughly online")
            recommendations.append("Check the company's official website and LinkedIn presence")
            recommendations.append("Verify the job posting on the company's official careers page")
            recommendations.append("Be wary of jobs that require immediate payment for 'training' or 'processing'")
            
            if any(i['category'] == 'suspicious_email' for i in indicators):
                recommendations.append("Contact the company through their official website, not the email in the ad")
        
        recommendations.append("Trust your instincts - if it seems too good to be true, it probably is")
        recommendations.append("Report suspicious job ads to the platform where they were posted")
        
        return {
            'risk_level': risk_level,
            'is_suspicious': risk_level in ['High', 'Medium'],
            'indicators': indicators,
            'explanation': explanations,
            'recommendations': recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
