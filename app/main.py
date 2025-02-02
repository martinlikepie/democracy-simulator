import streamlit as st
import json
import os

# Define the file path
GAME_STATE_FILE = "data/game_state.json"

# Function to load game state
def load_game_state():
    if not os.path.exists(GAME_STATE_FILE):
        # Initialize with default values if file doesn't exist
        game_state = {"budget": 1000, "public_approval": 50, "economic_growth": 1.0, "turns": 1}
        save_game_state(game_state)
    else:
        with open(GAME_STATE_FILE, "r") as file:
            game_state = json.load(file)
        
        # Ensure "turns" key exists
        if "turns" not in game_state:
            game_state["turns"] = 1
            save_game_state(game_state)
    
    return game_state

# Function to save game state
def save_game_state(state):
    with open(GAME_STATE_FILE, "w") as file:
        json.dump(state, file)

# Load game state
game_state = load_game_state()

# Streamlit UI
st.title("Democracy Simulator")
st.write("Welcome to the interactive democracy simulation.")

# Display current turn
st.subheader(f"Turn: {game_state['turns']}")

# Button to advance turn
if st.button("Next Turn"):
    game_state["turns"] += 1
    save_game_state(game_state)
    st.experimental_rerun()
