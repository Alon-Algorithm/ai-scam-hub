import joblib
import re
import os
from typing import Dict, List

class ScamDetectionService:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.scam_patterns = self._get_scam_patterns()
        self._load_models()
    
    def _get_scam_patterns(self):
        return {
            'urgency': ['urgent', 'immediately', 'hurry', 'asap', 'act now', 'limited time', 'expire'],
            'financial': ['money', 'cash', 'bank', 'payment', 'transfer', 'million', 'dollars', 'won', 'prize', 'lottery'],
            'personal_info': ['password', 'pin', 'otp', 'verification', 'id', 'social security', 'verify'],
            'suspicious_links': ['bit.ly', 'tinyurl', 'click here', 'http://', 'https://'],
            'scam_phrases': ['congratulations', 'winner', 'you won', 'claim', 'free', 'selected']
        }
    
    def _load_models(self):
        try:
            model_paths = [
                '../ml-models/scam_classifier.pkl',
                'ml-models/scam_classifier.pkl',
                'C:/Users/lolli/Downloads/proj2/ai-scam-hub/ml-models/scam_classifier.pkl'
            ]
            vectorizer_paths = [
                '../ml-models/scam_vectorizer.pkl',
                'ml-models/scam_vectorizer.pkl',
                'C:/Users/lolli/Downloads/proj2/ai-scam-hub/ml-models/scam_vectorizer.pkl'
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
        if not text:
            return ''
        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = ' '.join(text.split())
        return text
    
    def analyze_text(self, text: str) -> Dict:
        print(f'🔍 Analyzing: {text[:50]}...')
        
        # Use ML model if available
        if self.model is not None and self.vectorizer is not None:
            try:
                clean_text = self.preprocess_text(text)
                print(f'✅ Clean text: {clean_text[:50]}...')
                
                vectorized = self.vectorizer.transform([clean_text])
                print(f'✅ Vectorized shape: {vectorized.shape}')
                
                prob_array = self.model.predict_proba(vectorized)
                print(f'✅ Probability array: {prob_array}')
                
                probability = float(prob_array[0][1])
                print(f'✅ Probability: {probability}')
                
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
                    'explanation': self._generate_ml_explanations(text, probability),
                    'recommendations': self._generate_ml_recommendations(probability)
                }
            except Exception as e:
                print(f'⚠️ ML error: {e}, using fallback')
                import traceback
                traceback.print_exc()
                return self._fallback_analysis(text)
        
        print('⚠️ Using fallback pattern matching')
        return self._fallback_analysis(text)
    
    def _extract_indicators(self, text: str) -> List:
        indicators = []
        text_lower = text.lower()
        
        for category, keywords in self.scam_patterns.items():
            matches = [k for k in keywords if k in text_lower]
            if matches:
                severity = 'High' if len(matches) > 2 else 'Medium'
                indicators.append({
                    'category': category,
                    'matches': matches[:3],
                    'severity': severity
                })
        
        return indicators
    
    def _generate_ml_explanations(self, text: str, probability: float) -> List[str]:
        explanations = []
        
        if probability > 0.7:
            explanations.append('This message shows strong scam indicators with high confidence.')
        elif probability > 0.3:
            explanations.append('This message shows some suspicious patterns requiring caution.')
        else:
            explanations.append('This message appears to be legitimate with low scam indicators.')
        
        text_lower = text.lower()
        if any(word in text_lower for word in ['won', 'congratulations', 'winner', 'prize', 'lottery']):
            explanations.append('Contains lottery or prize-winning language commonly used in scams.')
        if any(word in text_lower for word in ['urgent', 'immediately', 'hurry', 'act now']):
            explanations.append('Uses urgency tactics to pressure you into acting quickly.')
        if any(word in text_lower for word in ['click here', 'link', 'http', 'https', 'bit.ly']):
            explanations.append('Contains suspicious links that may lead to phishing websites.')
        if any(word in text_lower for word in ['money', 'bank', 'payment', 'transfer', 'million']):
            explanations.append('Mentions money or financial transactions - a common scam tactic.')
        
        explanations.append('Always verify the sender identity before taking any action.')
        return explanations
    
    def _generate_ml_recommendations(self, probability: float) -> List[str]:
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
        
        if total_indicators >= 3:
            risk_level = 'High'
        elif total_indicators >= 1:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        return {
            'risk_level': risk_level,
            'confidence_score': round(confidence_score, 2),
            'scam_probability': round(scam_probability, 2),
            'indicators': indicators,
            'explanation': self._generate_fallback_explanations(indicators, risk_level),
            'recommendations': self._generate_fallback_recommendations(indicators, risk_level)
        }
    
    def _generate_fallback_explanations(self, indicators: List, risk_level: str) -> List[str]:
        explanations = []
        
        if risk_level == 'High':
            explanations.append('This message shows multiple strong indicators of a scam.')
        elif risk_level == 'Medium':
            explanations.append('This message shows some suspicious patterns that require caution.')
        else:
            explanations.append('No significant scam indicators were detected.')
        
        for indicator in indicators[:3]:
            category = indicator['category']
            matches = indicator['matches'][:2]
            explanations.append(f'Found {matches} in {category}')
        
        if risk_level in ['High', 'Medium']:
            explanations.append('Always verify the sender identity before taking any action.')
        
        return explanations
    
    def _generate_fallback_recommendations(self, indicators: List, risk_level: str) -> List[str]:
        recommendations = []
        
        if risk_level in ['High', 'Medium']:
            recommendations.append('Do not respond to this message')
            recommendations.append('Do not click any links or download attachments')
            recommendations.append('Never share personal or financial information')
            recommendations.append('Report the message to the relevant authorities')
        
        recommendations.append('If unsure, ask a trusted friend or family member')
        recommendations.append('Learn more about scams at the Education Hub')
        
        return recommendations
