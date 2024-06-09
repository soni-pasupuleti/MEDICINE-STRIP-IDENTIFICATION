import streamlit as st
import speech_recognition as sr
import pyttsx3
import time
from sqlconnection import execute_query

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    if 'r' not in st.session_state:
        st.session_state.r = sr.Recognizer()
    r = st.session_state.r
    
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        user_input = r.recognize_google(audio)
        return user_input
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

def signup():
     
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'phone_number' not in st.session_state:
        st.session_state.phone_number = ""
    if 'password' not in st.session_state:
        st.session_state.password = ""
    if 'confirm_password' not in st.session_state:
        st.session_state.confirm_password = ""

    

    speak("Entering your username.")
    username = st.text_input("Username", value=st.session_state.username)
    if not username:
        speak("Please speak your username.")
        username = listen()
        st.write("Username:", username)
        st.session_state.username = username

    speak("Entering your phone number.")
    phone_number = st.text_input("Phone Number", value=st.session_state.phone_number)
    if not phone_number:
        speak("Please speak your phone number.")
        phone_number = listen()
        st.write("Phone Number:", phone_number)
        st.session_state.phone_number = phone_number

    speak("Entering your password.")
    
    password = st.text_input("Password", type="password", value=st.session_state.password)
    if not password:
        speak("Please speak your password.")
        password = listen()
        st.write("Password:", password)
        st.session_state.password = password

    speak("Confirming your password.")
    
    confirm_password = st.text_input("Confirm Password", type="password", value=st.session_state.confirm_password)
    if not confirm_password:
        speak("Please speak your password again.")
        confirm_password = listen()
        st.write("Confirm Password:", confirm_password)
        st.session_state.confirm_password = confirm_password

    if st.button("Sign Up"):
        if username and phone_number and password and confirm_password:
            # Check if password matches confirm password
            if password == confirm_password:
                # Insert user data into the user table
                query = "INSERT INTO user (username, phone_number, password) VALUES (%s, %s, %s)"
                values = (username, phone_number, password)
                execute_query(query, values)
                
                speak("All fields have been filled and submitted.")
                st.success("Account created for {}".format(username))
                speak("Account created for {}".format(username))
                st.write("Phone Number:", phone_number)
                exit()
            else:
                st.warning("Passwords do not match. Please re-enter.")
        else:
            st.warning("Please fill all fields.")
            
        
    
    
        

if __name__ == "__main__":
    signup()
