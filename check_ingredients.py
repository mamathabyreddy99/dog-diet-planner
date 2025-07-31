import sqlite3

conn = sqlite3.connect("dog_nutrition.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM ingredients")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
