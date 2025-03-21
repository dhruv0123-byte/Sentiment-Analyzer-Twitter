import sqlite3

conn = sqlite3.connect("customer_feedbacks.db")
cursor = conn.cursor()

# Check existing data
cursor.execute("SELECT id, feedback FROM feedbacks;")  # Sentiment hata diya
rows = cursor.fetchall()

for row in rows:
    print(row)  # Print all feedbacks

conn.close()
