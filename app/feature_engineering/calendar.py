# app/feature_engineering/calendar.py

import streamlit as st
import pandas as pd
from streamlit_calendar import calendar as st_calendar # The FullCalendar-based Streamlit component



def load_calendar_data():
    """
    Loads 'chelsea_fc_calendar.csv' with columns:
      - event_date (YYYY-MM-DD HH:MM:SS or just YYYY-MM-DD)
      - event_type (e.g. 'Match', 'Training', 'Media', etc.)
      - event_name (optional string describing the event)
    """
    df = pd.read_csv("data/csv/chelsea_fc_calendar.csv", parse_dates=["event_date"])
    return df

def show_calendar_ui():
    """
    Renders a calendar in the Streamlit UI using 'streamlit-calendar' library.
    - If 'event_date' is at midnight, we treat it as all-day to avoid '12a' entries.
    - We color events based on 'event_type': matches = red, training = green, else default.
    """
    st.subheader("Chelsea FC Calendar (using streamlit-calendar)")

    # 1) Load event data
    df = load_calendar_data()
    if df.empty:
        st.warning("No events found in 'chelsea_fc_calendar.csv'.")
        return

    # 2) Convert each row in df to a 'streamlit-calendar' event dictionary
    calendar_events = []
    for _, row in df.iterrows():
        event_dt = row["event_date"]
        # If time is exactly midnight => treat as allDay event
        all_day = (event_dt.hour == 0 and event_dt.minute == 0 and event_dt.second == 0)

        # Basic event details
        event_type = row.get("event_type", "Event")
        event_name = row.get("event_name", "")
        start_str = event_dt.isoformat()  # e.g. '2024-08-01T00:00:00'

        # Choose color if desired
        # For a match -> red, training -> green
        color = None
        if event_type.lower() == "match":
            color = "#FF8888"
        elif event_type.lower() == "training":
            color = "#88FF88"

        # Build event dictionary
        event_dict = {
            "title": f"{event_type}: {event_name}" if event_name else event_type,
            "start": start_str,
            "allDay": all_day
        }
        if color:
            event_dict["backgroundColor"] = color
            event_dict["borderColor"] = color

        calendar_events.append(event_dict)

    # 3) Configure FullCalendar options
    #    Docs: https://fullcalendar.io/docs
    #    streamlit-calendar 'options' pass through to FullCalendar.
    calendar_options = {
        "initialView": "dayGridMonth",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek",
        },
        # This changes how times (like 12:00) display: e.g. 24-hr format "HH:mm"
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

    # 4) Render the calendar in the Streamlit UI
    #    'key' ensures stable state if the user interacts with it
    cal_response = st_calendar(
        events=calendar_events,
        options=calendar_options,
        custom_css=custom_css,
        key="chelsea_calendar"
    )

    # 5) Optionally, see if the user clicked or edited an event
    #    cal_response is a dict with details about callbacks from user interactions
    st.write("Calendar response:", cal_response)

    # 6) Display raw data for reference
    with st.expander("Raw Calendar CSV Data"):
        st.dataframe(df)

    st.caption("Events at midnight are treated as all-day. Matches are red, training sessions green.")

