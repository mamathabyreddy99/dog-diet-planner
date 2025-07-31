import pandas as pd
import psycopg2

# Load CSV
df = pd.read_csv("Formatted_Ingredient_Data (2).csv")

# Rename columns to match DB schema
column_map = {
    
    "Water": "water_g",
    "Energy": "energy_kcal",
    "Protein": "protein_g",
    "Total lipid (fat)": "fat_g",  # <- this is the exact column from your error
    "Ash": "ash_g",
    "Carbohydrate": "cho_g",
    "Fiber": "fiber_g",
    "Calcium, Ca": "calcium_mg",
    "Iron, Fe": "iron_mg",
    "Phosphorus, P": "phosphorus_mg",
    "Potassium, K": "potassium_mg",
    "Sodium, Na": "sodium_mg",
    "Zinc, Zn": "zinc_mg",
    "Copper, Cu": "copper_mg",
    "Iodine, I": "iodine_mg",
    "Selenium, Se": "selenium_mg",
    "Thiamin (B1)": "thiamin_mg",
    "Riboflavin (B2)": "riboflavin_mg",
    "Niacin (B3)": "niacin_mg",
    "Pantothenic acid (B5)": "pantothenic_acid_mg",
    "Vitamin B6": "vitamin_b6_mg",
    "Folate": "folate_ug",
    "Choline": "choline_mg",
    "Vitamin B12": "vitamin_b12_ug",
    "Vitamin A": "vitamin_a_iu",
    "Vitamin E": "vitamin_e_mg",
    "Vitamin D": "vitamin_d_iu",
    "Omega-6 (18:2)": "pufa_18_2_g",
    "Omega-3 (18:3)": "pufa_18_3_g",
    "EPA (20:5)": "pufa_20_5_g",
    "DHA (22:6)": "pufa_22_6_g",
    "Tryptophan": "tryptophan_g",
    "Threonine": "threonine_g",
    "Isoleucine": "isoleucine_g",
    "Leucine": "leucine_g",
    "Lysine": "lysine_g",
    "Methionine": "methionine_g",
    "Cystine": "cystine_g",
    "Phenylalanine": "phenylalanine_g",
    "Tyrosine": "tyrosine_g",
    "Valine": "valine_g",
    "Arginine": "arginine_g",
    "Magnesium, Mg": "magnesium_mg"
}



df.rename(columns=column_map, inplace=True)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="dog_diet_db",
    user="postgres",
    password="Southern@2025"
)
cursor = conn.cursor()

# Prepare and insert rows
for _, row in df.iterrows():
    placeholders = ", ".join(["%s"] * len(row))
    columns = ", ".join(row.index)
    sql = f"INSERT INTO user_ingredients ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, tuple(row))

conn.commit()
cursor.close()
conn.close()

print("✅ All new ingredients inserted successfully.")
