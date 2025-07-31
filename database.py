import psycopg2

def get_fixed_ingredients():
    conn = psycopg2.connect(
        host="localhost",
        database="dog_diet_db",
        user="postgres",
        password="Southern@2025"  # Update if needed
    )
    cursor = conn.cursor()
    cursor.execute("SELECT ingredient_name, group_name, dm_g, fat_g, protein_g, water_g, calcium_mg, iron_mg FROM fixed_ingredients")
    rows = cursor.fetchall()
    conn.close()

    ingredients = []
    for row in rows:
        ingredients.append({
            "ingredient_name": row[0],
            "group_name": row[1],
            "dm_g": row[2],
            "fat_g": row[3],
            "protein_g": row[4],
            "water_g": row[5],
            "calcium_mg": row[6],
            "iron_mg": row[7],
        })

    return ingredients
