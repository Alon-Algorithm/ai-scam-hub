import React from 'react';
import { Link } from 'react-router-dom';

interface Topic {
  id: string;
  title: string;
  description: string;
  icon: string;
  color: string;
  level: 'Beginner' | 'Intermediate' | 'Advanced';
}

const topics: Topic[] = [
  {
    id: 'phishing',
    title: 'Phishing Awareness',
    description: 'Learn to identify phishing emails, SMS, and websites',
    icon: '🎣',
    color: 'bg-red-100',
    level: 'Beginner'
  },
  {
    id: 'deepfake',
    title: 'Deepfake Recognition',
    description: 'Understand AI-generated media and how to spot it',
    icon: '🤖',
    color: 'bg-purple-100',
    level: 'Intermediate'
  },
  {
    id: 'password-security',
    title: 'Password Security',
    description: 'Create strong passwords and use 2FA effectively',
    icon: '🔐',
    color: 'bg-green-100',
    level: 'Beginner'
  },
  {
    id: 'social-engineering',
    title: 'Social Engineering',
    description: 'Recognize manipulation tactics used by scammers',
    icon: '🧠',
    color: 'bg-orange-100',
    level: 'Intermediate'
  },
  {
    id: 'job-scams',
    title: 'Job Scams',
    description: 'Identify fraudulent job advertisements and recruitment scams',
    icon: '💼',
    color: 'bg-blue-100',
    level: 'Beginner'
  },
  {
    id: 'ai-misinformation',
    title: 'AI Misinformation',
    description: 'Understand AI-generated fake news and manipulation',
    icon: '📰',
    color: 'bg-indigo-100',
    level: 'Advanced'
  }
];

export const EducationHub: React.FC = () => {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">Learn & Stay Safe Online</h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Educational resources to help you recognize scams and protect yourself online
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {topics.map((topic) => (
          <Link
            key={topic.id}
            to={`/learn/${topic.id}`}
            className="block group"
          >
            <div className={`${topic.color} rounded-lg p-6 shadow-md hover:shadow-xl transition-shadow duration-300`}>
              <div className="text-4xl mb-4">{topic.icon}</div>
              <h3 className="text-xl font-bold mb-2">{topic.title}</h3>
              <p className="text-gray-600 text-sm mb-4">{topic.description}</p>
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium px-2 py-1 bg-white rounded-full">
                  {topic.level}
                </span>
                <span className="text-blue-600 group-hover:translate-x-1 transition-transform">
                  Learn More →
                </span>
              </div>
            </div>
          </Link>
        ))}
      </div>

      <div className="mt-12 bg-gray-50 rounded-lg p-8">
        <h2 className="text-2xl font-bold mb-4">Interactive Quizzes</h2>
        <p className="text-gray-600 mb-4">
          Test your knowledge with our interactive quizzes on scam awareness
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow">
            🎯 Phishing Recognition Quiz
          </button>
          <button className="p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow">
            🔐 Password Strength Quiz
          </button>
          <button className="p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow">
            🤖 AI Awareness Quiz
          </button>
        </div>
      </div>
    </div>
  );
};