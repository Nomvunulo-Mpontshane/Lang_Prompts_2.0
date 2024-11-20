import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import io

# Define the SQLite database
DB_NAME = 'prompts.db'

# Function to initialize the database and create the prompts table
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS prompts (
                        id INTEGER PRIMARY KEY,
                        language TEXT,
                        topic TEXT,
                        subtopic TEXT,
                        scenario TEXT,
                        keyword TEXT,
                        prompt TEXT,
                        user_name TEXT,
                        timestamp TEXT)''')
    conn.commit()
    conn.close()

# Function to save prompts to the database
def save_prompt_to_db(language, topic, subtopic, scenario, keyword, prompt, user_name):
    # Define your timezone (example: 'Africa/Johannesburg' for South Africa)
    local_tz = pytz.timezone('Africa/Johannesburg')

    # Get the current time in UTC and then convert it to the local timezone
    timestamp_utc = datetime.now(pytz.utc)
    timestamp_local = timestamp_utc.astimezone(local_tz)
    timestamp_str = timestamp_local.strftime('%Y-%m-%d %H:%M:%S')

    # Connect to the SQLite database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Insert the new prompt into the table
    cursor.execute('''INSERT INTO prompts (language, topic, subtopic, scenario, keyword, prompt, user_name, timestamp) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (language, topic, subtopic, scenario, keyword, prompt, user_name, timestamp_str))

    conn.commit()
    conn.close()

# Function to get prompts by subtopic or scenario for CSV download
def get_prompts_by_subtopic_or_scenario(subtopic=None, scenario=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if subtopic:
        cursor.execute('''SELECT * FROM prompts WHERE subtopic = ?''', (subtopic,))
    elif scenario:
        cursor.execute('''SELECT * FROM prompts WHERE scenario = ?''', (scenario,))
    else:
        return []
    
    rows = cursor.fetchall()
    conn.close()
    return rows

# Streamlit app
st.title('Prompt Generator for ANV Project')

# Initialize the database
init_db()

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
        save_prompt_to_db(language, selected_topic, selected_subtopic, selected_scenario, selected_keyword, new_prompt, st.session_state.user_name)
        st.success(f"Prompt saved for {selected_keyword} in {language} under {selected_scenario}, {selected_subtopic}, and {selected_topic} by {st.session_state.user_name}!")
    elif not st.session_state.user_name:
        st.error("Please enter your name before saving the prompt.")
    elif not selected_keyword:
        st.error("Please select a keyword.")
    else:
        st.error("Please enter a prompt before saving.")

# **Download CSV feature:**
# Choose subtopic or scenario for which to download prompts
download_choice = st.selectbox("Download prompts for which subtopic or scenario?", ["Subtopic", "Scenario"])

if download_choice == "Subtopic":
    subtopic = st.selectbox("Select subtopic to download prompts for", topic_subtopic_mapping[selected_topic])
    if subtopic:
        prompts = get_prompts_by_subtopic_or_scenario(subtopic=subtopic)
        if prompts:
            # Convert the prompts to a Pandas DataFrame
            df = pd.DataFrame(prompts, columns=["ID", "Language", "Topic", "Subtopic", "Scenario", "Keyword", "Prompt", "User Name", "Timestamp"])
            # Download the dataframe as a CSV file
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{subtopic}_prompts.csv",
                mime="text/csv"
            )
        else:
            st.warning(f"No prompts available for subtopic: {subtopic}")

elif download_choice == "Scenario":
    scenario = st.selectbox("Select scenario to download prompts for", subtopic_scenario_mapping[selected_subtopic])
    if scenario:
        prompts = get_prompts_by_subtopic_or_scenario(scenario=scenario)
        if prompts:
            # Convert the prompts to a Pandas DataFrame
            df = pd.DataFrame(prompts, columns=["ID", "Language", "Topic", "Subtopic", "Scenario", "Keyword", "Prompt", "User Name", "Timestamp"])
            # Download the dataframe as a CSV file
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{scenario}_prompts.csv",
                mime="text/csv"
            )
        else:
            st.warning(f"No prompts available for scenario: {scenario}")
