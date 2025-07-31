import pandas as pd

# Path to your Excel file
excel_path = "Template-1.xlsx"

# List of sheets to process
sheet_names = ['Meat', 'Grains', 'Vegetables', 'oils', 'Fruits', 'Mixed']

all_data = []

for sheet in sheet_names:
    # Read the current sheet
    df = pd.read_excel(excel_path, sheet_name=sheet)

    # Transpose the data: columns become rows and vice versa
    df = df.set_index(df.columns[0]).T.reset_index()

    # Rename the first column to 'ingredient'
    df.rename(columns={'index': 'ingredient'}, inplace=True)

    # Add a column for the group (the sheet name)
    df['group'] = sheet

    # Add this data to the list
    all_data.append(df)

# Combine data from all sheets into one big DataFrame
combined_df = pd.concat(all_data, ignore_index=True)

# Save to CSV file for easier viewing or later use
combined_df.to_csv("combined_ingredients.csv", index=False)

print("Combined data saved to combined_ingredients.csv")
