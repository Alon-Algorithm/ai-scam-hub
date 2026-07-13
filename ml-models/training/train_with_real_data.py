import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
from sklearn.pipeline import Pipeline
import joblib
import re
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("AI SCAM DETECTOR - TRAINING WITH REAL DATA")
print("=" * 60)

# ============ 1. LOAD REAL DATA ============
print("\n📊 Step 1: Loading real dataset...")

# Try to load real data first
try:
    # Load the UCI SMS Spam dataset
    df = pd.read_csv('../data/sms_spam_dataset.csv')
    print(f"✅ Loaded real dataset: {len(df)} messages")
    print(f"   - Scam/Spam: {len(df[df['label'] == 1])}")
    print(f"   - Legitimate/Ham: {len(df[df['label'] == 0])}")
    
except FileNotFoundError:
    print("⚠️  Real dataset not found. Using sample data...")
    
    # Fallback to sample data
    scam_messages = [
        ("Congratulations! You have won R100,000!", 1),
        ("URGENT: Your bank account has been suspended.", 1),
        ("You have been selected for a cash prize of ,000.", 1),
        ("Work from home! Earn R50,000 per month.", 1),
        ("Your PayPal account has been limited.", 1),
    ]
    legit_messages = [
        ("Hi Mom, I'll be home for dinner at 6pm.", 0),
        ("The meeting is at 2pm tomorrow.", 0),
        ("Happy birthday! Hope you have an amazing day!", 0),
        ("Can we reschedule today's meeting to 3pm?", 0),
        ("Thanks for the gift! I really appreciate it.", 0),
    ]
    all_messages = scam_messages + legit_messages
    df = pd.DataFrame(all_messages, columns=['text', 'label'])

# ============ 2. TEXT PREPROCESSING ============
print("\n🔧 Step 2: Preprocessing text...")

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    return text

df['clean_text'] = df['text'].apply(preprocess_text)
print("✅ Text preprocessing complete")

# ============ 3. TRAIN/TEST SPLIT ============
print("\n📊 Step 3: Splitting data...")

X = df['clean_text']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"✅ Training set: {len(X_train)} samples")
print(f"✅ Testing set: {len(X_test)} samples")

# ============ 4. TRAIN MODELS ============
print("\n🤖 Step 4: Training models...")

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
}

results = {}
best_model = None
best_score = 0

for name, model in models.items():
    print(f"\n   Training {name}...")
    
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(
            max_features=5000, 
            ngram_range=(1, 2), 
            stop_words='english'
        )),
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
    
    print(f"   ✅ Accuracy: {accuracy:.4f}")
    print(f"   ✅ ROC-AUC: {roc_auc:.4f}")
    
    if accuracy > best_score:
        best_score = accuracy
        best_model = pipeline
        best_name = name

# ============ 5. SAVE BEST MODEL ============
print("\n💾 Step 5: Saving models...")

vectorizer = TfidfVectorizer(
    max_features=5000, 
    ngram_range=(1, 2), 
    stop_words='english'
)
vectorizer.fit(X_train)

# Save to the backend's ml-models folder
joblib.dump(vectorizer, '../../ml-models/scam_vectorizer.pkl')
joblib.dump(best_model, '../../ml-models/scam_classifier.pkl')

print(f"✅ Best model: {best_name}")
print(f"✅ Accuracy: {best_score:.2%}")
print(f"✅ Saved to: ml-models/")

# ============ 6. FEATURE IMPORTANCE ============
print("\n📊 Step 6: Analyzing important features...")

if hasattr(best_model.named_steps['classifier'], 'coef_'):
    feature_names = vectorizer.get_feature_names_out()
    coefficients = best_model.named_steps['classifier'].coef_[0]
    
    # Get top scam indicators
    top_scam_idx = np.argsort(coefficients)[-10:][::-1]
    top_scam_words = [feature_names[i] for i in top_scam_idx]
    
    print("\n🔴 Top Scam Indicators:")
    for word in top_scam_words:
        print(f"   - {word}")

# ============ 7. TEST ON REAL MESSAGES ============
print("\n🧪 Step 7: Testing on sample messages...")

test_messages = [
    "Congratulations! You have won ,000,000 in our lottery!",
    "Your account has been compromised. Click here to verify.",
    "Hi Mom, I'll be home for dinner at 6pm.",
    "You've been selected for a free iPhone! Send your address.",
    "Meeting at 2pm tomorrow in the boardroom.",
    "URGENT: Your bank account has been locked. Verify now.",
    "Thanks for the gift! I really appreciate it.",
]

print("\n📝 Test Results:")
print("-" * 70)
for msg in test_messages:
    clean_msg = preprocess_text(msg)
    prob = best_model.predict_proba([clean_msg])[0][1]
    pred = "⚠️ SCAM" if prob > 0.5 else "✅ LEGITIMATE"
    confidence = prob if prob > 0.5 else 1 - prob
    print(f"{pred:15} | {confidence:6.1%} | {msg[:50]}...")
print("-" * 70)

print("\n" + "=" * 60)
print("🎉 TRAINING COMPLETE!")
print("=" * 60)
