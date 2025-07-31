import sqlite3

conn = sqlite3.connect("dog_nutrition.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS ingredients;")

conn.commit()
conn.close()

print("Old ingredients table dropped successfully (if it existed).")
