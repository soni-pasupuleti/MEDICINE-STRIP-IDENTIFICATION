import streamlit as st
import speech_recognition as sr
import pyttsx3
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

def login():
    

    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'password' not in st.session_state:
        st.session_state.password = ""

    speak("Entering your username.")
    username = st.text_input("Username", value=st.session_state.username)
    if not username:
        speak("Please speak your username.")
        username = listen()
        st.write("Username:", username)
        st.session_state.username = username

    speak("Entering your password.")
    password = st.text_input("Password", type="password", value=st.session_state.password)
    if not password:
        speak("Please speak your password.")
        password = listen()
        st.write("Password:", password)
        st.session_state.password = password

    if st.button("Login"):
        
        username = st.session_state.username
        password = st.session_state.password
        
        # Query the user table to check if the entered username and password exist
        query = "SELECT * FROM user WHERE username = %s AND password = %s"
        values = (username, password)
        result = execute_query(query, values, fetchall=False)
        
        if result:
            speak("Login successful.")
            st.success("Login successful.")
        else:
            speak("Invalid username or password. Please try again.")
            st.error("Invalid username or password. Please try again.")
        
        

if __name__ == "__main__":
    login()
