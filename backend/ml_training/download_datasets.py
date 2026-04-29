"""
Dataset downloader for phishing detection.
We use two public datasets:
1. Email dataset - UCI Spam/Phishing emails
2. URL dataset - PhishTank + legitimate URLs
"""

import pandas as pd
import requests
import os

DATASETS_DIR = os.path.join(os.path.dirname(__file__), "datasets")

def download_url_dataset():
    """
    Downloads a combined phishing + legitimate URL dataset.
    Source: A preprocessed version of PhishTank + Alexa top sites.
    We'll use a well-known public CSV for this.
    """
    print("📥 Downloading URL dataset...")

    # This is a popular phishing URL dataset used in research
    url = "https://raw.githubusercontent.com/GregaVrbancic/Phishing-Dataset/master/dataset_small.csv"

    try:
        response = requests.get(url, timeout=10)
        filepath = os.path.join(DATASETS_DIR, "url_dataset.csv")
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"✅ URL dataset saved to {filepath}")
    except Exception as e:
        print(f"❌ Failed to download: {e}")
        print("👉 Manually download from PhishTank: https://www.phishtank.com/developer_info.php")


def create_sample_email_dataset():
    """
    Creates a small sample email dataset for development.
    In production, use the Nazario Phishing Corpus or CEAS 2008 dataset.
    """
    print("📧 Creating sample email dataset...")

    data = {
        "text": [
            # Phishing emails
            "Urgent! Your account has been compromised. Click here to verify your identity immediately.",
            "Dear customer, your PayPal account is suspended. Login now to restore access: http://paypa1.fake.com",
            "You have won a prize! Claim your $1000 gift card now. Limited time offer!",
            "ALERT: Unusual sign-in activity detected. Verify your account or it will be deleted.",
            "Your bank account needs verification. Provide your SSN and password to continue.",
            "Congratulations! You've been selected for a free iPhone. Click to claim before it expires!",
            "Security warning: Your password expires today. Update it now via this link.",
            "IRS Notice: You owe back taxes. Pay immediately to avoid legal action.",
            "Your Netflix subscription failed. Update payment info to continue watching.",
            "Dear user, confirm your email address or your account will be permanently closed.",

            # Legitimate emails
            "Hi John, just following up on the project timeline we discussed in Monday's meeting.",
            "Your order #12345 has shipped and will arrive by Friday. Track it here.",
            "Meeting reminder: Team standup at 10 AM tomorrow in Conference Room B.",
            "Thank you for your purchase! Your receipt is attached for your records.",
            "Newsletter: Check out this month's top articles on technology and innovation.",
            "Your subscription renewal is coming up on March 15th. No action needed.",
            "Hi, I wanted to share the report we finished last week. Let me know your thoughts.",
            "Reminder: Your dentist appointment is scheduled for next Tuesday at 3 PM.",
            "Welcome to our platform! Here are some tips to get started.",
            "Your monthly statement is now available. Log in to view your account summary.",
        ],
        "label": [1,1,1,1,1,1,1,1,1,1,  # 1 = phishing
                  0,0,0,0,0,0,0,0,0,0]   # 0 = legitimate
    }

    df = pd.DataFrame(data)
    filepath = os.path.join(DATASETS_DIR, "email_dataset.csv")
    df.to_csv(filepath, index=False)
    print(f"✅ Sample email dataset saved to {filepath}")
    print("⚠️  Note: This is a tiny sample. For real training, use the Nazario Phishing Corpus.")
    return df


if __name__ == "__main__":
    os.makedirs(DATASETS_DIR, exist_ok=True)
    create_sample_email_dataset()
    download_url_dataset()