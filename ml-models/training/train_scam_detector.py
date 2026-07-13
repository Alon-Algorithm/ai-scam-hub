import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score
from sklearn.pipeline import Pipeline
import joblib
import re
import nltk
from nltk.corpus import stopwords
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("AI SCAM DETECTOR - TRAINING PIPELINE")
print("=" * 60)

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# ============ 1. CREATE TRAINING DATA ============
print("\nStep 1: Creating training dataset...")

# Sample scam messages
scam_messages = [
    ("Congratulations! You have won R100,000 in our lottery! Click here to claim your prize.", 1),
    ("URGENT: Your bank account has been suspended. Verify your identity immediately.", 1),
    ("You have been selected for a cash prize of ,000. Send  for processing.", 1),
    ("Your PayPal account has been limited. Click the link to restore access.", 1),
    ("We need to verify your credit card information. Please click the link below.", 1),
    ("Work from home! Earn R50,000 per month. No experience needed. Send R500 for training.", 1),
    ("URGENT HIRING! We need people immediately. No degree required. Apply now!", 1),
    ("Make money online! Guaranteed income of R10,000 per week. Start today!", 1),
    ("We have a job opening for you! Send your CV and pay R200 for processing.", 1),
    ("Become a millionaire with our proven system! Just R1,000 to get started.", 1),
    ("Congratulations! You won an iPhone 15! Click here: bit.ly/claim-now", 1),
    ("Your account has been compromised. Send your password to secure it.", 1),
    ("Free money! Just share this message with 10 people and send R50 to this number.", 1),
    ("You have inherited ,000,000 from a relative. Send your bank details.", 1),
    ("Lottery winner! You have won R50,000. Send R1,000 to release your funds.", 1),
    ("Verify your identity now: https://fake-bank-verify.xyz or your account will be closed.", 1),
    ("Your Apple ID is about to expire. Click here to verify: https://apple-id-verify.xyz", 1),
    ("Netflix subscription suspended. Update your payment: https://netflix-update.xyz", 1),
    ("Your Facebook account has been hacked. Secure it here: https://fb-secure.xyz", 1),
    ("Amazon order #789456 requires verification. Click to confirm.", 1),
    ("I am Prince Adebayo from Nigeria. I have ,000,000 to transfer. Help me and get 20%.", 1),
    ("Dear friend, I need your help to transfer ,000,000. Please send your bank details.", 1),
    ("I am a wealthy businessman needing assistance. You will be rewarded handsomely.", 1),
    ("Confidential: I need a foreign partner to receive funds. Please reply urgently.", 1)
]

# Sample legitimate messages
legit_messages = [
    ("Hi Mom, I'll be home for dinner at 6pm. Can you make chicken stew?", 0),
    ("Hey, how are you doing? Want to grab coffee this weekend?", 0),
    ("Just checking in! How was your day? Let's catch up soon.", 0),
    ("Happy birthday! Hope you have an amazing day!", 0),
    ("The meeting is at 2pm tomorrow. Please bring your laptop.", 0),
    ("Hi team, please review the attached document and share feedback.", 0),
    ("Reminder: Project deadline is Friday. Let me know if you need help.", 0),
    ("The quarterly report is due next week. Please submit by Monday.", 0),
    ("Can we reschedule today's meeting to 3pm? Let me know.", 0),
    ("Great job on the presentation! The client was very impressed.", 0),
    ("The assignment is due tomorrow. Please submit it on the portal.", 0),
    ("Class has been cancelled today due to the teacher being sick.", 0),
    ("Can you help me with the homework? I'm stuck on question 5.", 0),
    ("The exam schedule has been posted on the notice board.", 0),
    ("Congratulations on passing! Your hard work paid off.", 0),
    ("Thanks for the gift! I really appreciate it.", 0),
    ("Let's meet at 7pm at the restaurant. See you there!", 0),
    ("The movie was great! You should definitely watch it.", 0),
    ("I'll be there in 15 minutes. Traffic is bad.", 0),
    ("Don't forget to bring your ticket for the event.", 0),
    ("Thank you for your application. We'll review it and get back to you.", 0),
    ("Your appointment is confirmed for Monday at 10am.", 0),
    ("The package has been delivered. You can pick it up at reception.", 0),
    ("Please submit the report by end of day. Thanks for your work!", 0),
    ("Welcome to the team! We look forward to working with you.", 0)
]

# Combine and create DataFrame
all_messages = scam_messages + legit_messages
df = pd.DataFrame(all_messages, columns=['text', 'label'])
df['label_name'] = df['label'].map({1: 'scam', 0: 'legitimate'})

print(f"Created dataset with {len(df)} samples")
print(f"   - Scams: {len(df[df['label'] == 1])}")
print(f"   - Legitimate: {len(df[df['label'] == 0])}")

# ============ 2. TEXT PREPROCESSING ============
print("\nStep 2: Preprocessing text...")

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    return text

df['clean_text'] = df['text'].apply(preprocess_text)
print("Text preprocessing complete")

# ============ 3. TRAIN/TEST SPLIT ============
print("\nStep 3: Splitting data...")

X = df['clean_text']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

print(f"Training set: {len(X_train)} samples")
print(f"Testing set: {len(X_test)} samples")

# ============ 4. TRAIN MODELS ============
print("\nStep 4: Training models...")

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(kernel='linear', probability=True, random_state=42)
}

results = {}
best_model = None
best_score = 0

for name, model in models.items():
    print(f"\n   Training {name}...")
    
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words='english')),
        ('classifier', model)
    ])
    
    pipeline.fit(X_train, y_train)
    
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]
    
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)
    
    results[name] = {
        'pipeline': pipeline,
        'accuracy': accuracy,
        'roc_auc': roc_auc,
        'report': classification_report(y_test, y_pred, target_names=['legitimate', 'scam'])
    }
    
    print(f"   Accuracy: {accuracy:.4f}")
    print(f"   ROC-AUC: {roc_auc:.4f}")
    
    if accuracy > best_score:
        best_score = accuracy
        best_model = pipeline
        best_name = name

# ============ 5. SAVE BEST MODEL ============
print("\nStep 5: Saving models...")

vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words='english')
vectorizer.fit(X_train)

joblib.dump(vectorizer, '../../ml-models/scam_vectorizer.pkl')
joblib.dump(best_model, '../../ml-models/scam_classifier.pkl')

print(f"Best model: {best_name}")
print(f"Saved vectorizer to: ml-models/scam_vectorizer.pkl")
print(f"Saved classifier to: ml-models/scam_classifier.pkl")

# ============ 6. SAMPLE TESTS ============
print("\nStep 6: Testing on sample messages...")

test_samples = [
    "You have won R100,000! Click here to claim.",
    "Hi Mom, I'll be home at 6pm.",
    "Your account has been hacked! Send your password.",
    "Meeting at 2pm tomorrow in the boardroom."
]

print("\nSample Predictions:")
print("-" * 60)
for sample in test_samples:
    clean_sample = preprocess_text(sample)
    prob = best_model.predict_proba([clean_sample])[0][1]
    pred = "SCAM" if prob > 0.5 else "LEGITIMATE"
    print(f"Text: {sample[:50]}...")
    print(f"Prediction: {pred} (confidence: {prob:.2%})")
    print("-" * 60)

print("\n" + "=" * 60)
print("TRAINING COMPLETE!")
print("=" * 60)
