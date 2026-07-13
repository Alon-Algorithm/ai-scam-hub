import re
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class JobScamDetector:
    def __init__(self):
        self.suspicious_patterns = {
            'upfront_payment': [
                'pay', 'fee', 'deposit', 'registration', 'processing',
                'application fee', 'training fee', 'equipment fee'
            ],
            'unrealistic_salary': [
                'r100,000', 'r50,000', 'commission', 'bonus',
                'immediate start', 'no experience'
            ],
            'suspicious_email': [
                '@gmail.com', '@yahoo.com', '@outlook.com',
                '@hotmail.com', '@protonmail.com'
            ],
            'red_flags': [
                'western union', 'moneygram', 'bank transfer',
                'cryptocurrency', 'bitcoin', 'paypal',
                'confidential', 'discreet', 'urgent hiring'
            ]
        }
    
    def analyze_job_ad(self, text: str) -> Dict:
        """Analyze job advertisement for scam indicators"""
        results = {
            'is_suspicious': False,
            'risk_level': 'Low',
            'indicators': [],
            'explanation': [],
            'recommendations': []
        }
        
        text_lower = text.lower()
        total_score = 0
        
        # Check each pattern category
        for category, patterns in self.suspicious_patterns.items():
            matches = [p for p in patterns if p in text_lower]
            if matches:
                score = self._calculate_category_score(category, len(matches))
                total_score += score
                results['indicators'].append({
                    'category': category,
                    'matches': matches,
                    'score': score
                })
        
        # Determine risk level
        if total_score >= 0.6:
            results['risk_level'] = 'High'
            results['is_suspicious'] = True
        elif total_score >= 0.3:
            results['risk_level'] = 'Medium'
            results['is_suspicious'] = True
        
        # Generate explanation
        results['explanation'] = self._generate_explanation(
            results['indicators'],
            results['risk_level']
        )
        
        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(
            results['indicators'],
            results['risk_level']
        )
        
        return results
    
    def _calculate_category_score(self, category: str, match_count: int) -> float:
        """Calculate score for a category based on number of matches"""
        weights = {
            'upfront_payment': 0.3,
            'unrealistic_salary': 0.2,
            'suspicious_email': 0.2,
            'red_flags': 0.3
        }
        weight = weights.get(category, 0.1)
        return min(weight * min(match_count, 3), weight)
    
    def _generate_explanation(self, indicators: List, risk_level: str) -> List[str]:
        """Generate explanations for job ad analysis"""
        explanations = []
        
        if risk_level == 'High':
            explanations.append("This job advertisement shows strong scam indicators.")
        elif risk_level == 'Medium':
            explanations.append("This job advertisement requires careful verification.")
        else:
            explanations.append("No major scam indicators detected.")
        
        for indicator in indicators[:3]:
            category = indicator['category'].replace('_', ' ').title()
            matches = ', '.join(indicator['matches'][:2])
            explanations.append(f"• {category}: Contains '{matches}'")
        
        return explanations
    
    def _generate_recommendations(self, indicators: List, risk_level: str) -> List[str]:
        """Generate recommendations for job seekers"""
        recommendations = []
        
        if risk_level in ['High', 'Medium']:
            recommendations.append("Research the company thoroughly before applying")
            recommendations.append("Check the company's official website and LinkedIn presence")
            recommendations.append("Be wary of jobs that ask for money upfront")
            recommendations.append("Verify job posting on official company careers page")
        
        recommendations.append("Trust your instincts - if it seems too good to be true, it probably is")
        
        return recommendations