import sqlite3

conn = sqlite3.connect("dog_nutrition.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS ingredients;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    main_group TEXT NOT NULL,
    sub_group TEXT,
    water REAL,
    energy REAL,
    protein REAL,
    total_lipid_fat REAL,
    ash REAL,
    cho REAL,
    fiber_total_dietary REAL,
    calcium_ca REAL,
    iron_fe REAL,
    magnesium_mg REAL,
    phosphorus_p REAL,
    potassium_k REAL,
    sodium_na REAL,
    zinc_zn REAL,
    copper_cu REAL,
    iodine REAL,
    selenium_se_ug REAL,
    thiamin REAL,
    riboflavin REAL,
    niacin REAL,
    pantothenic_acid REAL,
    vitamin_b6 REAL,
    folate_total_ug REAL,
    choline_total REAL,
    vitamin_b12_ug REAL,
    vitamin_a_iu REAL,
    vitamin_e_alpha_tocopherol REAL,
    vitamin_d_d2_d3_iu REAL,
    pufa_18_2 REAL,
    pufa_18_3 REAL,
    pufa_20_5_n3_epa REAL,
    pufa_22_6_n3_dha REAL,
    tryptophan REAL,
    threonine REAL,
    isoleucine REAL,
    leucine REAL,
    lysine REAL,
    methionine REAL,
    cystine REAL,
    phenylalanine REAL,
    tyrosine REAL,
    valine REAL,
    arginine REAL
);
""")

conn.commit()
conn.close()

print("Ingredients table created with groups and detailed nutrients.")
