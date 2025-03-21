import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

conn = sqlite3.connect("customer_feedbacks.db")
df = pd.read_sql_query("SELECT feedback FROM feedbacks;", conn)
conn.close()

text = " ".join(df["feedback"])
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Customer Feedback WordCloud")
plt.show()
