import streamlit as st
import json
import os
import sys

# Ensure Python can find the `utils` module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.utils import trigger_random_event  # Import after fixing path

game_state_file = "data/game_state.json"

def load_game_state():
    if os.path.exists(game_state_file):
        with open(game_state_file, "r") as file:
            game_state = json.load(file)
    else:
        game_state = {}

    # Ensure all required keys exist
    defaults = {
        "budget": 1000, "public_approval": 50, "turns": 1, "policy_history": [],
        "gdp": 100, "unemployment": 5, "crime_rate": 10,
        "citizen_groups": {"Business Owners": 50, "Workers": 50, "Environmentalists": 50},
        "event_history": []  # ✅ Ensure event history exists
    }

    for key, value in defaults.items():
        if key not in game_state:
            game_state[key] = value

    return game_state

def save_game_state(state):
    with open(game_state_file, "w") as file:
        json.dump(state, file)

def apply_policy(game_state, policy, intensity):
    effects = {
        "Income Tax": {"budget": intensity * 10, "public_approval": -intensity, "gdp": -intensity * 2},
        "Healthcare Funding": {"budget": -intensity * 15, "public_approval": intensity, "unemployment": -intensity},
        "Police Funding": {"budget": -intensity * 10, "public_approval": intensity - 5, "crime_rate": -intensity},
        "Welfare Spending": {"budget": -intensity * 20, "public_approval": intensity + 5, "unemployment": intensity}
    }
    
    for key, value in effects[policy].items():
        game_state[key] += value
    game_state["policy_history"].append({"policy": policy, "intensity": intensity})
    save_game_state(game_state)

def check_game_status(game_state):
    if game_state["public_approval"] <= 0:
        st.error("Game Over! Public approval dropped to 0.")
        st.stop()
    elif game_state["turns"] >= 20:
        st.success("Congratulations! You have successfully completed 20 turns.")
        st.stop()

st.title("Democracy Simulator")
st.write("Welcome to the interactive democracy simulation.")

game_state = load_game_state()

st.subheader(f"Turn: {game_state['turns']}")

# Load effects from game_state.json
if os.path.exists(game_state_file):
    with open(game_state_file, "r") as file:
        game_data = json.load(file)
        effects = game_data.get("effects", {})  # Ensure effects is always a dictionary
else:
    effects = {}  # Default to empty dictionary if file doesn't exist

# ✅ **Fixed issue: Only one selectbox for policy selection**
policy = st.selectbox("Choose a policy to adjust:", list(effects.keys()) if effects else ["No Policies Available"], key="policy_selector")

# Select intensity
intensity = st.slider("Select policy intensity", 0, 10, 5)

if st.button("Apply Policy"):
    apply_policy(game_state, policy, intensity)
    st.write(f"You selected **{policy}** with intensity level **{intensity}**.")

st.subheader("Policy History")
for entry in game_state["policy_history"][-5:]:
    st.write(f"{entry['policy']}: Intensity {entry['intensity']}")

st.write(f"Updated Budget: {game_state['budget']}")
st.write(f"Public Approval: {game_state['public_approval']}")
st.write(f"GDP: {game_state['gdp']}")
st.write(f"Unemployment Rate: {game_state['unemployment']}%")
st.write(f"Crime Rate: {game_state['crime_rate']}")

# ✅ **Display Event History**
st.subheader("Event History")
if "event_history" in game_state and game_state["event_history"]:
    for event in game_state["event_history"][-5:]:  # Show last 5 events
        st.write(f"📌 {event}")
else:
    st.write("No major events have occurred yet.")

if st.button("Next Turn"):
    game_state["turns"] += 1
    random_event = trigger_random_event(game_state)  # ✅ Trigger a random event
    save_game_state(game_state)
    check_game_status(game_state)
    st.rerun()
