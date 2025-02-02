import streamlit as st
import json
import os

game_state_file = "data/game_state.json"

def load_game_state():
    if os.path.exists(game_state_file):
        with open(game_state_file, "r") as file:
            return json.load(file)
    return {"budget": 1000, "public_approval": 50, "turns": 1, "policy_history": []}

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
st.write(f"Public Approval: {game_state['approval']}")

# Next Turn Button
if st.button("Next Turn"):
    game_state["turns"] += 1
    save_game_state(game_state)
    st.rerun()
