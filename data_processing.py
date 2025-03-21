import os
import sqlite3
import pandas as pd
import nltk
import openai
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv("C:\\Users\\mahes\\sd\\twitter\\twitter.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not OPENAI_API_KEY or not GROQ_API_KEY:
    raise ValueError("API keys are missing! Please check your .env file.")

# Sample customer feedback
customer_feedbacks = [
    "I love the product! It's amazing and works perfectly.",
    "Worst experience ever! The service was terrible.",
    "The delivery was fast, but the packaging was damaged.",
    "Amazing support team! They helped me with my issue quickly.",
    "Product quality is not as expected. Disappointed!"
]

# Download NLTK resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

# Text preprocessing
def preprocess_text(text):
    text = text.lower()
    words = word_tokenize(text)
    words = [word for word in words if word.isalnum() and word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(words)

# Clean and preprocess the feedback
cleaned_feedbacks = [preprocess_text(text) for text in customer_feedbacks]

# Save feedbacks to CSV
df = pd.DataFrame({"original": customer_feedbacks, "cleaned": cleaned_feedbacks})
df.to_csv("customer_feedbacks.csv", index=False)

# Store feedbacks in SQLite database
conn = sqlite3.connect("customer_feedbacks.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedbacks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original TEXT,
        cleaned TEXT
    )
""")

for original, cleaned in zip(customer_feedbacks, cleaned_feedbacks):
    cursor.execute("INSERT INTO feedbacks (original, cleaned) VALUES (?, ?)", (original, cleaned))

conn.commit()
conn.close()

print("Data processing complete! Feedback stored in CSV and database.")
