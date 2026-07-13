/// <reference types="react-scripts" />

import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { RiskBadge } from './components/RiskBadge';
import { ExplanationCard } from './components/ExplanationCard';
import { RecommendationList } from './components/RecommendationList';

console.log('✅ App loading - Professional Corporate UI');

// ============ API CONFIGURATION ============
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
console.log('📡 API URL:', API_URL);

// ============ RESULT DISPLAY ============
const ResultDisplay: React.FC<{ result: any }> = ({ result }) => {
  if (!result) return null;
  
  // Handle different field names from different endpoints
  const confidence = result.confidence_score !== undefined ? result.confidence_score : 
                    result.score !== undefined ? result.score : 0;
  const probability = result.scam_probability !== undefined ? result.scam_probability : 
                     result.probability !== undefined ? result.probability : 0;
  const riskLevel = result.risk_level || 'Low';
  const indicators = result.indicators || [];
  const explanations = result.explanation || result.explanations || [];
  const recommendations = result.recommendations || [];
  const isSuspicious = result.is_suspicious;
  
  return (
    <div className="mt-6 space-y-4">
      <div className="flex items-center justify-between border-b border-gray-200 pb-4">
        <h3 className="text-xl font-semibold text-gray-800">Analysis Results</h3>
        <RiskBadge level={riskLevel} />
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
          <p className="text-sm text-gray-600">Confidence Score</p>
          <p className="text-2xl font-bold text-gray-800">
            {confidence ? `${(confidence * 100).toFixed(0)}%` : 'N/A'}
          </p>
        </div>
        <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
          <p className="text-sm text-gray-600">Risk Score</p>
          <p className="text-2xl font-bold text-gray-800">
            {probability ? `${(probability * 100).toFixed(0)}%` : 'N/A'}
          </p>
        </div>
      </div>
      {isSuspicious !== undefined && (
        <div className={`p-3 rounded-lg text-center font-semibold ${
          isSuspicious ? 'bg-red-50 text-red-700 border border-red-200' : 'bg-green-50 text-green-700 border border-green-200'
        }`}>
          {isSuspicious ? '⚠️ This job posting appears suspicious' : '✅ This job posting appears legitimate'}
        </div>
      )}
      {explanations && explanations.length > 0 && (
        <ExplanationCard explanations={explanations} />
      )}
      {recommendations && recommendations.length > 0 && (
        <RecommendationList recommendations={recommendations} />
      )}
      {indicators && indicators.length > 0 && (
        <div className="mt-4">
          <h4 className="font-semibold text-gray-800 mb-2">Detected Indicators</h4>
          <ul className="list-disc pl-5 space-y-1">
            {indicators.map((indicator: any, idx: number) => (
              <li key={idx} className="text-gray-700">
                <span className="font-medium">{indicator.category || 'Indicator'}:</span>{' '}
                {indicator.matches ? indicator.matches.join(', ') : typeof indicator === 'string' ? indicator : JSON.stringify(indicator)}
                {indicator.severity && (
                  <span className={`ml-2 text-xs px-2 py-1 rounded-full ${
                    indicator.severity === 'High' ? 'bg-red-100 text-red-700' :
                    indicator.severity === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                    'bg-green-100 text-green-700'
                  }`}>
                    {indicator.severity}
                  </span>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

// ============ ICON COMPONENTS ============
const IconMessage = () => <span className="material-icons text-blue-600 text-2xl">message</span>;
const IconWork = () => <span className="material-icons text-purple-600 text-2xl">work</span>;
const IconLink = () => <span className="material-icons text-green-600 text-2xl">link</span>;
const IconImage = () => <span className="material-icons text-pink-600 text-2xl">image</span>;
const IconWarning = () => <span className="material-icons text-orange-600 text-2xl">warning</span>;
const IconSchool = () => <span className="material-icons text-indigo-600 text-2xl">school</span>;

// ============ QUIZ MODAL ============
const QuizModal: React.FC<{ 
  title: string; 
  questions: any[]; 
  onClose: () => void;
}> = ({ title, questions, onClose }) => {
  const [currentQuestion, setCurrentQuestion] = React.useState(0);
  const [selectedAnswer, setSelectedAnswer] = React.useState<number | null>(null);
  const [score, setScore] = React.useState(0);
  const [showResult, setShowResult] = React.useState(false);

  const handleAnswer = (index: number) => {
    if (selectedAnswer !== null) return;
    setSelectedAnswer(index);
    if (index === questions[currentQuestion].correct) {
      setScore(score + 1);
    }
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer(null);
    } else {
      setShowResult(true);
    }
  };

  const handleRestart = () => {
    setCurrentQuestion(0);
    setSelectedAnswer(null);
    setScore(0);
    setShowResult(false);
  };

  if (showResult) {
    const percentage = Math.round((score / questions.length) * 100);
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full p-8 max-h-[90vh] overflow-y-auto">
          <div className="text-center">
            <div className="text-6xl mb-4">
              {percentage >= 80 ? '🎉' : percentage >= 60 ? '😊' : '📚'}
            </div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Quiz Complete!</h2>
            <p className="text-gray-600 mb-4">You scored {score} out of {questions.length}</p>
            <div className="w-full bg-gray-200 rounded-full h-4 mb-6">
              <div 
                className={`h-4 rounded-full transition-all ${
                  percentage >= 80 ? 'bg-green-500' : 
                  percentage >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                }`}
                style={{ width: `${percentage}%` }}
              />
            </div>
            <p className="text-sm text-gray-600 mb-6">
              {percentage >= 80 ? 'Excellent! You really know your stuff!' :
               percentage >= 60 ? 'Good job! Keep learning to stay safe online!' :
               'Keep learning! Review the topics and try again.'}
            </p>
            <div className="flex gap-4 justify-center">
              <button
                onClick={handleRestart}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Retry Quiz
              </button>
              <button
                onClick={onClose}
                className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const question = questions[currentQuestion];
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full p-8 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-gray-800">{title}</h2>
          <span className="text-sm text-gray-500">
            Question {currentQuestion + 1} of {questions.length}
          </span>
        </div>
        
        <div className="mb-6">
          <p className="text-lg text-gray-800">{question.question}</p>
        </div>

        <div className="space-y-3">
          {question.options.map((option: string, idx: number) => (
            <button
              key={idx}
              onClick={() => handleAnswer(idx)}
              className={`w-full text-left p-4 rounded-lg border transition-all ${
                selectedAnswer === null
                  ? 'hover:bg-gray-50 hover:border-blue-300'
                  : idx === question.correct
                  ? 'bg-green-50 border-green-500'
                  : selectedAnswer === idx
                  ? 'bg-red-50 border-red-500'
                  : 'border-gray-200'
              }`}
              disabled={selectedAnswer !== null}
            >
              <span className="font-medium">{String.fromCharCode(65 + idx)}. </span>
              {option}
              {selectedAnswer !== null && idx === question.correct && (
                <span className="ml-2 text-green-600">✓</span>
              )}
              {selectedAnswer === idx && idx !== question.correct && (
                <span className="ml-2 text-red-600">✗</span>
              )}
            </button>
          ))}
        </div>

        <div className="mt-6 flex justify-between items-center">
          <span className="text-sm text-gray-500">
            Score: {score} / {questions.length}
          </span>
          {selectedAnswer !== null && (
            <button
              onClick={handleNext}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              {currentQuestion < questions.length - 1 ? 'Next Question →' : 'See Results'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

// ============ SCAM ANALYZER ============
const ScamAnalyzer: React.FC = () => {
  const [text, setText] = React.useState('');
  const [isAnalyzing, setIsAnalyzing] = React.useState(false);
  const [result, setResult] = React.useState<any>(null);
  const [error, setError] = React.useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!text.trim() || text.length < 10) {
      setError('Please enter at least 10 characters');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setResult(null);

    try {
      console.log('📤 Sending request to:', `${API_URL}/scam/analyze`);
      const response = await fetch(`${API_URL}/scam/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('📥 Received response:', data);
      setResult(data);
    } catch (err: any) {
      console.error('❌ Error:', err);
      setError(err.message || 'Failed to analyze. Please make sure the backend is running.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
        <div className="flex items-center gap-3 mb-2">
          <IconMessage />
          <h2 className="text-2xl font-bold text-gray-800">Message Analysis</h2>
        </div>
        <p className="text-gray-600 mb-4 ml-10">Analyze WhatsApp messages, SMS, emails, and other text content</p>
        <textarea
          className="w-full h-32 p-4 border border-gray-300 rounded-lg mb-4 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          placeholder="Paste a suspicious message here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button
          className={`w-full py-3 px-6 rounded-lg font-semibold text-white transition-all ${
            isAnalyzing ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 hover:shadow-lg'
          }`}
          onClick={handleAnalyze}
          disabled={isAnalyzing}
        >
          {isAnalyzing ? 'Analyzing...' : 'Analyze Message'}
        </button>
        {error && <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">{error}</div>}
        {result && <ResultDisplay result={result} />}
      </div>
    </div>
  );
};

// ============ JOB ANALYZER ============
const JobAnalyzer: React.FC = () => {
  const [jobText, setJobText] = React.useState('');
  const [companyName, setCompanyName] = React.useState('');
  const [isAnalyzing, setIsAnalyzing] = React.useState(false);
  const [result, setResult] = React.useState<any>(null);
  const [error, setError] = React.useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!jobText.trim() || jobText.length < 20) {
      setError('Please enter at least 20 characters');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setResult(null);

    try {
      console.log('📤 Sending job request to:', `${API_URL}/jobs/analyze`);
      const response = await fetch(`${API_URL}/jobs/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_text: jobText, company_name: companyName }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('📥 Received job response:', data);
      setResult(data);
    } catch (err: any) {
      console.error('❌ Error:', err);
      setError(err.message || 'Failed to analyze job');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
        <div className="flex items-center gap-3 mb-2">
          <IconWork />
          <h2 className="text-2xl font-bold text-gray-800">Job Advertisement Analysis</h2>
        </div>
        <p className="text-gray-600 mb-4 ml-10">Verify if a job posting is legitimate</p>
        <textarea
          className="w-full h-32 p-4 border border-gray-300 rounded-lg mb-4 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          placeholder="Paste the full job advertisement here..."
          value={jobText}
          onChange={(e) => setJobText(e.target.value)}
        />
        <input
          type="text"
          className="w-full p-3 border border-gray-300 rounded-lg mb-4 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          placeholder="Company Name (optional)"
          value={companyName}
          onChange={(e) => setCompanyName(e.target.value)}
        />
        <button
          className={`w-full py-3 px-6 rounded-lg font-semibold text-white transition-all ${
            isAnalyzing ? 'bg-gray-400 cursor-not-allowed' : 'bg-purple-600 hover:bg-purple-700 hover:shadow-lg'
          }`}
          onClick={handleAnalyze}
          disabled={isAnalyzing}
        >
          {isAnalyzing ? 'Analyzing...' : 'Check Job Advertisement'}
        </button>
        {error && <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">{error}</div>}
        {result && <ResultDisplay result={result} />}
      </div>
    </div>
  );
};

// ============ URL CHECKER ============
const URLChecker: React.FC = () => {
  const [url, setUrl] = React.useState('');
  const [isChecking, setIsChecking] = React.useState(false);
  const [result, setResult] = React.useState<any>(null);
  const [error, setError] = React.useState<string | null>(null);

  const handleCheck = async () => {
    if (!url.trim()) {
      setError('Please enter a URL');
      return;
    }

    setIsChecking(true);
    setError(null);
    setResult(null);

    try {
      console.log('📤 Sending URL request to:', `${API_URL}/url/check`);
      const response = await fetch(`${API_URL}/url/check`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('📥 Received URL response:', data);
      setResult(data);
    } catch (err: any) {
      console.error('❌ Error:', err);
      setError(err.message || 'Failed to check URL');
    } finally {
      setIsChecking(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch(status) {
      case 'Safe': return 'bg-green-100 text-green-800 border-green-200';
      case 'Suspicious': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'Dangerous': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
        <div className="flex items-center gap-3 mb-2">
          <IconLink />
          <h2 className="text-2xl font-bold text-gray-800">URL Safety Check</h2>
        </div>
        <p className="text-gray-600 mb-4 ml-10">Check if a website link is safe or potentially malicious</p>
        <input
          type="text"
          className="w-full p-3 border border-gray-300 rounded-lg mb-4 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          placeholder="Enter URL to check (e.g., https://example.com)"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button
          className={`w-full py-3 px-6 rounded-lg font-semibold text-white transition-all ${
            isChecking ? 'bg-gray-400 cursor-not-allowed' : 'bg-green-600 hover:bg-green-700 hover:shadow-lg'
          }`}
          onClick={handleCheck}
          disabled={isChecking}
        >
          {isChecking ? 'Checking...' : 'Check URL'}
        </button>
        {error && <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">{error}</div>}
        {result && (
          <div className="mt-6 space-y-4">
            <div className="flex items-center justify-between border-b border-gray-200 pb-4">
              <h3 className="text-xl font-semibold text-gray-800">URL Analysis</h3>
              <span className={`px-4 py-2 rounded-full text-sm font-semibold border ${getStatusColor(result.safety_status)}`}>
                {result.safety_status}
              </span>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
              <p className="text-sm text-gray-600">Risk Score</p>
              <p className="text-2xl font-bold text-gray-800">{(result.risk_score * 100).toFixed(0)}%</p>
            </div>
            {result.indicators && result.indicators.length > 0 && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <h4 className="font-semibold text-yellow-800 mb-2">Suspicious Indicators</h4>
                <ul className="list-disc pl-5 space-y-1">
                  {result.indicators.map((indicator: string, idx: number) => (
                    <li key={idx} className="text-yellow-700">{indicator}</li>
                  ))}
                </ul>
              </div>
            )}
            <ExplanationCard explanations={result.explanation || []} />
            <RecommendationList recommendations={result.recommendations || []} />
          </div>
        )}
      </div>
    </div>
  );
};

// ============ IMAGE ANALYZER ============
const ImageAnalyzer: React.FC = () => {
  const [file, setFile] = React.useState<File | null>(null);
  const [preview, setPreview] = React.useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = React.useState(false);
  const [result, setResult] = React.useState<any>(null);
  const [error, setError] = React.useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result as string);
      reader.readAsDataURL(selectedFile);
    }
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please select an image');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('image', file);
      console.log('📤 Sending image to:', `${API_URL}/image/analyze`);
      const response = await fetch(`${API_URL}/image/analyze`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('📥 Received image response:', data);
      setResult(data);
    } catch (err: any) {
      console.error('❌ Error:', err);
      setError(err.message || 'Failed to analyze image');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
        <div className="flex items-center gap-3 mb-2">
          <IconImage />
          <h2 className="text-2xl font-bold text-gray-800">Image & Screenshot Analysis</h2>
        </div>
        <p className="text-gray-600 mb-4 ml-10">Upload a screenshot of a suspicious message for analysis</p>
        
        <input
          type="file"
          accept="image/*"
          className="w-full p-4 border-2 border-dashed border-gray-300 rounded-lg mb-4 cursor-pointer hover:border-blue-500 transition-colors"
          onChange={handleFileChange}
        />
        
        {preview && (
          <div className="mb-4">
            <img src={preview} alt="Preview" className="max-h-64 mx-auto rounded-lg border" />
          </div>
        )}
        
        <button
          className={`w-full py-3 px-6 rounded-lg font-semibold text-white transition-all ${
            isAnalyzing || !file ? 'bg-gray-400 cursor-not-allowed' : 'bg-pink-600 hover:bg-pink-700 hover:shadow-lg'
          }`}
          onClick={handleAnalyze}
          disabled={isAnalyzing || !file}
        >
          {isAnalyzing ? 'Analyzing...' : 'Analyze Image'}
        </button>
        
        {error && <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">{error}</div>}
        
        {result && (
          <div className="mt-6 p-6 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-center gap-2 mb-3">
              <span className="material-icons text-blue-600">info</span>
              <h3 className="text-lg font-semibold text-blue-800">Analysis Complete</h3>
            </div>
            <p className="text-blue-700">
              Image uploaded successfully. The text has been extracted and analyzed.
            </p>
            {result.extracted_text && (
              <div className="mt-3 p-3 bg-white rounded border border-blue-200">
                <p className="text-sm text-gray-600 font-semibold">Extracted Text:</p>
                <p className="text-sm text-gray-700 mt-1">{result.extracted_text}</p>
              </div>
            )}
            {result.analysis && <ResultDisplay result={result.analysis} />}
          </div>
        )}
        
        {!result && !error && (
          <div className="mt-4 p-4 bg-gray-50 border border-gray-200 rounded-lg">
            <p className="text-gray-600 text-sm">
              Upload a screenshot of a suspicious message (WhatsApp, SMS, email, etc.) for analysis. 
              The system will extract text and detect potential scams.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

// ============ MISINFORMATION DETECTOR ============
const MisinformationDetector: React.FC = () => {
  const [text, setText] = React.useState('');
  const [isAnalyzing, setIsAnalyzing] = React.useState(false);
  const [result, setResult] = React.useState<any>(null);
  const [error, setError] = React.useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!text.trim() || text.length < 10) {
      setError('Please enter at least 10 characters');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setResult(null);

    try {
      console.log('📤 Sending misinformation request to:', `${API_URL}/misinfo/analyze`);
      const response = await fetch(`${API_URL}/misinfo/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('📥 Received misinformation response:', data);
      setResult(data);
    } catch (err: any) {
      console.error('❌ Error:', err);
      setError(err.message || 'Failed to analyze misinformation');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
        <div className="flex items-center gap-3 mb-2">
          <IconWarning />
          <h2 className="text-2xl font-bold text-gray-800">Misinformation Detection</h2>
        </div>
        <p className="text-gray-600 mb-4 ml-10">Analyze news articles and social media posts for potential misinformation</p>
        <textarea
          className="w-full h-32 p-4 border border-gray-300 rounded-lg mb-4 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          placeholder="Paste a news article, social media post, or claim here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button
          className={`w-full py-3 px-6 rounded-lg font-semibold text-white transition-all ${
            isAnalyzing ? 'bg-gray-400 cursor-not-allowed' : 'bg-orange-600 hover:bg-orange-700 hover:shadow-lg'
          }`}
          onClick={handleAnalyze}
          disabled={isAnalyzing}
        >
          {isAnalyzing ? 'Analyzing...' : 'Check for Misinformation'}
        </button>
        {error && <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">{error}</div>}
        {result && (
          <div className="mt-6 space-y-4">
            <div className="flex items-center justify-between border-b border-gray-200 pb-4">
              <h3 className="text-xl font-semibold text-gray-800">Analysis Results</h3>
              <RiskBadge level={result.risk_level} />
            </div>
            {result.suspicious_elements && result.suspicious_elements.length > 0 && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <h4 className="font-semibold text-yellow-800 mb-2">Suspicious Elements</h4>
                <ul className="list-disc pl-5 space-y-1">
                  {result.suspicious_elements.map((item: any, idx: number) => (
                    <li key={idx} className="text-yellow-700">
                      <strong>"{item.word}"</strong> - {item.category}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            <ExplanationCard explanations={result.explanation || []} />
            <RecommendationList recommendations={result.recommendations || []} />
          </div>
        )}
      </div>
    </div>
  );
};

// ============ EDUCATION HUB ============
const EducationHub: React.FC = () => {
  const [expandedTopic, setExpandedTopic] = React.useState<string | null>(null);
  const [activeQuiz, setActiveQuiz] = React.useState<{title: string, questions: any[]} | null>(null);

  const topics = [
    {
      id: 'phishing',
      title: 'Phishing Awareness',
      description: 'Learn to identify phishing emails, SMS, and websites',
      icon: 'security',
      content: [
        'Check the sender\'s email address carefully - scammers often use slight variations',
        'Never click on suspicious links - hover over them to see the real URL',
        'Look for poor grammar and spelling errors',
        'Be suspicious of urgent requests for personal information',
        'Verify suspicious messages by contacting the company directly using official channels'
      ]
    },
    {
      id: 'deepfake',
      title: 'Deepfake Recognition',
      description: 'Understand AI-generated media and how to spot it',
      icon: 'smart_display',
      content: [
        'Look for unnatural eye movements and blinking patterns',
        'Check for inconsistent lighting and shadows',
        'Listen for unnatural voice patterns and robotic speech',
        'Watch for inconsistent facial expressions',
        'Use reverse image search to verify suspicious content'
      ]
    },
    {
      id: 'password-security',
      title: 'Password Security',
      description: 'Create strong passwords and use 2FA effectively',
      icon: 'lock',
      content: [
        'Use passwords at least 12 characters long with a mix of characters',
        'Never reuse passwords across multiple accounts',
        'Enable Two-Factor Authentication (2FA) whenever possible',
        'Use a password manager to store and generate strong passwords',
        'Regularly check if your accounts have been compromised'
      ]
    },
    {
      id: 'social-engineering',
      title: 'Social Engineering',
      description: 'Recognize manipulation tactics used by scammers',
      icon: 'psychology',
      content: [
        'Be wary of unsolicited requests for personal information',
        'Never share sensitive information over the phone unless you initiated the call',
        'Verify the identity of anyone asking for sensitive data',
        'Be suspicious of calls claiming to be from banks or government agencies',
        'If something feels off, trust your instincts and verify independently'
      ]
    },
    {
      id: 'job-scams',
      title: 'Job Scams',
      description: 'Identify fraudulent job advertisements and recruitment scams',
      icon: 'work_off',
      content: [
        'Research the company thoroughly before applying',
        'Be cautious of jobs that ask for money upfront',
        'Verify the company has a professional website and online presence',
        'Check for unrealistic salary offers that seem too good to be true',
        'Report suspicious job ads to the platform where they were posted'
      ]
    },
    {
      id: 'ai-misinformation',
      title: 'AI Misinformation',
      description: 'Understand AI-generated fake news and manipulation',
      icon: 'auto_awesome',
      content: [
        'Always verify information from multiple trusted sources',
        'Check the credibility of the source before sharing',
        'Look for missing context or manipulated statistics',
        'Use fact-checking websites like Snopes or FactCheck.org',
        'Be critical of content that triggers strong emotional responses'
      ]
    }
  ];

  const quizzes = {
    phishing: {
      title: 'Phishing Detection Quiz',
      questions: [
        {
          question: 'What is a common sign of a phishing email?',
          options: ['Professional language and perfect grammar', 'Urgent requests for personal information', 'Links to reputable websites', 'All of the above'],
          correct: 1
        },
        {
          question: 'What should you do if you receive a suspicious email?',
          options: ['Reply and ask for more information', 'Click the link to verify', 'Don\'t respond and report it', 'Forward it to all your contacts'],
          correct: 2
        },
        {
          question: 'What does "phishing" refer to?',
          options: ['A legitimate marketing technique', 'An attempt to steal personal information through deceptive emails', 'A new programming language', 'A type of computer virus'],
          correct: 1
        },
        {
          question: 'Which of these is a red flag in an email?',
          options: ['Personalized greeting', 'Requests for your password', 'Professional signature', 'Clear subject line'],
          correct: 1
        },
        {
          question: 'What should you check before clicking a link in an email?',
          options: ['The font size', 'The color of the link', 'The actual URL by hovering over it', 'Whether the link is bold'],
          correct: 2
        }
      ]
    },
    password: {
      title: 'Password Security Quiz',
      questions: [
        {
          question: 'What makes a password strong?',
          options: ['Using your pet\'s name', 'At least 12 characters with a mix of types', 'Using the same password everywhere', 'Using only numbers'],
          correct: 1
        },
        {
          question: 'How often should you change your passwords?',
          options: ['Never', 'Every month', 'When you suspect a breach', 'Every decade'],
          correct: 2
        },
        {
          question: 'What is Two-Factor Authentication (2FA)?',
          options: ['Using two passwords', 'A second layer of security beyond your password', 'Having two accounts', 'A type of password manager'],
          correct: 1
        },
        {
          question: 'Is it safe to use the same password for multiple accounts?',
          options: ['Yes, it saves time', 'No, if one is compromised, all are at risk', 'Only if it\'s a strong password', 'It depends on the account type'],
          correct: 1
        },
        {
          question: 'What is a password manager?',
          options: ['A tool to help you remember passwords', 'A tool to generate and store strong passwords securely', 'A person who manages passwords', 'A new type of lock'],
          correct: 1
        }
      ]
    },
    ai_misinfo: {
      title: 'AI Misinformation Quiz',
      questions: [
        {
          question: 'What is AI-generated misinformation?',
          options: ['Information created by AI that is false or misleading', 'Information created by humans', 'All AI content is misinformation', 'Only text-based content'],
          correct: 0
        },
        {
          question: 'How can you spot AI-generated content?',
          options: ['Always trust it', 'Look for inconsistencies, unnatural language, and check sources', 'It\'s impossible to spot', 'Only use social media to verify'],
          correct: 1
        },
        {
          question: 'What should you do before sharing news online?',
          options: ['Share it immediately', 'Verify the source and check multiple outlets', 'Only share if it\'s shocking', 'Share it only on one platform'],
          correct: 1
        },
        {
          question: 'What is a deepfake?',
          options: ['A type of social media post', 'AI-generated media that manipulates faces and voices', 'A new type of camera', 'A legitimate news source'],
          correct: 1
        },
        {
          question: 'Why is critical thinking important online?',
          options: ['It\'s not important', 'Because not everything you read online is true', 'Only for young people', 'To win arguments'],
          correct: 1
        }
      ]
    }
  };

  const toggleTopic = (id: string) => {
    setExpandedTopic(expandedTopic === id ? null : id);
  };

  const startQuiz = (quizKey: string) => {
    const quiz = quizzes[quizKey as keyof typeof quizzes];
    if (quiz) {
      setActiveQuiz(quiz);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      {activeQuiz && (
        <QuizModal
          title={activeQuiz.title}
          questions={activeQuiz.questions}
          onClose={() => setActiveQuiz(null)}
        />
      )}

      <div className="text-center mb-12">
        <div className="flex justify-center items-center gap-3 mb-4">
          <span className="material-icons text-blue-600 text-4xl">school</span>
          <h1 className="text-4xl font-bold text-gray-800">Education & Safety Hub</h1>
        </div>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Learn how to protect yourself from online scams and misinformation
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {topics.map((topic) => (
          <div 
            key={topic.id}
            className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100"
          >
            <div 
              className="p-6 cursor-pointer hover:bg-gray-50 transition-colors" 
              onClick={() => toggleTopic(topic.id)}
            >
              <div className="flex items-center gap-3 mb-2">
                <span className="material-icons text-blue-600 text-3xl">{topic.icon}</span>
                <h3 className="text-xl font-bold text-gray-800">{topic.title}</h3>
              </div>
              <p className="text-gray-600 text-sm ml-11">{topic.description}</p>
              <div className="flex items-center justify-end mt-3 text-blue-600 text-sm font-medium">
                <span className="material-icons text-sm">{expandedTopic === topic.id ? 'expand_less' : 'expand_more'}</span>
              </div>
            </div>
            
            {expandedTopic === topic.id && (
              <div className="px-6 pb-6 border-t border-gray-100 pt-4">
                <ul className="space-y-2">
                  {topic.content.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="material-icons text-blue-500 text-sm mt-0.5">check_circle</span>
                      <span className="text-gray-700 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Interactive Quizzes */}
      <div className="mt-12 bg-white rounded-xl shadow-lg border border-gray-100 p-8">
        <div className="flex items-center gap-3 mb-4">
          <span className="material-icons text-blue-600 text-3xl">quiz</span>
          <h2 className="text-2xl font-bold text-gray-800">Knowledge Quizzes</h2>
        </div>
        <p className="text-gray-600 mb-6 ml-11">Test your understanding of scam awareness and online safety</p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button 
            className="flex items-center gap-3 p-4 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors text-left"
            onClick={() => startQuiz('phishing')}
          >
            <span className="material-icons text-blue-600">security</span>
            <div>
              <h4 className="font-semibold text-blue-800">Phishing Detection</h4>
              <p className="text-sm text-blue-600">5 questions • Beginner</p>
            </div>
          </button>
          
          <button 
            className="flex items-center gap-3 p-4 bg-green-50 border border-green-200 rounded-lg hover:bg-green-100 transition-colors text-left"
            onClick={() => startQuiz('password')}
          >
            <span className="material-icons text-green-600">lock</span>
            <div>
              <h4 className="font-semibold text-green-800">Password Security</h4>
              <p className="text-sm text-green-600">5 questions • Intermediate</p>
            </div>
          </button>
          
          <button 
            className="flex items-center gap-3 p-4 bg-purple-50 border border-purple-200 rounded-lg hover:bg-purple-100 transition-colors text-left"
            onClick={() => startQuiz('ai_misinfo')}
          >
            <span className="material-icons text-purple-600">auto_awesome</span>
            <div>
              <h4 className="font-semibold text-purple-800">AI Misinformation</h4>
              <p className="text-sm text-purple-600">5 questions • Advanced</p>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
};

// ============ MAIN APP ============
const App: React.FC = () => {
  const [activeTab, setActiveTab] = React.useState('scam');

  const tabs = [
    { id: 'scam', label: 'Message Analysis', icon: 'message' },
    { id: 'jobs', label: 'Job Analysis', icon: 'work' },
    { id: 'url', label: 'URL Check', icon: 'link' },
    { id: 'image', label: 'Image Analysis', icon: 'image' },
    { id: 'misinfo', label: 'Misinformation', icon: 'warning' },
    { id: 'learn', label: 'Education', icon: 'school' },
  ];

  const components: Record<string, React.FC> = {
    scam: ScamAnalyzer,
    jobs: JobAnalyzer,
    url: URLChecker,
    image: ImageAnalyzer,
    misinfo: MisinformationDetector,
    learn: EducationHub,
  };

  const ActiveComponent = components[activeTab] || ScamAnalyzer;

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-md sticky top-0 z-50 border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex flex-wrap items-center justify-between py-3">
            <div className="flex items-center gap-2">
              <span className="material-icons text-blue-600 text-3xl">shield</span>
              <h1 className="text-2xl font-bold text-blue-600 tracking-tight">AI Scam Hub</h1>
            </div>
            <div className="flex flex-wrap gap-1 md:gap-2">
              {tabs.map(tab => (
                <button
                  key={tab.id}
                  className={`flex items-center gap-1.5 px-3 md:px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                    activeTab === tab.id
                      ? 'bg-blue-50 text-blue-700 border border-blue-200'
                      : 'text-gray-600 hover:bg-gray-100 hover:text-gray-800'
                  }`}
                  onClick={() => setActiveTab(tab.id)}
                >
                  <span className="material-icons text-sm">{tab.icon}</span>
                  <span className="hidden sm:inline">{tab.label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      </nav>
      <div className="py-8">
        <ActiveComponent />
      </div>
    </div>
  );
};

const rootElement = document.getElementById('root');
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
}
