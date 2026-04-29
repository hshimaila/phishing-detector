import os
import sys
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.utils.url_parser import extract_url_features

DATASETS_DIR = os.path.join(os.path.dirname(__file__), "datasets")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "saved_models")


def load_data():
    """
    Load URL dataset.
    Expected CSV format: columns 'url' and 'label' (1=phishing, 0=legit)
    """
    filepath = os.path.join(DATASETS_DIR, "url_dataset.csv")
    
    if not os.path.exists(filepath):
        print("⚠️  URL dataset not found. Creating a small sample dataset...")
        return create_sample_url_dataset()
    
    df = pd.read_csv(filepath)

    # Normalize column names — different datasets use different naming
    df.columns = df.columns.str.lower().str.strip()
    
    # Try to find the URL and label columns
    url_col = next((c for c in df.columns if 'url' in c), None)
    label_col = next((c for c in df.columns if 'label' in c or 'class' in c or 'status' in c), None)
    
    if not url_col or not label_col:
        print(f"Available columns: {df.columns.tolist()}")
        print("⚠️  Could not find URL/label columns. Using sample dataset.")
        return create_sample_url_dataset()

    df = df[[url_col, label_col]].rename(columns={url_col: "url", label_col: "label"})
    
    # Ensure binary labels
    df["label"] = (df["label"] != 0).astype(int)
    df = df.dropna()

    print(f"✅ Loaded {len(df)} URLs ({df['label'].sum()} phishing, {(df['label']==0).sum()} legitimate)")
    return df


def create_sample_url_dataset():
    """Fallback sample dataset if download failed."""
    data = {
        "url": [
            # Phishing URLs
            "http://paypa1.verify-login.tk/secure/account",
            "http://192.168.1.1/login/bank/verify",
            "http://amazon-security-alert.xyz/update-payment",
            "http://netfl1x.account-verify.ml/signin",
            "http://apple-id.verify-now.top/confirm",
            "http://google.com.login.fake-site.tk/auth",
            "http://secure-bankofamerica.login-verify.cf/update",
            "http://microsoft-account.verify.gq/password-reset",

            # Legitimate URLs
            "https://www.google.com/search?q=python",
            "https://github.com/user/repository",
            "https://www.amazon.com/products",
            "https://mail.google.com/mail/inbox",
            "https://www.linkedin.com/in/profile",
            "https://stackoverflow.com/questions/12345",
            "https://www.wikipedia.org/wiki/Machine_learning",
            "https://docs.python.org/3/library/",
        ],
        "label": [1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0]
    }
    return pd.DataFrame(data)


def build_features(df):
    """Extract structured feature vectors from all URLs."""
    print("\n🔧 Extracting URL features...")

    features_list = []
    for url in df["url"]:
        features = extract_url_features(str(url))
        features_list.append(features)

    X = pd.DataFrame(features_list).fillna(0)
    y = df["label"].values

    print(f"✅ Feature matrix: {X.shape[0]} URLs × {X.shape[1]} features")
    print(f"Features used: {X.columns.tolist()}")
    return X, y, X.columns.tolist()


def train_model(X, y):
    """Train and evaluate the URL classifier."""
    print("\n🌲 Training URL Random Forest...")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # Evaluation
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print("\n📊 Model Evaluation:")
    print(classification_report(y_test, y_pred, target_names=["Legitimate", "Phishing"]))
    print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.3f}")

    # Feature importance — shows WHICH URL features matter most
    feature_names = X.columns.tolist()
    importances = model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]

    print("\n🔍 Top 5 Most Important URL Features:")
    for i in range(min(5, len(feature_names))):
        idx = sorted_idx[i]
        print(f"  {i+1}. {feature_names[idx]}: {importances[idx]:.3f}")

    return model


def save_model(model, feature_names):
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    joblib.dump(model, os.path.join(MODELS_DIR, "url_model.pkl"))
    joblib.dump(feature_names, os.path.join(MODELS_DIR, "url_feature_names.pkl"))
    
    print(f"\n💾 URL model saved to {MODELS_DIR}/url_model.pkl")


def test_with_examples(model, feature_names):
    """Quick sanity check on obvious URLs."""
    print("\n🧪 Sanity Check:")

    test_urls = [
        ("http://paypa1.verify-login.tk/secure", "🚨 Phishing"),
        ("https://www.google.com/search", "✅ Legitimate"),
        ("http://192.168.0.1/bank/login/verify", "🚨 Phishing"),
        ("https://github.com/user/repo", "✅ Legitimate"),
    ]

    for url, expected in test_urls:
        features = extract_url_features(url)
        X = pd.DataFrame([features])[feature_names].fillna(0)

        pred = model.predict(X)[0]
        conf = model.predict_proba(X)[0][1]
        result = "🚨 PHISHING" if pred == 1 else "✅ SAFE"

        print(f"\n  URL: {url}")
        print(f"  Expected: {expected} | Got: {result} | Confidence: {conf:.0%}")


if __name__ == "__main__":
    df = load_data()
    X, y, feature_names = build_features(df)
    model = train_model(X, y)
    save_model(model, feature_names)
    test_with_examples(model, feature_names)
    print("\n✅ URL model training complete!")