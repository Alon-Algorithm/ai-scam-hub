import React, { useState } from 'react';
import { analyzeJob } from '../services/api';
import { RiskBadge } from './RiskBadge';
import { ExplanationCard } from './ExplanationCard';
import { RecommendationList } from './RecommendationList';

interface AnalysisResult {
  risk_level: string;
  is_suspicious: boolean;
  indicators: Array<{
    category: string;
    matches: string[];
    score: number;
  }>;
  explanation: string[];
  recommendations: string[];
}

export const JobAnalyzer: React.FC = () => {
  const [jobText, setJobText] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!jobText.trim()) {
      setError('Please paste a job advertisement to analyze');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    
    try {
      const response = await analyzeJob({ 
        job_text: jobText, 
        company_name: companyName 
      });
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-4">Job Advertisement Checker</h2>
        <p className="text-gray-600 mb-4">
          Paste a job advertisement to check for common scam indicators
        </p>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Job Description</label>
            <textarea
              className="w-full h-48 p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Paste the full job advertisement here..."
              value={jobText}
              onChange={(e) => setJobText(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Company Name (Optional)</label>
            <input
              type="text"
              className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter company name if known..."
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
            />
          </div>

          <button
            className={`w-full py-3 px-6 rounded-lg font-semibold text-white ${
              isAnalyzing || !jobText.trim() 
                ? 'bg-gray-400 cursor-not-allowed' 
                : 'bg-blue-600 hover:bg-blue-700'
            } transition-colors`}
            onClick={handleAnalyze}
            disabled={isAnalyzing || !jobText.trim()}
          >
            {isAnalyzing ? 'Analyzing...' : 'Check Job Advertisement'}
          </button>

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">
              {error}
            </div>
          )}
        </div>

        {result && (
          <div className="mt-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-semibold">Analysis Results</h3>
              <RiskBadge level={result.risk_level} />
            </div>

            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600">Status</p>
              <p className="text-lg font-semibold">
                {result.is_suspicious ? '⚠️ Suspicious Job Ad' : '✅ No Major Concerns Detected'}
              </p>
            </div>

            <ExplanationCard explanations={result.explanation} />
            <RecommendationList recommendations={result.recommendations} />

            {result.indicators && result.indicators.length > 0 && (
              <div className="mt-4 border-t pt-4">
                <h4 className="font-semibold mb-2">Detailed Indicators:</h4>
                <div className="space-y-2">
                  {result.indicators.map((indicator, idx) => (
                    <div key={idx} className="bg-yellow-50 p-3 rounded-lg">
                      <span className="font-medium">
                        {indicator.category.replace('_', ' ').toUpperCase()}
                      </span>
                      <p className="text-sm text-gray-600">
                        Found: {indicator.matches.join(', ')}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};