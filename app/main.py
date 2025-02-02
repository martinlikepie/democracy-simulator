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
        "Income Tax": {"cost": -10, "approval": -2, "growth": 5},  # Generates budget, reduces approval
        "Healthcare Funding": {"cost": 15, "approval": 8, "growth": 0},  # No economy boost, high approval
        "Police Funding": {"cost": 12, "approval": 6, "growth": 1},  # Small economic boost
        "Welfare Spending": {"cost": 14, "approval": 7, "growth": -1}  # Improves approval but slows economy
    }
    with open(policies_file, "w") as file:
        json.dump(default_policies, file)

# Initialize game state if not present
game_state_file = os.path.join(data_path, "game_state.json")
if not os.path.exists(game_state_file):
    default_game_state = {"budget": 1000, "public_approval": 50, "turns": 1, "economic_growth": 2}
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

# Show Current Game Stats
st.subheader(f"Turn: {game_state['turns']}")
st.write(f"Budget: {game_state['budget']}")
st.write(f"Public Approval: {game_state['public_approval']}%")
st.write(f"Economic Growth Rate: {game_state['economic_growth']}%")

# Policy Selection
policy = st.selectbox("Choose a policy to adjust:", list(policies.keys()))

# Policy Intensity
intensity = st.slider("Select policy intensity", 0, 10, 5)

# Apply Policy Button
if st.button("Apply Policy", key="apply_policy_button"):
    cost = policies[policy]["cost"]
    approval = policies[policy]["approval"]
    growth = policies[policy]["growth"]

    # Adjust budget
    game_state["budget"] -= intensity * cost

    # Adjust public approval
    game_state["public_approval"] += intensity * approval

    # Adjust economic growth factor
    game_state["economic_growth"] += growth

    # Ensure values stay within bounds
    game_state["budget"] = max(0, game_state["budget"])
    game_state["public_approval"] = min(100, max(0, game_state["public_approval"]))

    # Save updated game state
    with open(game_state_file, "w") as file:
        json.dump(game_state, file)

    # Show changes
    st.success(f"Applied {policy} at intensity {intensity}.")
    st.write(f"New Budget: {game_state['budget']}")
    st.write(f"New Public Approval: {game_state['public_approval']}")
    st.write(f"Economic Growth Rate: {game_state['economic_growth']}")

# Next Turn Button
if st.button("Next Turn"):
    # Apply economic growth to budget
    game_state["budget"] += game_state["economic_growth"] * 10

    # Reduce approval slightly each turn (natural dissatisfaction)
    game_state["public_approval"] -= 1

    # Ensure values stay within bounds
    game_state["budget"] = max(0, game_state["budget"])
    game_state["public_approval"] = min(100, max(0, game_state["public_approval"]))

    # Increment turn
    game_state["turns"] += 1

    # Save game state
    with open(game_state_file, "w") as file:
        json.dump(game_state, file)

    # Refresh UI
    st.experimental_rerun()
