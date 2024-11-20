import streamlit as st
import pandas as pd
import os
import sqlite3
from datetime import datetime
import pytz

# Define the directory to store CSV files
DATA_DIR = "prompts_data"
os.makedirs(DATA_DIR, exist_ok=True)

# Database setup
DB_FILE = "prompts.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt TEXT,
    user TEXT,
    timestamp TEXT,
    language TEXT,
    topic TEXT,
    subtopic TEXT,
    scenario TEXT,
    keyword TEXT
)
""")
conn.commit()

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
}

# Function to save prompts into the database
def save_prompt_to_db(language, topic, subtopic, scenario, keyword, prompt, user_name):
    # Define your timezone (example: 'Africa/Johannesburg' for South Africa)
    local_tz = pytz.timezone('Africa/Johannesburg')
    timestamp = datetime.now(pytz.utc).astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute("""
    INSERT INTO prompts (prompt, user, timestamp, language, topic, subtopic, scenario, keyword)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (prompt, user_name, timestamp, language, topic, subtopic, scenario, keyword))
    conn.commit()

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
        save_prompt_to_db(language, selected_topic, selected_subtopic, selected_scenario, selected_keyword, new_prompt, st.session_state.user_name)
        st.success(f"Prompt saved!")
    else:
        st.error("Please fill in all fields before saving the prompt.")

# Search prompts
st.subheader("Search Prompts")
search_query = st.text_input("Search by keyword, topic, or prompt content")
if st.button("Search"):
    cursor.execute("""
    SELECT * FROM prompts
    WHERE prompt LIKE ? OR keyword LIKE ? OR topic LIKE ?
    """, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
    search_results = cursor.fetchall()
    if search_results:
        df = pd.DataFrame(search_results, columns=['ID', 'Prompt', 'User', 'Timestamp', 'Language', 'Topic', 'Subtopic', 'Scenario', 'Keyword'])
        st.dataframe(df)
    else:
        st.warning("No results found.")

# Download prompts as CSV
if st.button("Download All Prompts as CSV"):
    cursor.execute("SELECT * FROM prompts")
    all_prompts = cursor.fetchall()
    df = pd.DataFrame(all_prompts, columns=['ID', 'Prompt', 'User', 'Timestamp', 'Language', 'Topic', 'Subtopic', 'Scenario', 'Keyword'])
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="all_prompts.csv",
        mime="text/csv"
    )
