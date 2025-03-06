import pandas as pd
import os

# Set the file path
file_path = "/Users/DaisyCossio/Desktop/merged_df.csv"

# Load dataset
try:
    Social = pd.read_csv(file_path)
    print("Data loaded successfully!")
except FileNotFoundError:
    print("File not found. Check the path.")

# Show first 5 rows
print(Social.head())
