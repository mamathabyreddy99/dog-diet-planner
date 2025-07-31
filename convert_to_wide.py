import sqlite3
import pandas as pd

DB_PATH = "dog_nutrition.db"

def convert_long_to_wide():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM meat_nutrients", conn)
    conn.close()

    # Aggregate duplicates by taking the mean of 'value'
    df = df.groupby(["ingredient", "nutrient"], as_index=False)["value"].mean()

    # Now pivot safely without duplicates
    wide_df = df.pivot(index="ingredient", columns="nutrient", values="value")
    wide_df.reset_index(inplace=True)

    conn = sqlite3.connect(DB_PATH)
    wide_df.to_sql("ingredients_wide", conn, if_exists="replace", index=False)
    conn.close()

    print("Wide-format table created successfully.")

if __name__ == "__main__":
    convert_long_to_wide()
