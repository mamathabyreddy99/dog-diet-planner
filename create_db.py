import sqlite3

conn = sqlite3.connect('dog_nutrition.db')  # Creates the DB file or opens if exists
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    main_group TEXT NOT NULL,
    sub_group TEXT,
    mandatory BOOLEAN DEFAULT 0,
    fixed_amount_g REAL DEFAULT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS nutrients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_id INTEGER NOT NULL,
    water REAL,
    energy_kcal REAL,
    protein REAL,
    fat REAL,
    fiber REAL,
    calcium REAL,
    iron REAL,
    magnesium REAL,
    phosphorus REAL,
    potassium REAL,
    sodium REAL,
    zinc REAL,
    copper REAL,
    iodine REAL,
    selenium REAL,
    thiamin REAL,
    riboflavin REAL,
    niacin REAL,
    pantothenic_acid REAL,
    vitamin_b6 REAL,
    folate REAL,
    choline REAL,
    vitamin_b12 REAL,
    vitamin_a REAL,
    vitamin_e REAL,
    vitamin_d REAL,
    pufa_18_2 REAL,
    pufa_18_3 REAL,
    pufa_20_5 REAL,
    pufa_22_6 REAL,
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
    arginine REAL,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
)
''')

conn.commit()
conn.close()

print("Database tables created successfully!")
