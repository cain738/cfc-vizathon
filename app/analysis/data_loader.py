# file: app/analysis/data_loader.py

import os
import pandas as pd


def load_gps_data() -> pd.DataFrame:
    """
    Loads GPS data from /data/gps_data.csv.
    """
    script_dir = os.path.dirname(__file__)  # e.g. .../app/analysis
    gps_path = os.path.join(script_dir, "..", "..", "data", "csv", "gps_data.csv")
    return pd.read_csv(gps_path, parse_dates=["date"])


def load_recovery_data() -> pd.DataFrame:
    """
    Loads Recovery Status data from /data/recovery_status.csv.
    """
    script_dir = os.path.dirname(__file__)
    recovery_path = os.path.join(
        script_dir, "..", "..", "data", "csv", "recovery_status.csv"
    )
    return pd.read_csv(recovery_path, parse_dates=["date"])


def load_capability_data() -> pd.DataFrame:
    """
    Loads Physical Capability data from /data/physical_capability.csv.
    """
    script_dir = os.path.dirname(__file__)
    capability_path = os.path.join(
        script_dir, "..", "..", "data", "csv", "physical_capability.csv"
    )
    return pd.read_csv(capability_path, parse_dates=["date"])


def load_ipa_data() -> pd.DataFrame:
    """
    Loads Individual Priority Areas data from /data/individual_priority_areas.csv.
    """
    script_dir = os.path.dirname(__file__)
    ipa_path = os.path.join(
        script_dir, "..", "..", "data", "csv", "individual_priority_areas.csv"
    )
    return pd.read_csv(ipa_path, parse_dates=["target_set_date", "review_date"])

def load_calendar_data() -> pd.DataFrame:
    # Newly added function for Chelsea FC calendar
    script_dir = os.path.dirname(__file__)
    ipa_path = os.path.join(
        script_dir, "..", "..", "data", "csv", "chelsea_fc_calendar.csv"
    )
    return pd.read_csv(ipa_path, parse_dates=["event_date"])


def load_all_data():
    """
    Convenience function that loads all four datasets and returns them
    as a tuple: (gps_df, recovery_df, capability_df, ipa_df).
    """
    gps_df = load_gps_data()
    recovery_df = load_recovery_data()
    capability_df = load_capability_data()
    ipa_df = load_ipa_data()
    calendar_data = load_calendar_data()

    return gps_df, recovery_df, capability_df, ipa_df, calendar_data
