import streamlit as st
import base64
import speech_recognition as sr
import pyttsx3
import os 
import time
from PIL import Image
import io
from adddailyusage import add_daily_usage_tablets
from displaydailyusagetablets import displaydailyusage
from signup import signup, speak, listen
from login import login
from app import identify_tablets

from sqlconnection import execute_query, connect_to_database
current_directory = os.path.dirname(os.path.abspath(__file__))

image_directory = os.path.join(current_directory, "finaldata1")

bg_image =os.path.join(current_directory, "bgimage.png")
    


    
# Function to display recently identified tablet strips
def display_recent_identified_strips():
    
    
    # Retrieve data from the database
    query = "SELECT * FROM tablet_history"
    results = execute_query(query, fetchall=True)
    if results:
        
        for result in results:
            # Convert raw image data to base64-encoded string
            image_path= result[1]  # Assuming the image data is in the first column
            col1, col2 = st.columns([1, 3])  # Adjust column width ratio as needed
            with col1:
                
                with open(image_path, "rb") as f:
                    st.image(f.read(), caption="Identified Tablet Strip", use_column_width=True)
           
            with col2:
                st.write("Identified / Not: ", result[2])
                st.write("Identified Tablet Name: ", result[3])
                st.write("Similarity Score: ", result[4])
        
    else:
        st.write("No tablet strips identified yet.")
    
def identify_tablet_strip():
    identify_tablets()

def main():
    
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Select a page", ["Home" ,"signup","login", "Identify Tablet Strip", "Recently Identified Strips","Add Daily Usage Tablets","View daily usage tablets"])
    if page == "Recently Identified Strips":
        st.title("Recently Identified Strips")
        display_recent_identified_strips()
    elif page == "Identify Tablet Strip":
        st.title("Identify Tablet Strip")
        identify_tablet_strip()
    elif page == "Add Daily Usage Tablets":
        st.title("Add Daily Usage Tablets")
        add_daily_usage_tablets()
    elif page=="signup":
        st.title("Signup if you are a new user!")
        signup()
    elif page=="login":
        st.title("Welcome back, login to medovision.")
        login()
    elif page=="Home":
        st.title("MedoVision - Know Your medicine")
        col1, col2 = st.columns([1, 1]) 
        with col1:
            with open(bg_image, "rb") as f:
                st.image(f.read(), use_column_width=True)    
        with col2:
            st.write("MedoVision is a platform for medication management , speacially designed as a goal to be assistive technology for the visually impaired . With features like tablet strip identification, daily usage tracking, it ensures users maintain their medication schedule effortlessly. The application offers to identify tablet strips of all sizes and conditions, making it reliable and at hand. Leveraging cutting-edge assistive technology, MedoVision offers a seamless experience for all, including the visually impaired. Its commitment to accessibility and usability makes it inclusive for everyone, eliminating missed doses and confusion. MedoVision promises a healthier, happier life for all.")
            
    elif page == "View daily usage tablets":
        displaydailyusage()
        
        

if __name__ == "__main__":
    main()
