import streamlit as st
import pandas as pd
from later.data_analysis import get_team
st.set_page_config(page_icon=":bar_chart", layout="wide", page_title= "ROBOTIATORS 888")

st.title("888 Data Analysis")
st.write("Kenneth Wang, 2023")

if "data" not in st.session_state:
    st.session_state.data = pd.read_csv("Prematch Data.csv")

data = st.session_state.data
input_container = st.container()
team_choices = input_container.multiselect(label="Select Teams: ", options=data.iloc[:, 0].values)

if len(team_choices) > 0:
    comp_list = []
    for choice in team_choices:
        pairs = [st.expander(choice)]
        pairs.append(
            pairs[0].write(get_team(choice, data))
        )
        comp_list.append(pairs)
