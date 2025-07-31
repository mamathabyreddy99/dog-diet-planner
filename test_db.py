import sqlite3

conn = sqlite3.connect("dog_nutrition.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables in DB:", cursor.fetchall())

cursor.execute("SELECT * FROM ingredients_wide LIMIT 5;")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
