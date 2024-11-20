#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import os
from datetime import datetime
import pytz

def save_prompt_to_csv(language, topic, subtopic, prompt, user_name):
    # Define your timezone (example: 'Africa/Johannesburg' for South Africa)
    local_tz = pytz.timezone('Africa/Johannesburg')  # Change this to your timezone if different

    # Get the current time in UTC and then convert it to the local timezone
    timestamp_utc = datetime.now(pytz.utc)
    timestamp_local = timestamp_utc.astimezone(local_tz)
    timestamp_str = timestamp_local.strftime('%Y-%m-%d %H:%M:%S')

# Sample directory to store CSV files
DATA_DIR = "prompts_data"
os.makedirs(DATA_DIR, exist_ok=True)

# Define a mapping of topics to their respective subtopics
topic_subtopic_mapping = {
    'Technology': ['AI', 'Blockchain', 'Cybersecurity', 'Cloud Computing'],
    'Sports': ['Football', 'Basketball', 'Tennis', 'Cricket'],
    'Health': ['Nutrition', 'Fitness', 'Mental Health', 'Wellness'],
    'Education': ['Online Learning', 'Curriculum Design', 'Educational Psychology'],
}

# Function to save prompts into CSV (including user info and timestamp)
def save_prompt_to_csv(language, topic, subtopic, prompt, user_name):
    # Construct file name for the CSV based on language, topic, and subtopic
    file_path = os.path.join(DATA_DIR, f"{language}_{topic}_{subtopic}.csv")

    # Prepare the prompt data with user info and timestamp
    prompt_data = {
        "Prompt": prompt,
        "User": user_name,
        "Timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    # If the CSV file already exists, append the new prompt data
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df = df.append(prompt_data, ignore_index=True)
    else:
        # If the CSV file doesn't exist, create a new one
        df = pd.DataFrame([prompt_data])

    # Save the DataFrame back to CSV
    df.to_csv(file_path, index=False)

# Streamlit app
st.title('Prompt Generator with Dynamic Topic-Subtopic Correlation')

# Use session state to store user name (so they don't have to enter it each time)
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# If the name is not set, prompt the user to enter their name
if st.session_state.user_name == "":
    st.session_state.user_name = st.text_input("Enter your name (this will be tracked)", "")
else:
    st.write(f"Welcome, {st.session_state.user_name}!")

# Step 1: Language selection
language = st.selectbox("Select a language", ['English', 'Spanish', 'French', 'German', 'Italian', 'Portuguese', 'Dutch'])

# Step 2: Topic selection
selected_topic = st.selectbox("Select a topic", list(topic_subtopic_mapping.keys()))

# Step 3: Subtopic selection (filtered by selected topic)
selected_subtopic = st.selectbox("Select a subtopic", topic_subtopic_mapping[selected_topic])

# Step 5: Create new prompt input field
new_prompt = st.text_input("Enter your new prompt")

# Step 6: Add the new prompt to the CSV file for the selected language, topic, and subtopic
if st.button("Save Prompt"):
    if new_prompt and st.session_state.user_name:
        save_prompt_to_csv(language, selected_topic, selected_subtopic, new_prompt, st.session_state.user_name)
        st.success(f"Prompt saved for {selected_subtopic} in {language} under {selected_topic} by {st.session_state.user_name}!")
    elif not st.session_state.user_name:
        st.error("Please enter your name before saving the prompt.")
    else:
        st.error("Please enter a prompt before saving.")

# Step 7: Separate buttons for viewing and downloading prompts
# View existing prompts
if st.button("View Existing Prompts"):
    # Load and display existing prompts for the selected subtopic
    file_path = os.path.join(DATA_DIR, f"{language}_{selected_topic}_{selected_subtopic}.csv")
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.write(f"Existing prompts for {selected_subtopic} under {selected_topic} in {language}:")
        st.dataframe(df)
    else:
        st.warning("No prompts available yet for this subtopic.")

# Download existing prompts
if st.button("Download Prompts as CSV"):
    file_path = os.path.join(DATA_DIR, f"{language}_{selected_topic}_{selected_subtopic}.csv")
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{language}_{selected_topic}_{selected_subtopic}_prompts.csv",
            mime="text/csv"
        )
    else:
        st.warning("No prompts available yet for download.")

    file_path = os.path.join(DATA_DIR, f"{language}_{topic}_{subtopic}.csv")

    # Prompt data to be saved, including new columns
    prompt_data = {
        "Prompt": prompt,
        "User": user_name,
        "Timestamp": timestamp_str,
        "Language": language,  # Add language as a column
        "Topic": topic,        # Add topic as a column
        "Subtopic": subtopic,  # Add subtopic as a column
        "Topic Description": topic_description,  # New column
        "Subtopic Details": subtopic_details,  # New column
    }

    # Append the prompt data to the CSV file or create a new one
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df = df.append(prompt_data, ignore_index=True)
    else:
        df = pd.DataFrame([prompt_data])

    # Save the updated DataFrame to CSV
    df.to_csv(file_path, index=False)




# In[ ]:




