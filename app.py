import streamlit as st
import cv2 
import os
import numpy as np
from gtts import gTTS
import tempfile
import pyttsx3
import uuid
import base64
from io import BytesIO
from sqlconnection import execute_query, connect_to_database

current_directory = os.path.dirname(os.path.abspath(__file__))

image_directory = os.path.join(current_directory, "finaldata1")
uploaded_image_directory =os.path.join(current_directory,"uploaded_images")

def insert_into_tablet_history(image_path, identified, identified_tablet_name, similarity_score):
    query = "INSERT INTO tablet_history (image_path, identified, identified_tablet_name, similarity_score) VALUES (%s, %s, %s, %s)"
    values = (image_path, identified, identified_tablet_name, similarity_score)
    execute_query(query, values)

def save_image_file(file_bytes, filename):
    image_path = os.path.join(uploaded_image_directory, filename)
    with open(image_path, "wb") as f:
        f.write(file_bytes)
    return image_path
# Function to compute SIFT keypoints and descriptors for an image
def compute_sift(image):
    if image is None:
        return None, None
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(gray_image, None)
    return keypoints, descriptors

# Function to match images using SIFT
def match_images(new_image, image_directory):
    keypoints1, descriptors1 = compute_sift(new_image)
    bf = cv2.BFMatcher()
    similarity_scores = []
    for filename in os.listdir(image_directory):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(image_directory, filename)
            image = cv2.imread(image_path)
            if image is None:
                continue
            keypoints2, descriptors2 = compute_sift(image)
            matches = bf.knnMatch(descriptors1, descriptors2, k=2)
            good_matches = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)

            similarity_score = len(good_matches)
            similarity_scores.append((filename, similarity_score))

    sorted_images = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    
    return sorted_images

# Function to convert text to speech
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop() # Ensure the engine is stopped after usage

# Initial voice message flag
initial_voice_message_spoken =  False

# Streamlit app
def identify_tablets():
    st.title("Audio-Based Image Matching Web App for Visually Impaired Users")

    global initial_voice_message_spoken

    if not initial_voice_message_spoken:
        text_to_speech("Welcome to the Audio-Based Image Matching Web App for Visually Impaired Users. Please follow the instructions to use the app effectively. To start, you can either upload an image or take a picture using your camera.")
        initial_voice_message_spoken = True
    image_directory = os.path.join(current_directory, "finaldata1")
   

    option = st.radio("Choose an option:", ("Upload an image", "Take a picture with your camera"))

    if option == "Upload an image":
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            image_filename= uploaded_file.name
            # Display processing message
            st.write("Image is under processing...")

            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            new_image = cv2.imdecode(file_bytes, 1)
            st.image(new_image, caption='Uploaded Image', use_column_width=True, output_format='JPEG')
            sorted_images = match_images(new_image, image_directory)

            if sorted_images:
                best_matched_image_path = os.path.join(image_directory, sorted_images[0][0])
                best_matched_image = cv2.imread(best_matched_image_path)
                
                accuracy_threshold = 1000
                  
        
                if sorted_images[0][1] >= accuracy_threshold:
                        #display in this page
                        st.image(best_matched_image, caption='Best Matched Image', use_column_width=True, output_format='JPEG')
                        st.write(f"\nBest Matched Image: {sorted_images[0][0]}")
                        st.write(f"Similarity Score: {sorted_images[0][1]}")
                        text_result = f"The best matched image is {sorted_images[0][0]} with a similarity score of {sorted_images[0][1]}"
                        text_to_speech(text_result)
                        st.success("Voice-based result generated. Check your speakers for the output.")

                        #for saving in database
                        similarity_score = sorted_images[0][1]
                        identified = "Yes"  
                        identified_tablet_name = sorted_images[0][0] 
                        image_path = save_image_file(file_bytes, image_filename)
                        insert_into_tablet_history(image_path, identified, identified_tablet_name, similarity_score)
                
                else:
                    similarity_score = sorted_images[0][1]
                    identified = "No"  # Assuming if similarity score exceeds the threshold, it's identified
                    identified_tablet_name = "unidentified"  # Assuming tablet name is the image filename
                    image_path = save_image_file(file_bytes, image_filename)
                    insert_into_tablet_history(image_path, identified, identified_tablet_name, similarity_score)

                    st.warning("No images found for matching.")

    elif option == "Take a picture with your camera":
        st.warning("Please allow access to your camera.")
        st.warning("Click the 'Take Picture' button to capture an image.")
        if st.button("Take Picture"):
            st.warning("Processing...")

            video_capture = cv2.VideoCapture(0)
            ret, frame = video_capture.read()
            video_capture.release()

            if ret:
                
                # Convert frame to JPEG format
                is_success, buffer = cv2.imencode(".jpg", frame)
                if is_success:
                    image_filename = f"captured_image_{uuid.uuid4().hex}.jpg"
                    frame_bytes = BytesIO(buffer)
                    st.image(frame_bytes, caption='Captured Image', use_column_width=True, output_format='JPEG')
                    sorted_images = match_images(frame, image_directory)
                    if sorted_images:
                        best_matched_image_path = os.path.join(image_directory, sorted_images[0][0])
                        best_matched_image = cv2.imread(best_matched_image_path)
                        accuracy_threshold = 1000
        
                        if sorted_images[0][1] >= accuracy_threshold:
                            st.image(best_matched_image, caption='Best Matched Image', use_column_width=True, output_format='JPEG')
                            st.write(f"\nBest Matched Image: {sorted_images[0][0]}")
                            st.write(f"Similarity Score: {sorted_images[0][1]}")
                            similarity_score = sorted_images[0][1]
                            text_result = f"The best matched image is {sorted_images[0][0]} with a similarity score of {sorted_images[0][1]}"
                            text_to_speech(text_result)
                            st.success("Voice-based result generated. Check your speakers for the output.")

                            similarity_score = sorted_images[0][1]
                            identified = "Yes"  # Assuming if similarity score exceeds the threshold, it's identified
                            identified_tablet_name = sorted_images[0][0]  # Assuming tablet name is the image filename
                            image_path = save_image_file(buffer, image_filename)
                            insert_into_tablet_history(image_path, identified, identified_tablet_name, similarity_score)
                
                        else:
                            st.warning("No images found for matching.")

                            similarity_score = sorted_images[0][1]
                            identified = "No"  # Assuming if similarity score exceeds the threshold, it's identified
                            identified_tablet_name = "unidentified"  # Assuming tablet name is the image filename
                            image_path = save_image_file(buffer, image_filename)
                            insert_into_tablet_history(image_path, identified, identified_tablet_name, similarity_score)            
                else:
                    st.warning("Failed to encode captured image.")
            else:
                st.warning("Failed to capture image from the webcam.")

