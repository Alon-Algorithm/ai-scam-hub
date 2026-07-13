import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ScamAnalyzer } from './components/ScamAnalyzer';
import { JobAnalyzer } from './components/JobAnalyzer';
import { EducationHub } from './components/EducationHub';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow-md">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <h1 className="text-xl font-bold text-blue-600">🛡️ AI Scam Hub</h1>
              </div>
              <div className="flex items-center space-x-4">
                <a href="/" className="text-gray-700 hover:text-blue-600">Analyzer</a>
                <a href="/jobs" className="text-gray-700 hover:text-blue-600">Job Checker</a>
                <a href="/learn" className="text-gray-700 hover:text-blue-600">Learn</a>
              </div>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<ScamAnalyzer />} />
          <Route path="/jobs" element={<JobAnalyzer />} />
          <Route path="/learn" element={<EducationHub />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;