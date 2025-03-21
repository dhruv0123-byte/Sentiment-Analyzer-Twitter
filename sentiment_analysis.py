import sqlite3
import os
import groq
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "twitter.env")
load_dotenv(dotenv_path)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing! Please check your .env file.")
groq_client = groq.Client(api_key=GROQ_API_KEY)

conn = sqlite3.connect("customer_feedbacks.db")
cursor = conn.cursor()

cursor.execute("SELECT id, feedback FROM feedbacks")
feedbacks = cursor.fetchall()

def analyze_sentiment(text):
    try:
        response = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "Analyze sentiment (positive, negative, neutral)."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content.strip().lower()
    except Exception as e:
        print(f"Error in Groq API: {e}")
        return "error"

cursor.execute("PRAGMA table_info(feedbacks);")
if "sentiment" not in [col[1] for col in cursor.fetchall()]:
    cursor.execute("ALTER TABLE feedbacks ADD COLUMN sentiment TEXT")
    conn.commit()

for feedback_id, text in feedbacks:
    sentiment = analyze_sentiment(text)
    cursor.execute("UPDATE feedbacks SET sentiment = ? WHERE id = ?", (sentiment, feedback_id))
    conn.commit()

conn.close()
print("✅ Sentiment analysis completed and stored in the database!")
