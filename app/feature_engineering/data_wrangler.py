# app/feature_engineering/data_wrangler.py

import pandas as pd

def merge_gps_with_calendar(gps_df: pd.DataFrame, cal_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges GPS data with calendar to enrich it with training context (e.g., training_load).
    Args:
        gps_df: DataFrame from gps_data.csv
        cal_df: DataFrame from chelsea_fc_calendar.csv
    Returns:
        Merged DataFrame with 'training_load' and all GPS metrics.
    """
    gps_df["date"] = pd.to_datetime(gps_df["date"])
    cal_df["event_date"] = pd.to_datetime(cal_df["event_date"])
    
    # Rename to align keys
    cal_df = cal_df.rename(columns={"event_date": "date"})
    
    merged = pd.merge(gps_df, cal_df[["player", "date", "training_load"]], on=["player", "date"], how="left")
    merged = merged.dropna(subset=["training_load"])
    return merged

# app/feature_engineering/data_wrangler.py

def merge_recovery_with_calendar(recovery_df: pd.DataFrame, cal_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges recovery data with calendar and marks MD-1 days.
    """
    recovery_df["date"] = pd.to_datetime(recovery_df["date"])
    cal_df["event_date"] = pd.to_datetime(cal_df["event_date"])

    # Extract MD-1 days per player
    md1_dates = cal_df[cal_df["event_type"].str.lower() == "match"]
    md1_dates["md_minus_1_date"] = md1_dates["event_date"] - pd.Timedelta(days=1)

    # Join on date
    merged = pd.merge(recovery_df, md1_dates[["player", "md_minus_1_date"]], 
                      left_on=["player", "date"], right_on=["player", "md_minus_1_date"], how="left")

    merged["is_md_minus_1"] = merged["md_minus_1_date"].notnull().astype(int)
    merged.drop(columns=["md_minus_1_date"], inplace=True)

    return merged

def merge_capability_with_calendar(cap_df: pd.DataFrame, cal_df: pd.DataFrame) -> pd.DataFrame:
    cap_df["date"] = pd.to_datetime(cap_df["date"])
    cal_df["event_date"] = pd.to_datetime(cal_df["event_date"])

    md_df = cal_df[cal_df["event_type"].str.lower() == "match"].copy()
    md_df["md_minus_1"] = md_df["event_date"] - pd.Timedelta(days=1)

    # Merge for MD-1 flag
    cap_df = pd.merge(
        cap_df,
        md_df[["player", "md_minus_1"]],
        left_on=["player", "date"],
        right_on=["player", "md_minus_1"],
        how="left"
    )
    cap_df["is_md_minus_1"] = cap_df["md_minus_1"].notnull().astype(int)
    cap_df.drop(columns=["md_minus_1"], inplace=True)

    # ✅ Merge with calendar to fetch position info
    cal_df = cal_df.rename(columns={"event_date": "date"})
    cap_df = pd.merge(
        cap_df,
        cal_df[["player", "date", "position"]],
        on=["player", "date"],
        how="left"
    )

    return cap_df

def merge_capability_with_recovery(cap_df: pd.DataFrame, recovery_df: pd.DataFrame) -> pd.DataFrame:
    cap_df["date"] = pd.to_datetime(cap_df["date"])
    recovery_df["date"] = pd.to_datetime(recovery_df["date"])
    return pd.merge(cap_df, recovery_df, on=["player", "date"], how="left")
