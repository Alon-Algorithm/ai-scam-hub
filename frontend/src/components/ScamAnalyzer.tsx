import React, { useState } from 'react';
import { RiskBadge } from './RiskBadge';
import { ExplanationCard } from './ExplanationCard';
import { RecommendationList } from './RecommendationList';

interface AnalysisResult {
  risk_level: string;
  confidence_score: number;
  scam_probability: number;
  indicators: Array<{
    category: string;
    matches: string[];
    severity: string;
  }>;
  explanation: string[];
  recommendations: string[];
}

export const ScamAnalyzer: React.FC = () => {
  const [text, setText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = () => {
    if (!text.trim() || text.length < 10) {
      setError('Please enter at least 10 characters for analysis');
      return;
    }

    console.log('🔍 Starting analysis...');
    setIsAnalyzing(true);
    setError(null);
    setResult(null);

    // Simulate API call with fake data
    setTimeout(() => {
      console.log('✅ Analysis complete!');
      
      const mockResult: AnalysisResult = {
        risk_level: 'High',
        confidence_score: 0.87,
        scam_probability: 0.92,
        indicators: [
          {
            category: 'Urgency',
            matches: ['won', 'congratulations', 'hurry'],
            severity: 'High'
          },
          {
            category: 'Financial',
            matches: ['40 million', 'dollars'],
            severity: 'High'
          },
          {
            category: 'Scam Phrases',
            matches: ['you won', 'prize'],
            severity: 'Medium'
          }
        ],
        explanation: [
          'This message shows multiple strong indicators of a scam.',
          'Urgency: Found "won", "hurry"',
          'Financial: Found "40 million", "dollars"',
          'Scam Phrases: Found "you won", "prize"'
        ],
        recommendations: [
          'Do not respond to this message',
          'Do not click any links or download attachments',
          'Never share financial information online',
          'Verify with the official organization directly',
          'Report the message to your local authorities'
        ]
      };
      
      console.log('📊 Setting result:', mockResult);
      setResult(mockResult);
      setIsAnalyzing(false);
      console.log('✅ State updated!');
    }, 1000);
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-4">Scam Message Analyzer</h2>
        
        <div className="mb-4">
          <textarea
            className="w-full h-48 p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Paste a WhatsApp message, SMS, email, or any suspicious text here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
        </div>

        <button
          className={`w-full py-3 px-6 rounded-lg font-semibold text-white ${
            isAnalyzing ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
          } transition-colors`}
          onClick={handleAnalyze}
          disabled={isAnalyzing}
        >
          {isAnalyzing ? 'Analyzing...' : 'Analyze Message'}
        </button>

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">
            {error}
          </div>
        )}

        {result && (
          <div className="mt-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-semibold">Analysis Results</h3>
              <RiskBadge level={result.risk_level} />
            </div>

            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Confidence Score</p>
                <p className="text-2xl font-bold">
                  {(result.confidence_score * 100).toFixed(0)}%
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Scam Probability</p>
                <p className="text-2xl font-bold">
                  {(result.scam_probability * 100).toFixed(0)}%
                </p>
              </div>
            </div>

            <ExplanationCard explanations={result.explanation} />
            <RecommendationList recommendations={result.recommendations} />

            {result.indicators && result.indicators.length > 0 && (
              <div className="mt-4">
                <h4 className="font-semibold mb-2">Detected Indicators:</h4>
                <ul className="list-disc pl-5 space-y-1">
                  {result.indicators.map((indicator, idx) => (
                    <li key={idx} className="text-gray-700">
                      <span className="font-medium">{indicator.category}:</span>{' '}
                      {indicator.matches.join(', ')}
                      <span className={`ml-2 text-xs px-2 py-1 rounded-full ${
                        indicator.severity === 'High' 
                          ? 'bg-red-100 text-red-700' 
                          : indicator.severity === 'Medium'
                          ? 'bg-yellow-100 text-yellow-700'
                          : 'bg-green-100 text-green-700'
                      }`}>
                        {indicator.severity}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};