# Imports first:
from pathlib import Path
import streamlit as st
import sys
import os

# Grab the filepath - points to the 'src' parent folder:
filepath = os.path.join(Path(__file__).parents[1])
print("This is the file path, babe: ", filepath)

# Insert the filepath into the system:
sys.path.insert(0, filepath)

# Import the ToMongo Class now:
from to_mongo import ToMongo

# Use absolute path
data_file_relative_path = 'data/netflix_database.csv'
data_file_absolute_path = os.path.abspath(os.path.join(filepath, data_file_relative_path))

# Instantiate the class:
c = ToMongo(filepath=data_file_absolute_path)

# Streamlit UI:
st.header('Query Page')
st.write('This page will search our Netflix database. Spelling currently must be exact.')

# Have the user enter a database attribute to search:
user_query = st.selectbox("Select an attribute to search:", ["subscription_type", "country", "gender", "device"])

if user_query:
    st.write(f"Unique values and counts for {user_query}:")
    results = c.get_unique_values_and_counts(user_query)
    for doc in results:
        st.write(f"{doc['_id']}: {doc['count']}")

