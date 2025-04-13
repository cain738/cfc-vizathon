# app/feature_engineering/data_wrangler.py

import os
import pandas as pd
import streamlit as st
from analysis.data_loader import load_capability_data, load_recovery_data, load_calendar_data

def load_capability_recovery_merged_data():
    """
    Load capability and recovery datasets,
    merge them on common keys ('player' and 'date'),
    and export the merged file to output/csv/capability_recovery_merged.csv.
    """
    capability_df = load_capability_data()
    recovery_df = load_recovery_data()
    
    # Merge the datasets on 'player' and 'date'
    merged_df = pd.merge(capability_df, recovery_df, on=["player", "date"], how="inner")
    
    # Ensure the output directory exists.
    output_dir = os.path.join("output", "csv")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, "capability_recovery_merged.csv")
    merged_df.to_csv(output_path, index=False)
    
    return merged_df, output_path

def load_advanced_capability_recovery_data():
    """
    Loads the capability and recovery datasets, merges them on 'player' and 'date',
    and then enhances the dataset using calendar data to compute advanced features.
    
    Advanced Features:
      - md_minus_1: Flag indicating if the record's date is exactly one day before a match day,
        derived from the calendar data.
    
    The function also exports the advanced merged dataset to 
    data/csv/advanced_capability_recovery_merged.csv.
    
    Returns:
        merged_df: The advanced merged DataFrame.
        output_path: The file path where the merged data is saved.
    """
    # Load capability and recovery data
    capability_df = load_capability_data()
    recovery_df = load_recovery_data()
    merged_df = pd.merge(capability_df, recovery_df, on=["player", "date"], how="inner")
    
    # Load calendar data
    calendar_df = load_calendar_data()
    # Filter for match events (assuming event_type "Match", case-insensitive)
    match_df = calendar_df[calendar_df["event_type"].str.lower() == "match"]
    
    # Compute MD–1 dates: subtract one day from each match date
    md_minus_1_dates = pd.to_datetime(match_df["event_date"]) - pd.Timedelta(days=1)
    
    # Add a new column 'md_minus_1': 1 if the record's date is one day before a match, else 0
    merged_df["md_minus_1"] = merged_df["date"].isin(md_minus_1_dates).astype(int)
    
    # (Optional) Further advanced features could be computed here, such as MD+1, days_from_match, etc.
    
    # Export the advanced merged dataset
    output_dir = os.path.join("data", "csv")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, "advanced_capability_recovery_merged.csv")
    merged_df.to_csv(output_path, index=False)
    
    return merged_df, output_path