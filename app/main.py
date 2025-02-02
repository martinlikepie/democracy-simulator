import streamlit as st
import json
import os

game_state_file = "data/game_state.json"

def load_game_state():
    if os.path.exists(game_state_file):
        with open(game_state_file, "r") as file:
            return json.load(file)
    return {
        "budget": 1000, "public_approval": 50, "turns": 1, "policy_history": [],
        "gdp": 100, "unemployment": 5, "crime_rate": 10,
        "citizen_groups": {"Business Owners": 50, "Workers": 50, "Environmentalists": 50}
    }

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
policy = st.selectbox("Choose a policy to adjust:", list(effects.keys()))
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
    save_game_state(game_state)
    check_game_status(game_state)
    st.rerun()
