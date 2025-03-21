from flask import Flask, render_template, jsonify, request
import sqlite3
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables (API keys)
load_dotenv("twitter.env")

# Route to render the main page (real-time feedback analysis)
@app.route("/")
def index():
    return render_template("index.html")

# Route to render the sentiment analysis dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Route to fetch feedback and sentiment data from the database
@app.route("/feedbacks")
def feedbacks():
    conn = sqlite3.connect("customer_feedbacks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT feedback, sentiment FROM feedbacks;")
    feedbacks = cursor.fetchall()
    conn.close()
    return jsonify([{"text": f, "sentiment": s} for f, s in feedbacks])

# Route for real-time sentiment analysis using OpenAI/Groq APIs
@app.route("/analyze", methods=["POST"])
def analyze_sentiment():
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Fetch feedback text and location from the frontend
    data = request.json
    feedback_text = data.get("text")

    # Perform sentiment analysis using OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": feedback_text}]
    )
    sentiment = response["choices"][0]["message"]["content"]

    return jsonify({"sentiment": sentiment})

if __name__ == "__main__":
    app.run(debug=True)
