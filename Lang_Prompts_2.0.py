#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import os

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

# Function to save prompts into CSV
def save_prompt_to_csv(language, topic, subtopic, prompt):
    # Construct file name for the CSV based on language, topic, and subtopic
    file_path = os.path.join(DATA_DIR, f"{language}_{topic}_{subtopic}.csv")

    # If the CSV file already exists, append the new prompt
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df = df.append({"Prompt": prompt}, ignore_index=True)
    else:
        # If the CSV file doesn't exist, create a new one
        df = pd.DataFrame({"Prompt": [prompt]})

    # Save the DataFrame back to CSV
    df.to_csv(file_path, index=False)

# Streamlit app
st.title('African Languages Prompt Generator App')

# Step 1: Language selection
language = st.selectbox("Select a language", ['Sesotho', 'IsiZulu', 'IsiXhosa'])

# Step 2: Topic selection
selected_topic = st.selectbox("Select a topic", list(topic_subtopic_mapping.keys()))

# Step 3: Subtopic selection (filtered by selected topic)
selected_subtopic = st.selectbox("Select a subtopic", topic_subtopic_mapping[selected_topic])

# Step 4: Create new prompt input field
new_prompt = st.text_input("Enter your new prompt")

# Step 5: Add the new prompt to the CSV file for the selected language, topic, and subtopic
if st.button("Save Prompt"):
    if new_prompt:
        save_prompt_to_csv(language, selected_topic, selected_subtopic, new_prompt)
        st.success(f"Prompt saved for {selected_subtopic} in {language} under {selected_topic}!")
    else:
        st.error("Please enter a prompt before saving.")

# Step 6: Option to view existing prompts
if st.button("View Existing Prompts"):
    # Load and display existing prompts for the selected subtopic
    file_path = os.path.join(DATA_DIR, f"{language}_{selected_topic}_{selected_subtopic}.csv")
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.write(f"Existing prompts for {selected_subtopic} under {selected_topic} in {language}:")
        st.dataframe(df)
    else:
        st.warning("No prompts available yet for this subtopic.")



# In[ ]:




