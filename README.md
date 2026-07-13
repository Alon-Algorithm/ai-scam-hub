# 🛡️ AI Scam Hub

## AI-Powered Scam Detection Platform

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2-blue.svg)](https://reactjs.org/)
[![Tailwind](https://img.shields.io/badge/Tailwind-3.3-38B2AC.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

**AI Scam Hub** is a full-stack web application that helps individuals identify online scams, phishing attempts, fraudulent job advertisements, fake websites, and AI-generated misinformation before they become victims.

The platform combines **Natural Language Processing (NLP)**, **Machine Learning**, **Computer Vision**, and **Explainable AI** to provide users with easy-to-understand risk assessments, detailed reasoning behind every prediction, and educational guidance on how to stay safe online.

## 🎯 Key Features

### 📱 Message Analysis
- Analyze WhatsApp messages, SMS, emails, and social media content
- Real-time scam detection with confidence scores
- Detailed explanations and recommendations

### 💼 Job Advertisement Checker
- Detect fraudulent job postings
- Identify red flags like upfront payment requests
- Verify company legitimacy

### 🔗 URL Safety Checker
- Check website links for phishing and malware
- Detect suspicious domain patterns
- Risk assessment with detailed indicators

### 🖼️ Image & Screenshot Analysis
- Upload screenshots of suspicious messages
- OCR text extraction and analysis
- Visual anomaly detection

### 📰 Misinformation Detector
- Identify fake news and misleading content
- Detect emotional manipulation
- Verify information credibility

### 📚 Education Hub
- Interactive learning resources
- Expandable topic cards
- Knowledge quizzes and statistics

## 🏗️ Architecture

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Material Icons** for professional UI
- Responsive design with modern UX

### Backend
- **FastAPI** for high-performance API
- **Machine Learning** with scikit-learn
- **NLP** with NLTK and custom models
- **Computer Vision** with OCR
- **Explainable AI** with transparency features

### ML Pipeline
- TfidfVectorizer for text features
- Logistic Regression for classification
- 92% detection accuracy
- Continuous improvement with new data

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone the repository**
`ash
git clone https://github.com/yourusername/ai-scam-hub.git
cd ai-scam-hub
Backend Setup

bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Frontend Setup

bash
cd frontend
npm install
npm start
Access the Application

Frontend: http://localhost:3000

Backend API: http://localhost:8000

API Docs: http://localhost:8000/docs

📊 Training the Model
bash
cd ml-models/training
python train_with_real_data.py
🧪 Testing
Test messages are available in the Education Hub or use:

bash
curl -X POST http://localhost:8000/api/scam/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Congratulations! You won ,000,000!"}'
📈 Performance
MetricScore
Accuracy92%
Precision91%
Recall89%
F1-Score90%
🛡️ Responsible AI
✅ Transparent predictions with explanations

✅ No black-box decisions

✅ User privacy protected

✅ Educational focus

✅ Human-in-the-loop design

📚 Tech Stack
Backend
FastAPI

Python 3.10

scikit-learn

NLTK

Tesseract OCR

SQLAlchemy

Frontend
React 18

TypeScript

Tailwind CSS

Material Icons

Axios

ML/AI
Logistic Regression

TfidfVectorizer

NLTK for NLP

scikit-learn

DevOps
Docker

Git

GitHub Actions

👥 Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Open a Pull Request

📄 License
MIT License - see LICENSE file for details

🤝 Acknowledgments
UCI SMS Spam Collection

Kaggle Datasets

South African Cybercrime Reports

📞 Contact
For questions or feedback, please open an issue on GitHub.

Made with ❤️ for a safer digital world
