import psycopg2
import pandas as pd

# Load from Excel
excel_path = "Template-2 for homemade diet-Mamatha.xlsx"
df = pd.read_excel(excel_path, sheet_name="For dogs (6)", header=None)

# Extract rows 33 to 63 (index 32 to 62), columns B to M (1 to 12)
ingredient_data = df.iloc[32:63, 1:13]
ingredient_data.columns = [
    "Ingredient",         # Column B
    "Fresh_weight_g",     # Column C
    "Water_percent",      # Column D
    "DM_weight_g",        # Column E
    "Energy_kcal",        # Column F
    "Protein_g",          # Column G
    "Fat_g",              # Column H
    "Ash_g",              # Column I
    "CHO_g",              # Column J
    "Fiber_g",            # Column K
    "Calcium_mg",         # Column L
    "Iron_mg"             # Column M
]

# Drop rows with missing ingredient names
ingredient_data = ingredient_data.dropna(subset=["Ingredient"])

# Remove header row inside data if present
ingredient_data = ingredient_data[~ingredient_data["Ingredient"].str.contains("Ingredient|amounts", na=False)]

# Convert all columns to correct types
cols_to_convert = ingredient_data.columns[1:]
ingredient_data[cols_to_convert] = ingredient_data[cols_to_convert].apply(pd.to_numeric, errors='coerce')

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="dog_diet_db",
    user="postgres",
    password="Southern@2025"  # 🔐 change if needed
)
cur = conn.cursor()

# Create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS fixed_ingredients (
        id SERIAL PRIMARY KEY,
        ingredient TEXT,
        fresh_weight_g REAL,
        water_percent REAL,
        dm_weight_g REAL,
        energy_kcal REAL,
        protein_g REAL,
        fat_g REAL,
        ash_g REAL,
        cho_g REAL,
        fiber_g REAL,
        calcium_mg REAL,
        iron_mg REAL
    );
""")

# Insert rows
for _, row in ingredient_data.iterrows():
    cur.execute("""
        INSERT INTO fixed_ingredients (
            ingredient, fresh_weight_g, water_percent, dm_weight_g,
            energy_kcal, protein_g, fat_g, ash_g, cho_g, fiber_g,
            calcium_mg, iron_mg
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

# Commit and close
conn.commit()
cur.close()
conn.close()

print("✅ Fixed ingredients loaded into PostgreSQL successfully.")
