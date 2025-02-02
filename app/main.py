import streamlit as st
import json
import os
import random

game_state_file = "data/game_state.json"

def load_game_state():
    if os.path.exists(game_state_file):
        with open(game_state_file, "r") as file:
            return json.load(file)
    return {"budget": 1000, "public_approval": 50, "turns": 1, "policy_history": [], "event_history": []}

def save_game_state(state):
    with open(game_state_file, "w") as file:
        json.dump(state, file)

st.title("Democracy Simulator")
st.write("Welcome to the interactive democracy simulation.")

game_state = load_game_state()

# Display current turn
st.subheader(f"Turn: {game_state['turns']}")

# Policy Selection Dropdown
policy = st.selectbox(
    "Choose a policy to adjust:",
    ["Income Tax", "Healthcare Funding", "Police Funding", "Welfare Spending"]
)

# Select Policy Intensity
intensity = st.slider("Select policy intensity", 0, 10, 5)

if st.button("Apply Policy"):
    # Adjust budget and approval based on policy changes
    game_state["budget"] -= intensity * 10
    game_state["public_approval"] += intensity - 5  # Slightly favoring higher intensity
    
    # Save policy decision to history
    game_state["policy_history"].append({"policy": policy, "intensity": intensity})
    
    save_game_state(game_state)
    st.write(f"You selected **{policy}** with intensity level **{intensity}**.")

# Display policy history
if game_state["policy_history"]:
    st.subheader("Policy History")
    for entry in game_state["policy_history"][-5:]:  # Show last 5 decisions
        st.write(f"{entry['policy']}: Intensity {entry['intensity']}")

# Display budget and public approval
st.write(f"Updated Budget: {game_state['budget']}")
st.write(f"Public Approval: {game_state['public_approval']}")

# Define possible random events
events = [
    {"name": "Economic Boom", "effect": {"budget": 100, "public_approval": 5}},
    {"name": "Protest", "effect": {"public_approval": -10}},
    {"name": "Natural Disaster", "effect": {"budget": -150, "public_approval": -5}},
    {"name": "Scientific Breakthrough", "effect": {"public_approval": 10}},
    {"name": "Corruption Scandal", "effect": {"public_approval": -15}}
]

# Function to trigger a random event
def trigger_event():
    event = random.choice(events)  # Pick a random event
    game_state["event_history"].append(event["name"])  # Log event
    
    # Apply effects
    for key, value in event["effect"].items():
        game_state[key] += value  # Modify budget/public approval

# Next Turn Button
if st.button("Next Turn"):
    game_state["turns"] += 1  # Advance turn
    trigger_event()  # Trigger an event
    save_game_state(game_state)
    st.rerun()

# Display Event History
if game_state["event_history"]:
    st.subheader("Event History")
    for event in game_state["event_history"][-5:]:  # Show last 5 events
        st.write(f"🔹 {event}")
