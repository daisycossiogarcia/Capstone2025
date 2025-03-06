import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta
import numpy as np

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

# Convert timestamp columns to datetime format
Social['published_at'] = pd.to_datetime(Social['published_at']).dt.tz_localize(None)

# Check dataset structure
print(Social.head())

# Ensure necessary columns exist
required_columns = ["id", "published_at", "description", "likes_count", "shares_count", "comments_count", "views_count", "complete_post_text"]
missing_cols = [col for col in required_columns if col not in Social.columns]
if missing_cols:
    print(f"Warning: Missing columns: {missing_cols}")
else:
    print("All required columns are present.")

print(Social["complete_post_text"].head(10))

# Define key events and their dates
key_events = {
    "Trump_v_United_States": "2024-07-01", 
    "Biden_No_Withdraw": "2024-07-05", 
    "Assassination_Attempt": "2024-07-13", 
    "Biden_Withdraw": "2024-07-21",
}

# Define a time window (e.g., 14 days before & after each event)
time_window = pd.Timedelta(days=14)

# Create filtered DataFrames for each event
event_data = {}
for event, date in key_events.items():
    event_date = pd.to_datetime(date)
    event_data[event] = Social[
        (Social['published_at'] >= (event_date - time_window)) &
        (Social['published_at'] <= (event_date + time_window))
    ]
# Function to plot engagement trends
def plot_engagement_trends(event_name, df):
    if df.empty:
        print(f"No data available for event: {event_name}")
        return
    
    # Ensure engagement columns exist
    engagement_cols = [
        "views_count", 
        "likes_count", 
        "shares_count", 
        "comments_count"
    ]
    for col in engagement_cols:
        if col not in df.columns:
            print(f"Column {col} not found in dataset.")
            return
    # Fill missing values
    df[engagement_cols] = df[engagement_cols].fillna(0)
     # Resample by day and sum engagement counts
    df_grouped = df.set_index("published_at").resample("D")[engagement_cols].sum()
    # Plot trends
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_grouped, x=df_grouped.index, y=df_grouped["views_count"], label="Views", marker="o")
    sns.lineplot(data=df_grouped, x=df_grouped.index, y=df_grouped["likes_count"], label="Likes", marker="o")
    sns.lineplot(data=df_grouped, x=df_grouped.index, y=df_grouped["shares_count"], label="Shares", marker="o")
    sns.lineplot(data=df_grouped, x=df_grouped.index, y=df_grouped["comments_count"], label="Comments", marker="o")
    # Add event date line
    event_date = pd.to_datetime(key_events[event_name])
    plt.axvline(event_date, color='red', linestyle='--', label="Event Date")

    # Formatting
    plt.legend()
    plt.xticks(rotation=45)
    plt.title(f"Engagement Trends Around {event_name}")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.show()

# Plot trends for each event
for event in key_events.keys():
    plot_engagement_trends(event, event_data[event])