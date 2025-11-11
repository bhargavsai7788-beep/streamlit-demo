import streamlit as st
import sqlite3
import pandas as pd

# --- INITIALIZE DATABASE (one-time setup) ---
# This part creates a simple SQLite database and adds some sample data.
def setup_database():
    # Connect to (or create) a database file
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    
    # Create a table (if it doesn't exist)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER
    )
    """)
    
    # Clear old data and insert new sample data
    cursor.execute("DELETE FROM users") # Clear table for a clean demo
    sample_data = [
        (1, 'Alice', 30),
        (2, 'Bob', 25),
        (3, 'Charlie', 42),
        (4, 'David', 19),
        (5, 'Eve', 22),
        (6, 'Frank', 18),
        (7, 'Grace', 27)
    ]
    cursor.executemany("INSERT INTO users (id, name, age) VALUES (?, ?, ?)", sample_data)
    
    conn.commit()
    conn.close()

# --- CACHED FUNCTION TO LOAD DATA ---
# We use st.cache_data to avoid re-running the query on every interaction
@st.cache_data
def load_data():
    conn = sqlite3.connect("test.db")
    # Execute a query and fetch all results into a pandas DataFrame
    query = "SELECT name, age FROM users WHERE age > 20"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# --- STREAMLIT APP ---
st.set_page_config(layout="wide")
st.title("Load Data from a SQLite Database")

# Run the setup function to create the database and table
setup_database()

st.subheader("User Data")
st.write("This data is loaded from a `test.db` file.")

# Load and display the data
try:
    df = load_data()
    st.dataframe(df, use_container_width=True)
    
    st.write(f"Showing {len(df)} users over 20 years old.")

except Exception as e:
    st.error(f"Error loading data: {e}")

# A button to show how caching works
if st.button("Reload data"):
    # Clear the cache and re-run the function
    st.cache_data.clear()
    df = load_data()
    st.success("Data reloaded!")