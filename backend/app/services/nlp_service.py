import re
from typing import Dict, List

class ScamDetectionService:
    def __init__(self):
        self.scam_patterns = {
            'urgency': [
                'urgent', 'immediately', 'hurry', 'asap', 'act now', 'limited time', 
                'expire', 'deadline', "don't miss", 'last chance', 'immediate', 'now', 'today'
            ],
            'financial': [
                'money', 'cash', 'bank', 'credit card', 'debit', 'payment',
                'transfer', 'wallet', 'account', 'r50,000', 'r100,000', 
                'million', 'dollars', 'won', 'prize', 'lottery',
                'r500', 'r1000', 'r5000', 'bitcoin', 'paypal'
            ],
            'personal_info': [
                'password', 'pin', 'otp', 'verification', 'id number',
                'confirm your details', 'update your information',
                'social security', 'verify', 'bank details',
                'credit card number', 'cvv', 'expiry date'
            ],
            'suspicious_links': [
                'bit.ly', 'tinyurl', 'shorturl', 'goo.gl', 'click here',
                '.xyz', '.top', '.online', '.club', '.site'
            ],
            'scam_phrases': [
                'you won', 'you are the winner', 'congratulations',
                'inherit', 'lottery', 'prize', 'free money',
                'work from home', 'get rich quick', 'investment opportunity',
                'claim your prize', 'you have been selected', 'urgent response needed',
                'dear sir', 'dear madam', 'prince',
                'confidential', 'exclusive opportunity'
            ],
            'social_engineering': [
                'help me', 'i need your help', 'trust me', 
                'family emergency', 'in trouble', 'need money',
                'i trust you', 'you are the only one'
            ]
        }
    
    def analyze_text(self, text: str) -> Dict:
        text_lower = text.lower()
        indicators = []
        
        for category, patterns in self.scam_patterns.items():
            matches = [p for p in patterns if p in text_lower]
            if matches:
                severity = 'High' if len(matches) > 2 else 'Medium' if len(matches) > 1 else 'Low'
                indicators.append({
                    'category': category,
                    'matches': matches[:5],
                    'severity': severity
                })
        
        total_indicators = len(indicators)
        scam_probability = min(0.95, total_indicators * 0.15 + 0.2)
        confidence_score = min(0.95, total_indicators * 0.12 + 0.3)
        
        # Boost for specific scam types
        if any(phrase in text_lower for phrase in ['prince', 'inheritance', 'foreign partner', 'transfer money']):
            scam_probability = min(0.95, scam_probability + 0.25)
            confidence_score = min(0.95, confidence_score + 0.20)
        
        if any(phrase in text_lower for phrase in ['urgent', 'suspended', 'verify immediately']):
            scam_probability = min(0.95, scam_probability + 0.20)
            confidence_score = min(0.95, confidence_score + 0.15)
        
        if total_indicators >= 3:
            risk_level = 'High'
        elif total_indicators >= 1:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        explanations = self._generate_explanations(indicators, risk_level, text_lower)
        recommendations = self._generate_recommendations(indicators, risk_level)
        
        return {
            'risk_level': risk_level,
            'confidence_score': round(confidence_score, 2),
            'scam_probability': round(scam_probability, 2),
            'indicators': indicators,
            'explanation': explanations,
            'recommendations': recommendations
        }
    
    def _generate_explanations(self, indicators: List, risk_level: str, text_lower: str) -> List[str]:
        explanations = []
        
        if risk_level == 'High':
            explanations.append("This message shows multiple strong indicators of a scam.")
        elif risk_level == 'Medium':
            explanations.append("This message shows some suspicious patterns that require caution.")
        else:
            explanations.append("No significant scam indicators were detected.")
        
        for indicator in indicators[:3]:
            category = indicator['category']
            matches = indicator['matches'][:2]
            if category == 'urgency':
                explanations.append(f"Uses urgency: Found '{', '.join(matches)}'")
            elif category == 'financial':
                explanations.append(f"Financial content: Found '{', '.join(matches)}'")
            elif category == 'personal_info':
                explanations.append(f"Requests personal information: Found '{', '.join(matches)}'")
            elif category == 'suspicious_links':
                explanations.append(f"Suspicious links: Found '{', '.join(matches)}'")
            elif category == 'scam_phrases':
                explanations.append(f"Common scam phrases: Found '{', '.join(matches)}'")
            elif category == 'social_engineering':
                explanations.append(f"Social engineering: Found '{', '.join(matches)}'")
        
        if risk_level in ['High', 'Medium']:
            # Check for Nigerian Prince specific pattern
            if any(phrase in text_lower for phrase in ['prince', 'inheritance', 'foreign', 'transfer', 'bank details']):
                explanations.append("This follows the classic 'Nigerian Prince' or 'foreign inheritance' scam pattern.")
            explanations.append("Always verify the sender's identity before taking any action.")
        
        return explanations
    
    def _generate_recommendations(self, indicators: List, risk_level: str) -> List[str]:
        recommendations = []
        
        if risk_level in ['High', 'Medium']:
            recommendations.append("Do not respond to this message")
            recommendations.append("Do not click any links or download attachments")
            
            has_financial = any(i['category'] == 'financial' for i in indicators)
            has_personal = any(i['category'] == 'personal_info' for i in indicators)
            has_links = any(i['category'] == 'suspicious_links' for i in indicators)
            has_social = any(i['category'] == 'social_engineering' for i in indicators)
            
            if has_financial:
                recommendations.append("Never share financial information online")
            if has_personal:
                recommendations.append("Never share personal information or passwords")
            if has_links:
                recommendations.append("Hover over links to check where they really go")
            if has_social:
                recommendations.append("Be aware of social engineering tactics")
            
            recommendations.append("Contact the company directly using their official website or phone number")
            recommendations.append("Report the message to your local authorities")
        
        recommendations.append("If unsure, ask a trusted friend or family member")
        recommendations.append("Learn more about scams at the Education Hub")
        
        return recommendations
