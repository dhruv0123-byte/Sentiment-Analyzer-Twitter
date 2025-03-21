import sqlite3

conn = sqlite3.connect("customer_feedbacks.db")
cursor = conn.cursor()

try:
    cursor.execute("SELECT id, feedback FROM feedbacks;")
    rows = cursor.fetchall()

    print("\nCustomer Feedbacks:")
    for row in rows:
        print(f"ID: {row[0]}, Feedback: {row[1]}")
except sqlite3.Error as e:
    print(f"An error occurred: {e}")
finally:
    conn.close()
