import streamlit as st
import json
import os
import random

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
        "citizen_groups": {"Business Owners": 50, "Workers": 50, "Environmentalists": 50}
    }

    for key, value in defaults.items():
        if key not in game_state:
            game_state[key] = value

    return game_state


def save_game_state(state):
    with open(game_state_file, "w") as file:
        json.dump(state, file)

def trigger_random_event(game_state):
    events = [
        {"name": "Economic Boom", "gdp": 10, "public_approval": 5},
        {"name": "Recession", "gdp": -10, "public_approval": -5},
        {"name": "Scientific Breakthrough", "public_approval": 10},
        {"name": "Corruption Scandal", "public_approval": -10},
        {"name": "Natural Disaster", "budget": -50, "public_approval": -5},
    ]

    if "event_history" not in game_state:
        game_state["event_history"] = []  # Initialize event history if missing

    if random.random() < 0.3:  # 30% chance of an event happening
        event = random.choice(events)
        for key, value in event.items():
            if key != "name":  # Don't try to add "name" to the numbers
                game_state[key] += value

        game_state["event_history"].append(event["name"])
        return event["name"]
    return None

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

if st.button("Next Turn"):
    game_state["turns"] += 1
    random_event = trigger_random_event(game_state)  # Trigger a random event
    save_game_state(game_state)
    check_game_status(game_state)
    st.rerun()

