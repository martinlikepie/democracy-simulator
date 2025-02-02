import streamlit as st
import json

# Load policy data
with open("data/policies.json", "r") as file:
    policies = json.load(file)

# Load game state
with open("data/game_state.json", "r") as file:
    game_state = json.load(file)

# Title
st.title("Democracy Simulator")
st.write("Welcome to the interactive democracy simulation.")

# Policy Selection
policy = st.selectbox("Choose a policy to adjust:", list(policies.keys()))

# Policy Intensity
intensity = st.slider("Select policy intensity", 0, 10, 5)

# Apply Policy Button - Ensure this is not duplicated
if st.button("Apply Policy", key="apply_policy_button"):
    game_state["budget"] -= intensity * 10
    game_state["public_approval"] += intensity * 2

    # Save updated game state
    with open("data/game_state.json", "w") as file:
        json.dump(game_state, file)

    st.write(f"Updated Budget: {game_state['budget']}")
    st.write(f"Public Approval: {game_state['public_approval']}")
