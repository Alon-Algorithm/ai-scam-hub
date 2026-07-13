import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score, confusion_matrix
from sklearn.pipeline import Pipeline
import joblib
import re
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("AI SCAM DETECTOR - TRAINING WITH REAL DATA")
print("=" * 60)

# ============ STEP 1: LOAD REAL DATA ============
print("\n📊 Step 1: Loading real dataset...")

def load_data():
    """Load and prepare training data"""
    
    # Sample data - REPLACE with your real data
    scam_samples = [
        # Financial scams with varied wording
        ("Congratulations! You have won a lottery prize of $1,000,000.", 1),
        ("You are the lucky winner of our annual cash prize drawing.", 1),
        ("Your account has been selected for a special reward of $500,000.", 1),
        ("We are pleased to inform you that you have won our grand prize.", 1),
        ("Your name was drawn in our international lottery. You win $2,000,000.", 1),
        ("You have been randomly selected as the winner of our sweepstakes.", 1),
        ("Congratulations, you are the winner of our online promotion.", 1),
        
        # Nigerian Prince variations - different wording, same pattern
        ("I am a wealthy businessman from overseas needing assistance with a large financial transaction. I will compensate you generously.", 1),
        ("I am a foreign national with a large inheritance that I need help moving out of my country. You will receive a percentage.", 1),
        ("I am a government official with access to funds that need to be transferred abroad. Your help is needed.", 1),
        ("I need a trusted partner to help with a confidential business matter involving large sums of money.", 1),
        ("I am a contractor who has been overpaid by the government and need a foreign account to receive the funds.", 1),
        ("My late husband left me a fortune, but I need help transferring it out of my country. I will share it with you.", 1),
        ("I am a diplomat who has discovered a large sum of money that needs to be moved secretly. I need your help.", 1),
        ("A wealthy client of mine died without heirs. I need a foreign partner to claim the inheritance.", 1),
        ("I represent a foreign company looking for a local partner to handle a large financial transaction.", 1),
        ("I have a confidential business proposal that involves moving funds across borders. You will be rewarded.", 1),
        
        # Banking phishing
        ("Your bank account has been suspended. Click here to verify your identity.", 1),
        ("We have detected unusual activity on your account. Please confirm your details.", 1),
        ("Your account is at risk. Please click the link to secure it.", 1),
        ("Urgent: Your credit card has been compromised. Call this number immediately.", 1),
        ("We need to verify your identity to prevent your account from being closed.", 1),
        ("There is a problem with your payment method. Please update your information.", 1),
        ("Your account will be suspended unless you verify your identity within 24 hours.", 1),
        
        # Job scams
        ("Work from home and earn $50,000 per month with no experience needed.", 1),
        ("Easy money online! Get paid $100 per hour working from home.", 1),
        ("We are hiring urgently with amazing salaries. No qualifications needed.", 1),
        ("Become a millionaire with our proven system. Start making money today.", 1),
        ("Make $10,000 per week with this simple method that anyone can do.", 1),
        ("We need people immediately for high-paying jobs with no experience required.", 1),
        ("Get rich quick with our exclusive investment opportunity.", 1),
        ("We have a job for you that pays $50/hour working from your phone.", 1),
        
        # Social engineering scams
        ("I need your help urgently. My family is in trouble and I need money.", 1),
        ("Please help me, I am stranded and need funds to get home.", 1),
        ("Your brother called me saying he is in trouble and needs money.", 1),
        ("I am in the hospital and need money for medical treatment.", 1),
        ("There is a family emergency and I need you to send money immediately.", 1),
        ("I trust you more than anyone. I need your help with a personal matter.", 1),
        
        # WhatsApp/Text scams
        ("You won an iPhone 15! Click here to claim your prize.", 1),
        ("Free money! Share this message with 10 people and send $50.", 1),
        ("You have been selected for a cash prize. Reply with your details.", 1),
        ("Click this link to claim your free gift.", 1),
        ("Your account has been compromised. Send your password to secure it.", 1),
        ("We have a surprise for you. Click here to see what you won.", 1),
        
        # MORE Nigerian Prince variations
        ("I am a prince from a wealthy country who needs to move funds abroad. I will reward you.", 1),
        ("Help me transfer $5,000,000 out of my country and you keep 30%", 1),
        ("I have $10,000,000 from my late father that I want to invest overseas. I need your help.", 1),
        ("I am a successful businessman wanting to invest in your country. I need a partner.", 1),
        ("There is a large sum of money waiting to be claimed. I need you to be the recipient.", 1),
        ("I am a refugee with valuable assets in a foreign bank. I need help accessing them.", 1),
        ("I was a government minister with access to funds. I need a safe way to move them.", 1),
        ("I inherited a fortune but need a foreigner to help me access it.", 1),
        ("I represent a company that overpaid for supplies and need to move the surplus.", 1),
        ("I need to move money out of my country due to political instability. Can you help?", 1),
    ]
    
    # Legitimate samples
    legit_samples = [
        ("Hi Mom, I'll be home for dinner at 6pm.", 0),
        ("Can we meet for coffee this weekend?", 0),
        ("The meeting is at 2pm tomorrow.", 0),
        ("I'll be there in 10 minutes.", 0),
        ("Please bring your laptop to the meeting.", 0),
        ("Happy birthday! Hope you have an amazing day.", 0),
        ("Thanks for the gift. I really appreciate it.", 0),
        ("Let's catch up soon.", 0),
        ("How are you doing?", 0),
        ("Just checking in on you.", 0),
        ("The project deadline is Friday.", 0),
        ("Please submit the report by end of day.", 0),
        ("Great job on the presentation!", 0),
        ("Welcome to the team!", 0),
        ("Your order has been shipped.", 0),
        ("Your package will arrive tomorrow.", 0),
        ("The doctor's appointment is confirmed.", 0),
        ("Thank you for your application. We'll review it.", 0),
        ("I'll send you the invoice later.", 0),
        ("Let me know if you need any help.", 0),
        ("The party starts at 7pm.", 0),
        ("Don't forget to bring your ID.", 0),
        ("The weather is beautiful today.", 0),
        ("I'll call you back later.", 0),
        ("Please RSVP by Friday.", 0),
    ]
    
    # Create DataFrame
    all_samples = scam_samples + legit_samples
    df = pd.DataFrame(all_samples, columns=['text', 'label'])
    
    print(f"✅ Loaded {len(df)} samples")
    print(f"   - Scams: {len(df[df['label'] == 1])}")
    print(f"   - Legitimate: {len(df[df['label'] == 0])}")
    
    return df

df = load_data()

# ============ STEP 2: TEXT PREPROCESSING ============
print("\n🔧 Step 2: Preprocessing text...")

def preprocess_text(text):
    """Clean and preprocess text - only basic cleaning"""
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    return text

df['clean_text'] = df['text'].apply(preprocess_text)
print("✅ Text preprocessing complete")

# ============ STEP 3: TRAIN/TEST SPLIT ============
print("\n📊 Step 3: Splitting data...")

X = df['clean_text']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"✅ Training set: {len(X_train)} samples")
print(f"✅ Testing set: {len(X_test)} samples")

# ============ STEP 4: TRAIN MODELS ============
print("\n🤖 Step 4: Training models...")

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42, C=1.0),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=5),
}

results = {}
best_model = None
best_score = 0

for name, model in models.items():
    print(f"\n   Training {name}...")
    
    # Create pipeline with TF-IDF and classifier
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 3),  # Unigrams, bigrams, trigrams
            stop_words='english',
            use_idf=True,
            smooth_idf=True,
            sublinear_tf=True
        )),
        ('classifier', model)
    ])
    
    pipeline.fit(X_train, y_train)
    
    # Evaluate
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

# ============ STEP 5: SAVE BEST MODEL ============
print("\n💾 Step 5: Saving models...")

# Save the vectorizer and best model
vectorizer = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 3),
    stop_words='english',
    use_idf=True,
    smooth_idf=True,
    sublinear_tf=True
)
vectorizer.fit(X_train)

joblib.dump(vectorizer, '../../ml-models/scam_vectorizer.pkl')
joblib.dump(best_model, '../../ml-models/scam_classifier.pkl')

print(f"✅ Best model: {best_name}")
print(f"✅ Accuracy: {best_score:.2%}")
print(f"✅ Saved to: ml-models/")

# ============ STEP 6: FEATURE IMPORTANCE ============
print("\n📊 Step 6: Analyzing important features...")

if hasattr(best_model.named_steps['classifier'], 'coef_'):
    feature_names = vectorizer.get_feature_names_out()
    coefficients = best_model.named_steps['classifier'].coef_[0]
    
    # Get top scam indicators (highest positive coefficients)
    top_scam_idx = np.argsort(coefficients)[-20:][::-1]
    top_scam_words = [feature_names[i] for i in top_scam_idx]
    
    print("\n🔴 Top Scam Indicators (ML learned):")
    for word in top_scam_words[:15]:
        print(f"   - {word}")

# ============ STEP 7: CONFUSION MATRIX ============
print("\n📊 Step 7: Confusion Matrix...")

y_pred = best_model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
print(f"\n   True Negatives: {cm[0][0]}")
print(f"   False Positives: {cm[0][1]}")
print(f"   False Negatives: {cm[1][0]}")
print(f"   True Positives: {cm[1][1]}")

# ============ STEP 8: TEST ON SAMPLE MESSAGES ============
print("\n🧪 Step 8: Testing on sample messages...")

test_messages = [
    # High risk
    "I am a wealthy businessman from overseas needing assistance with a large financial transaction.",
    "Congratulations! You have won a lottery prize of $1,000,000.",
    "Your bank account has been suspended. Click here to verify.",
    "Work from home and earn $50,000 per month with no experience.",
    "I need your help urgently. My family is in trouble and I need money.",
    
    # Low risk
    "Hi Mom, I'll be home for dinner at 6pm.",
    "The meeting is at 2pm tomorrow.",
    "Thanks for the gift. I really appreciate it.",
    "The weather is beautiful today.",
    "Just checking in on you.",
]

print("\n📝 Test Results:")
print("-" * 70)
for msg in test_messages:
    clean_msg = preprocess_text(msg)
    prob = best_model.predict_proba([clean_msg])[0][1]
    pred = "⚠️ SCAM" if prob > 0.5 else "✅ LEGIT"
    risk = "HIGH" if prob > 0.7 else "MEDIUM" if prob > 0.3 else "LOW"
    print(f"{pred:12} | {risk:6} | {prob:6.1%} | {msg[:45]}...")
print("-" * 70)

print("\n" + "=" * 60)
print("🎉 TRAINING COMPLETE!")
print("=" * 60)
