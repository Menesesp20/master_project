import pandas as pd

import streamlit as st

@st.cache
def getDataOPTA():
    eventsPlayers = pd.read_csv('Data/opta/optaData.csv')
    return eventsPlayers

@st.cache
def getDataWyScout():
    wyScout = pd.read_csv('Data/WyScout/WyScout.csv')
    return wyScout