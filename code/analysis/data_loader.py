# code/analysis/data_loader.py
import pandas as pd

def load_gps_data():
    return pd.read_csv("data/gps_data.csv", parse_dates=["date"])

def load_recovery_data():
    return pd.read_csv("data/recovery_status.csv", parse_dates=["date"])

def load_capability_data():
    return pd.read_csv("data/physical_capability.csv", parse_dates=["date"])

def load_ipa_data():
    return pd.read_csv("data/individual_priority_areas.csv", parse_dates=["target_set_date", "review_date"])

def load_all_data():
    gps_df = load_gps_data()
    recovery_df = load_recovery_data()
    capability_df = load_capability_data()
    ipa_df = load_ipa_data()
    return gps_df, recovery_df, capability_df, ipa_df
