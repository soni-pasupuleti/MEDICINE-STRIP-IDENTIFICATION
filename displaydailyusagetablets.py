import streamlit as st
import pandas as pd
from sqlconnection import connect_to_database,execute_query

def fetch_daily_usage_tablets():
    query = "SELECT tablet_name, dosage, frequency FROM daily_usage"
    return execute_query(query, fetchall=True)

def render_frequency_checkboxes(frequency):
    checkboxes = []
    if frequency == "Once a day":
        checkboxes.append("Take once")
    elif frequency == "Twice a day":
        checkboxes.append("Take in morning")
        checkboxes.append("Take in evening")
    elif frequency == "Thrice a day":
        checkboxes.append("Take in morning")
        checkboxes.append("Take in afternoon")
        checkboxes.append("Take in evening")
    
    else:
        checkboxes.append("Unknown frequency")
    return checkboxes



def displaydailyusage():
    st.title("Daily Usage Tablets")
    tablets = fetch_daily_usage_tablets()
    if tablets:
        data = []
        for tablet in tablets:
            frequency_actions = render_frequency_checkboxes(tablet[2])
            data.append(list(tablet[:2]) + [tablet[2], ", ".join(frequency_actions)])

        # Add headers to data
        headers = ["Tablet Name", "Dosage", "Frequency", "Action"]
        # data.insert(0, headers)

        df = pd.DataFrame(data, columns=headers)

        # Display table
        st.dataframe(df.style.set_properties(**{'font-weight': 'bold'}),width = 800)
    else:
        st.write("No daily usage tablets found.")
