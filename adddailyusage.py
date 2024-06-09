import streamlit as st
from sqlconnection import execute_query




def add_daily_usage_tablets():
    
    tablet_name = st.text_input("Tablet Name")
    dosage = st.text_input("Dosage(in mg)")
    frequency = st.selectbox("Frequency", ["Once a day", "Twice a day", "Thrice a day"])
    

    if st.button("Add Tablet"):
        
        if tablet_name and dosage and frequency:
            
            query = "INSERT INTO daily_usage (tablet_name, dosage, frequency) VALUES (%s, %s, %s)"
            values = (tablet_name, dosage, frequency)
            execute_query(query, values)
            
            st.success(f"Tablet '{tablet_name}' added to daily usage.")
        else:
            st.error("Please fill in all required fields.")
