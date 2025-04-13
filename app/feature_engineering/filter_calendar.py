# app/feature_engineering/filter_calendar.py

import streamlit as st
import pandas as pd
from streamlit_calendar import calendar

def load_calendar_data():
    """
    Load the CSV containing Chelsea FC’s important events (matches, training, etc.).
    Expects columns like:
      - start_date: date/datetime (YYYY-MM-DD or ISO string)
      - end_date: (optional) if multi-day or timed events
      - title: e.g., 'Chelsea vs Arsenal'
      - event_type: 'Match' or 'Training' etc.
    """
    df = pd.read_csv("data/csv/chelsea_fc_calendar.csv", parse_dates=["event_date"])
    # Drop all duplicate event_dates to keep only the first occurrence
    return df

def show_calendar_in_filter():
    """
    Renders the 'streamlit-calendar' calendar in the sidebar or main area as part of your filter UI.
    """
    st.subheader("Chelsea FC Events Calendar")

    df = load_calendar_data()
    if df.empty:
        st.warning("No calendar events found!")
        return
    
    # Convert rows to a list of dicts recognized by streamlit-calendar
    # Each event must have 'title', 'start', 'end' (optionally).
    # https://fullcalendar.io/docs/event-parsing
    # If 'end_date' is not in your CSV, you can omit it or set it the same as start_date.
    calendar_events = []
    for _, row in df.iterrows():
        event = {
            "title": row["event_type"],
            "start": row["event_date"].isoformat(),
            "allDay": True
        }
        # If you have an end_date
        if "end_date" in row and pd.notnull(row["end_date"]):
            event["end"] = row["end_date"].isoformat()

        # Optionally color-code by event_type (match / training)
        # e.g. event["backgroundColor"] = "#FFD1D1" if row["event_type"]=="Match" else "#C1FFC1"
        if "event_type" in row:
            if row["event_type"].lower() == "match":
                event["backgroundColor"] = "#FFD1D1"   # light red
                event["borderColor"] = "#FF6C6C"       # darker red
            elif row["event_type"].lower() == "training":
                event["backgroundColor"] = "#C1FFC1"   # light green
                event["borderColor"] = "#81FF81"       # bright green

        calendar_events.append(event)

    # Optional customization for the calendar UI
    calendar_options = {
        "initialView": "dayGridMonth",  # or 'timeGridWeek', 'listWeek', ...
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,listWeek"
        },
        "weekends": True,
        "editable": False,
        "selectable": False,
        # more FullCalendar options: https://fullcalendar.io/docs
        "eventTimeFormat": {
            "hour": "2-digit",
            "minute": "2-digit",
            "hour12": False
        },
    }

    # If you want to apply custom CSS
    custom_css = """
    .fc-event-title {
      font-weight: bold;
    }
    .fc-daygrid-event {
      border-radius: 5px;
      padding: 2px;
    }
    """

    # Render the calendar
    st.info("Below is the interactive FullCalendar for matchdays & trainings:")
    cal_value = calendar(
        events=calendar_events,
        options=calendar_options,
        custom_css=custom_css,
        key="chelsea_calendar",
    )

    st.write("Calendar return value:", cal_value)
    st.caption("Use the dictionary above to respond to event clicks or date selects if needed.")
