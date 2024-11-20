#!/usr/bin/env python
# coding: utf-8

#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import os
from datetime import datetime
import pytz

# Define the directory to store CSV files
DATA_DIR = "prompts_data"
os.makedirs(DATA_DIR, exist_ok=True)

# Define a mapping of topics to their respective subtopics
topic_subtopic_mapping = {
    'Agriculture': ['Agricultural Products and Sectors', 'Foraging for Edible Plants', 'Role of Agriculture in SA Economy', 'Climate Change and Agriculture'],
    'Health': ['Clinics and Hospitals', 'Medication', 'Family Planning', 'Aged Care', 'Health Conditions', 'Traditional Medicine', 'Emergency Services'],
    'General': ['Education', 'Transport', 'Finance', 'Sports and Hobbies'],
}

# Define scenarios for each subtopic
subtopic_scenario_mapping = {
    'Agricultural Products and Sectors': ['Crop Farming', 'Livestock', 'Aquaculture'],
    'Foraging for Edible Plants': ['Urban Foraging', 'Traditional Practices', 'Foraging Safety'],
    'Role of Agriculture in SA Economy': ['Exports', 'Local Markets', 'Employment'],
    'Climate Change and Agriculture': ['Impact on Crop Yields', 'Water Scarcity', 'Sustainable Practices'],
    'Clinics and Hospitals': ['Patient Care', 'Staffing Issues', 'Infrastructure'],
    'Medication': ['Drug Access', 'Counterfeit Medicines', 'Pharmaceutical Research'],
    'Family Planning': ['Access to Contraceptives', 'Community Education', 'Policy Impacts'],
    'Aged Care': ['Home Care Services', 'Elderly Rights', 'Retirement Planning'],
    'Health Conditions': ['Chronic Diseases', 'Infectious Diseases', 'Mental Health'],
    'Traditional Medicine': ['Herbal Remedies', 'Cultural Practices', 'Integration with Modern Medicine'],
    'Emergency Services': ['Ambulance Availability', 'Disaster Response', 'Public Awareness'],
    'Education': ['E-learning', 'Access to Education', 'Policy Reform'],
    'Transport': ['Public Transport', 'Road Safety', 'Infrastructure Development'],
    'Finance': ['Personal Finance', 'Economic Trends', 'Digital Banking'],
    'Sports and Hobbies': ['Youth Participation', 'Sports Facilities', 'Leisure Activities'],
}

# Define keywords for each scenario
scenario_keyword_mapping = {
    'Crop Farming': ['Pests', 'Fertilizers', 'Irrigation'],
    'Livestock': ['Cattle', 'Poultry', 'Dairy'],
    'Aquaculture': ['Fish Farming', 'Shellfish', 'Algae'],
    'Urban Foraging': ['City Parks', 'Community Gardens', 'Safety Measures'],
    'Traditional Practices': ['Cultural Knowledge', 'Native Plants', 'Harvesting Techniques'],
    'Foraging Safety': ['Toxic Plants', 'Identification', 'Preparation'],
    # Add more mappings as needed for other scenarios...
}

# Function to save prompts into a CSV file
def save_prompt_to_csv(language, topic, subtopic, scenario, keyword, prompt, user_name):
    # Define your timezone (example: 'Africa/Johannesburg' for South Africa)
    local_tz = pytz.timezone('Africa/Johannesburg')

    # Get the current time in UTC and then convert it to the local timezone
    timestamp_utc = datetime.now(pytz.utc)
    timestamp_local = timestamp_utc.astimezone(local_tz)
    timestamp_str = timestamp_local.strftime('%Y-%m-%d %H:%M:%S')

    # Construct file path based on language, topic, subtopic, scenario, and keyword
    file_path = os.path.join(DATA_DIR, f"{language}_{topic}_{subtopic}_{scenario}_{keyword}.csv")

    # Prepare the prompt data
    prompt_data = {
        "Prompt": prompt,
        "User": user_name,
        "Timestamp": timestamp_str,
        "Language": language,
        "Topic": topic,
        "Subtopic": subtopic,
        "Scenario": scenario,
        "Keyword": keyword,
    }

    # Append the prompt data to the CSV or create a new one
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df = pd.concat([df, pd.DataFrame([prompt_data])], ignore_index=True)
    else:
        df = pd.DataFrame([prompt_data])

    # Save the updated DataFrame to the CSV
    df.to_csv(file_path, index=False)

# Streamlit app
st.title('Prompt Generator for ANV Project')

# Use session state to store user name
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# Ask for the user's name
if st.session_state.user_name == "":
    st.session_state.user_name = st.text_input("Enter your name (this will be tracked)", "")
else:
    st.write(f"Welcome, {st.session_state.user_name}!")

# Step 1: Language selection
language = st.selectbox("Select a language", ['Sesotho', 'IsiZulu', 'IsiXhosa'])

# Step 2: Topic selection
selected_topic = st.selectbox("Select a topic", list(topic_subtopic_mapping.keys()))

# Step 3: Subtopic selection
selected_subtopic = st.selectbox("Select a subtopic", topic_subtopic_mapping[selected_topic])

# Step 4: Scenario selection
if selected_subtopic in subtopic_scenario_mapping:
    selected_scenario = st.selectbox("Select a scenario", subtopic_scenario_mapping[selected_subtopic])
else:
    selected_scenario = None
    st.warning("No scenarios available for this subtopic.")

# Step 5: Keyword selection
if selected_scenario in scenario_keyword_mapping:
    selected_keyword = st.selectbox("Select a keyword", scenario_keyword_mapping[selected_scenario])
else:
    selected_keyword = None
    st.warning("No keywords available for this scenario.")

# Step 6: Prompt input
new_prompt = st.text_input("Enter your new prompt")

# Save the prompt
if st.button("Save Prompt"):
    if new_prompt and st.session_state.user_name and selected_keyword:
        save_prompt_to_csv(language, selected_topic, selected_subtopic, selected_scenario, selected_keyword, new_prompt, st.session_state.user_name)
        st.success(f"Prompt saved for {selected_keyword} in {language} under {selected_scenario}, {selected_subtopic}, and {selected_topic} by {st.session_state.user_name}!")
    elif not st.session_state.user_name:
        st.error("Please enter your name before saving the prompt.")
    elif not selected_keyword:
        st.error("Please select a keyword.")
    else:
        st.error("Please enter a prompt before saving.")

# View existing prompts
if st.button("View Existing Prompts"):
    if selected_keyword:
        file_path = os.path.join(DATA_DIR, f"{language}_{selected_topic}_{selected_subtopic}_{selected_scenario}_{selected_keyword}.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            st.write(f"Existing prompts for {selected_keyword} under {selected_scenario}, {selected_subtopic}, and {selected_topic} in {language}:")
            st.dataframe(df)
        else:
            st.warning("No prompts available yet for this keyword.")
    else:
        st.error("Please select a keyword to view prompts.")

# Download existing prompts
if st.button("Download Prompts as CSV"):
    if selected_keyword:
        file_path = os.path.join(DATA_DIR, f"{language}_{selected_topic}_{selected_subtopic}_{selected_scenario}_{selected_keyword}.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{language}_{selected_topic}_{selected_subtopic}_{selected_scenario}_{selected_keyword}_prompts.csv",
                mime="text/csv"
            )
        else:
            st.warning("No prompts available yet for download.")
    else:
        st.error("Please select a keyword to download prompts.")



