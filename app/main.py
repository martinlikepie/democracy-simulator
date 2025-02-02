import streamlit as st
import json

# Load policy data
with open("data/policies.json", "r") as file:
    policies = json.load(file)

# Title
st.title("Democracy Simulator")
st.write("Welcome to the interactive democracy simulation.")

# Policy Selection
policy = st.selectbox("Choose a policy to adjust:", list(policies.keys()))

# Policy Intensity
intensity = st.slider("Select policy intensity", 0, 10, 5)

# Apply Policy Button
if st.button("Apply Policy"):
    st.write(f"You selected **{policy}** with intensity level **{intensity}!**")
