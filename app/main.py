import streamlit as st

# Title
st.title("Democracy Simulator")
st.write("Welcome to the interactive democracy simulation.")

# Policy Selection
policy = st.selectbox(
    "Choose a policy to adjust:",
    ["Income Tax", "Healthcare Funding", "Police Funding", "Welfare Spending"]
)

# Policy Intensity
intensity = st.slider("Select policy intensity", 0, 10, 5)

st.write(f"You selected **{policy}** with intensity level **{intensity}**.")
