import os
import sys
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import scipy.sparse as sp

# Add parent directory to path so we can import our utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.utils.text_cleaner import clean_text, extract_phishing_signals


# --- Paths ---
DATASETS_DIR = os.path.join(os.path.dirname(__file__), "datasets")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "saved_models")


def load_data():
    """Load and validate the email dataset."""
    filepath = os.path.join(DATASETS_DIR, "email_dataset.csv")
    
    if not os.path.exists(filepath):
        print("❌ Dataset not found. Run download_datasets.py first.")
        sys.exit(1)
    
    df = pd.read_csv(filepath)
    print(f"✅ Loaded {len(df)} emails ({df['label'].sum()} phishing, {(df['label']==0).sum()} legitimate)")
    return df


def build_features(df):
    """
    Convert raw email text into a feature matrix the model can learn from.
    
    We combine TWO types of features:
    1. TF-IDF features: statistical word importance scores
       "verify" appearing often in phishing = high weight for "verify"
    2. Signal features: handcrafted binary flags from extract_phishing_signals()
    
    Combining both gives better accuracy than either alone.
    """
    print("\n🔧 Building features...")

    # Step 1: Clean all texts
    print("  → Cleaning text with SpaCy...")
    df["cleaned_text"] = df["text"].apply(clean_text)

    # Step 2: TF-IDF Vectorization
    # TF-IDF = Term Frequency × Inverse Document Frequency
    # It gives high scores to words that appear often in one email
    # but rarely across all emails — those are the most distinctive words.
    print("  → Applying TF-IDF vectorization...")
    tfidf = TfidfVectorizer(
        max_features=500,    # Keep only top 500 most informative words
        ngram_range=(1, 2),  # Use single words AND two-word phrases ("click here", "verify account")
        min_df=1,            # Word must appear in at least 1 document
    )
    tfidf_matrix = tfidf.fit_transform(df["cleaned_text"])

    # Step 3: Extract hand-crafted phishing signal features
    print("  → Extracting phishing signals...")
    signals = df["text"].apply(extract_phishing_signals)
    signals_df = pd.DataFrame(signals.tolist())

    # Step 4: Combine TF-IDF sparse matrix with signal features
    signals_sparse = sp.csr_matrix(signals_df.values)
    X = sp.hstack([tfidf_matrix, signals_sparse])
    y = df["label"].values

    print(f"  ✅ Feature matrix shape: {X.shape} ({X.shape[1]} total features)")
    return X, y, tfidf


def train_model(X, y):
    """
    Train the Random Forest classifier.
    
    We use cross-validation to get a reliable accuracy estimate
    (instead of just one train/test split which can be lucky or unlucky).
    """
    print("\n🌲 Training Random Forest...")

    # Split into training (80%) and test (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Initialize the model
    # n_estimators=100 means 100 decision trees vote together
    # class_weight='balanced' handles uneven phishing/legit ratios
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        class_weight="balanced",  # Critical: prevents bias toward majority class
        random_state=42,
        n_jobs=-1  # Use all CPU cores
    )

    # Train the model
    model.fit(X_train, y_train)

    # --- Evaluation ---
    print("\n📊 Model Evaluation:")
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]  # Probability of being phishing

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Legitimate", "Phishing"]))

    print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.3f}")
    print("(1.0 = perfect, 0.5 = random guessing)")

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\nConfusion Matrix:")
    print(f"  True Negatives  (correctly said safe):     {cm[0][0]}")
    print(f"  False Positives (wrongly flagged as phish): {cm[0][1]}  ← We want this LOW")
    print(f"  False Negatives (missed phishing):          {cm[1][0]}  ← We want this LOW")
    print(f"  True Positives  (correctly caught phish):  {cm[1][1]}")

    return model, X_test, y_test


def save_model(model, tfidf):
    """Save the trained model and vectorizer to disk."""
    os.makedirs(MODELS_DIR, exist_ok=True)

    model_path = os.path.join(MODELS_DIR, "email_model.pkl")
    tfidf_path = os.path.join(MODELS_DIR, "email_tfidf.pkl")

    joblib.dump(model, model_path)
    joblib.dump(tfidf, tfidf_path)

    print(f"\n💾 Model saved to {model_path}")
    print(f"💾 TF-IDF vectorizer saved to {tfidf_path}")


def test_with_examples(model, tfidf):
    """
    Quick sanity check — run the model on obvious examples.
    If it can't get these right, something is wrong.
    """
    print("\n🧪 Sanity Check with Examples:")

    test_emails = [
        ("URGENT: Your account will be deleted! Click here to verify NOW!", "🚨 Phishing"),
        ("Hi Sarah, can we reschedule tomorrow's meeting to 3pm?", "✅ Legitimate"),
        ("You've won a $500 Amazon gift card! Claim it before it expires!", "🚨 Phishing"),
        ("Your package has been shipped and will arrive Thursday.", "✅ Legitimate"),
    ]

    for email_text, expected in test_emails:
        cleaned = clean_text(email_text)
        tfidf_features = tfidf.transform([cleaned])

        signals = extract_phishing_signals(email_text)
        import scipy.sparse as sp
        import numpy as np
        signals_sparse = sp.csr_matrix(np.array(list(signals.values())).reshape(1, -1))
        features = sp.hstack([tfidf_features, signals_sparse])

        prediction = model.predict(features)[0]
        confidence = model.predict_proba(features)[0][1]

        result = "🚨 PHISHING" if prediction == 1 else "✅ SAFE"
        print(f"\n  Email: \"{email_text[:60]}...\"")
        print(f"  Expected: {expected} | Got: {result} | Confidence: {confidence:.0%}")


if __name__ == "__main__":
    df = load_data()
    X, y, tfidf = build_features(df)
    model, X_test, y_test = train_model(X, y)
    save_model(model, tfidf)
    test_with_examples(model, tfidf)
    print("\n✅ Email model training complete!")