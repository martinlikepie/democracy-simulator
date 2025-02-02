import streamlit as st
import json
import os

# Ensure data directory exists
data_path = "data"
if not os.path.exists(data_path):
    os.makedirs(data_path)

# Initialize policy data if not present
policies_file = os.path.join(data_path, "policies.json")
if not os.path.exists(policies_file):
    default_policies = {
        "Income Tax": {"cost": 10, "approval": 5},
        "Healthcare Funding": {"cost": 15, "approval": 8},
        "Police Funding": {"cost": 12, "approval": 6},
        "Welfare Spending": {"cost": 14, "approval": 7}
    }
    with open(policies_file, "w") as file:
        json.dump(default_policies, file)

# Initialize game state if not present
game_state_file = os.path.join(data_path, "game_state.json")
if not os.path.exists(game_state_file):
    default_game_state = {"budget": 1000, "public_approval": 50}
    with open(game_state_file, "w") as file:
        json.dump(default_game_state, file)

# Load policy data
with open(policies_file, "r") as file:
    policies = json.load(file)

# Load game state
with open(game_state_file, "r") as file:
    game_state = json.load(file)

# Title
st.title("Democracy Simulator")
st.write("Welcome to the interactive democracy simulation.")

# Policy Selection
policy = st.selectbox("Choose a policy to adjust:", list(policies.keys()))

# Policy Intensity
intensity = st.slider("Select policy intensity", 0, 10, 5)

# Apply Policy Button
if st.button("Apply Policy", key="apply_policy_button"):
    cost = policies[policy]["cost"]
    approval = policies[policy]["approval"]

    # Adjust budget
    game_state["budget"] -= intensity * cost

    # Adjust public approval
    game_state["public_approval"] += intensity * approval

    # Ensure values stay within bounds
    game_state["budget"] = max(0, game_state["budget"])
    game_state["public_approval"] = min(100, max(0, game_state["public_approval"]))

    # Save updated game state
    with open(game_state_file, "w") as file:
        json.dump(game_state, file)

    # Debugging messages (REMOVE after testing)
    st.write(f"Policy applied: {policy}")
    st.write(f"Intensity: {intensity}")
    st.write(f"Cost per unit: {cost}")
    st.write(f"Approval impact per unit: {approval}")
    st.write(f"Updated Budget: {game_state['budget']}")
    st.write(f"Updated Public Approval: {game_state['public_approval']}")
