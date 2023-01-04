import pandas as pd

import streamlit as st

@st.cache(allow_output_mutation=True)
def getDataOPTA():
    eventsPlayers = pd.read_csv('Data/opta/optaData.csv')
    return eventsPlayers

@st.cache(allow_output_mutation=True)
def getDataWyScout():
    wyScout = pd.read_csv('Data/WyScout/WyScout.csv')
    return wyScout