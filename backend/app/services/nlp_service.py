import joblib
import re
import os
from typing import Dict, List

class ScamDetectionService:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self._load_models()
    
    def _load_models(self):
        """Load the trained ML models"""
        try:
            model_paths = [
                '../ml-models/scam_classifier.pkl',
                'ml-models/scam_classifier.pkl',
            ]
            vectorizer_paths = [
                '../ml-models/scam_vectorizer.pkl',
                'ml-models/scam_vectorizer.pkl',
            ]
            
            for mp, vp in zip(model_paths, vectorizer_paths):
                if os.path.exists(mp) and os.path.exists(vp):
                    self.model = joblib.load(mp)
                    self.vectorizer = joblib.load(vp)
                    print(f'✅ Loaded trained ML models from {mp}')
                    return
            
            print('⚠️ Trained models not found, using fallback patterns')
            self.model = None
            self.vectorizer = None
                
        except Exception as e:
            print(f'⚠️ Error loading models: {e}')
            self.model = None
            self.vectorizer = None
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text - same as training"""
        if not text:
            return ''
        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = ' '.join(text.split())
        return text
    
    def analyze_text(self, text: str) -> Dict:
        """Analyze text using ML model"""
        print(f'🔍 Analyzing: {text[:50]}...')
        
        # Use ML model if available
        if self.model is not None and self.vectorizer is not None:
            try:
                clean_text = self.preprocess_text(text)
                vectorized = self.vectorizer.transform([clean_text])
                
                prob_array = self.model.predict_proba(vectorized)
                probability = float(prob_array[0][1])
                print(f'✅ ML Probability: {probability}')
                
                if probability > 0.7:
                    risk_level = 'High'
                elif probability > 0.3:
                    risk_level = 'Medium'
                else:
                    risk_level = 'Low'
                
                return {
                    'risk_level': risk_level,
                    'confidence_score': round(probability, 2),
                    'scam_probability': round(probability, 2),
                    'indicators': self._extract_indicators(text),
                    'explanation': self._generate_explanations(text, probability),
                    'recommendations': self._generate_recommendations(probability)
                }
            except Exception as e:
                print(f'⚠️ ML error: {e}')
                return self._fallback_analysis(text)
        
        print('⚠️ Using fallback pattern matching')
        return self._fallback_analysis(text)
    
    def _extract_indicators(self, text: str) -> List:
        """Extract scam indicators - only for display, not for decision making"""
        indicators = []
        text_lower = text.lower()
        
        # Only use keywords for display, not for classification
        keyword_map = {
            'urgency': ['urgent', 'immediately', 'hurry', 'asap', 'act now'],
            'financial': ['money', 'cash', 'bank', 'payment', 'transfer', 'million', 'dollars'],
            'personal_info': ['password', 'pin', 'otp', 'verification', 'id'],
            'suspicious_links': ['bit.ly', 'tinyurl', 'click here', 'http://', 'https://'],
            'social_engineering': ['help me', 'trust me', 'confidential', 'secret']
        }
        
        for category, keywords in keyword_map.items():
            matches = [k for k in keywords if k in text_lower]
            if matches:
                indicators.append({
                    'category': category,
                    'matches': matches[:3],
                    'severity': 'High' if len(matches) > 2 else 'Medium'
                })
        
        return indicators
    
    def _generate_explanations(self, text: str, probability: float) -> List[str]:
        """Generate explanations based on ML prediction"""
        explanations = []
        
        if probability > 0.7:
            explanations.append('This message shows strong scam indicators with high confidence.')
        elif probability > 0.3:
            explanations.append('This message shows some suspicious patterns requiring caution.')
        else:
            explanations.append('This message appears to be legitimate with low scam indicators.')
        
        # Add general observations (not hardcoded)
        text_lower = text.lower()
        if any(word in text_lower for word in ['won', 'congratulations', 'winner', 'prize']):
            explanations.append('Contains language commonly used in lottery or prize scams.')
        if any(word in text_lower for word in ['urgent', 'immediately', 'hurry', 'act now']):
            explanations.append('Uses urgency tactics to pressure you into acting quickly.')
        if any(word in text_lower for word in ['click here', 'link', 'http', 'https']):
            explanations.append('Contains links that may lead to phishing websites.')
        if any(word in text_lower for word in ['money', 'bank', 'payment', 'transfer']):
            explanations.append('Mentions financial transactions - a common scam tactic.')
        if any(word in text_lower for word in ['help me', 'trust me', 'confidential']):
            explanations.append('Uses social engineering tactics to build trust.')
        
        explanations.append('Always verify the sender identity before taking any action.')
        return explanations
    
    def _generate_recommendations(self, probability: float) -> List[str]:
        """Generate recommendations based on ML probability"""
        recommendations = []
        
        if probability > 0.3:
            recommendations.append('Do not respond to this message')
            recommendations.append('Do not click any links or download attachments')
        
        if probability > 0.5:
            recommendations.append('Never share personal or financial information online')
            recommendations.append('Verify with the official organization directly')
            recommendations.append('Report the message to your local authorities')
        
        recommendations.append('If unsure, ask a trusted friend or family member')
        recommendations.append('Learn more about scam prevention at the Education Hub')
        
        return recommendations
    
    def _fallback_analysis(self, text: str) -> Dict:
        """Fallback analysis when ML model isn't available"""
        return {
            'risk_level': 'Medium',
            'confidence_score': 0.5,
            'scam_probability': 0.5,
            'indicators': [],
            'explanation': ['ML model not available. Using basic analysis.'],
            'recommendations': ['Verify information from multiple sources.']
        }
