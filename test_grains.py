import sqlite3

# Connect to database
conn = sqlite3.connect("dog_nutrition.db")
cursor = conn.cursor()

# Fetch all nutrients for Grains group
cursor.execute("""
SELECT ingredient, nutrient, unit, value
FROM meat_nutrients
WHERE main_group = 'Grains'
ORDER BY ingredient, id
""")

rows = cursor.fetchall()

# Print the results
current_ingredient = ""
for ingredient, nutrient, unit, value in rows:
    if ingredient != current_ingredient:
        print(f"\n🍚 Nutrients for: {ingredient}")
        current_ingredient = ingredient
    print(f"  - {nutrient} ({unit}): {value}")

conn.close()
