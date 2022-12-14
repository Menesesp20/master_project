import pandas as pd

import pymysql

import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, Integer, Float, Boolean
from sqlalchemy import MetaData
from sqlalchemy import select

from soccerplots.radar_chart import Radar
from soccerplots.utils import add_image

import sys

from PIL import Image

import time

#############################################################################################################################################################

import matplotlib as plt
from matplotlib import font_manager

font_path = 'Fonts/Gagalin-Regular.otf'
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

#Courier New

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()

import matplotlib.pyplot as plt
import streamlit as st

#############################################################################################################################################################
<<<<<<< HEAD
from Functions.data import getDataOPTA
from Functions.data import getDataWyScout

#############################################################################################################################################################
df = getDataWyScout()

#############################################################################################################################################################

eventsPlayers = getDataOPTA()
=======

@st.cache
def load_model():
    
    df = pd.read_csv('Data/WyScout/WyScout.csv')
    return df

df = load_model()

#############################################################################################################################################################

@st.cache
def data():
    eventsPlayers = pd.read_csv('Data/opta/optaData.csv')
    return eventsPlayers

eventsPlayers = data()
>>>>>>> parent of 73d9b2d (update)
eventsPlayers['isTouch'] = eventsPlayers['isTouch'].astype(bool)

# DICTIONARY OF COLORS

clubColors = {'Atl??tico Madrid' : ['#e23829', '#262e62'],
              'Osasuna' : ['#ab172c', '#182c4c'],
              'Getafe' : ['#0b5ea2', '#5ba034'],
              'Granada' : ['#c40d2d', '#e8e8e8'],
              'Levante' : ['#b3043b', '#075ba0'],
              'Rayo Vallecano' : ['#dd2e34', '#e8e8e8'],
              'Celta Vigo' : ['#b7d0e7', '#dc1443'],
              'Espanyol' : ['#338ecc', '#e8b614'],
              'Betis' : ['#158c4b', '#e8e8e8'],
              'Real Sociedad' : ['#0b67ab', '#e8e8e8'],
              'Sevilla' : ['#d41926', '#e8e8e8'],
              'Valencia' : ['#fada0d', '#e8e8e8'],
              'Villarreal' : ['#f2e166', '#065283'],
              'Athletic Club' : ['#ff0000', '#e8e8e8'],
              'Real Madrid' : ['#1a346e', '#e8e8e8'],
              'FC Barcelona' : ['#c2043a', '#06274c'],
              'Deportivo Alav??s' : ['#062494', '#e8e8e8'],
              'Elche' : ['#076235', '#e8e8e8'],
              'Mallorca' : ['#ff0000', '#f9e006'],
              'Valladolid' : ['#5b2482', '#e8e8e8'],
              'Almeria' : ['#ff0000', '#e8e8e8'],
              ###################################
              'Corinthians' : ['#ff0000', '#e8e8e8'],
              'Avai' : ['#00679a', '#e8e8e8'],
              'Flamengo' : ['#ff0000', '#181818'],
              'Palmeiras' : ['#046434', '#e8e8e8'],
              ###################################
              'Manchester City' : ['#7bb1d8', '#062e63'],
              'Liverpool' : ['#d40424', '#e2e1ab']}

#############################################################################################################################################################

sys.path.append('Functions')
sys.path.append('whoscored_scraper')

from Functions import corners, throw

#############################################################################################################################################################

def search_qualifierOPTA(data, event):
  cols = data.columns

  list_Name = pd.DataFrame(columns=cols)

  data.reset_index(inplace=True)

  for idx, row in data.iterrows():
    if event in data['qualifiers'][idx]:
        events = pd.DataFrame([data.iloc[idx][cols].values], columns=cols)
        list_Name = pd.concat([list_Name, events], ignore_index=True)
          
  list_Name = list_Name.loc[~list_Name.index.duplicated(), :]

  return list_Name

#############################################################################################################################################################

first, second, third = st.columns(3)

st.title('Set Pieces')

teams = eventsPlayers.team.unique()

teams = teams.tolist()

teams.insert(0, 'Athletic Club')

teams_choice = first.selectbox('Choose team:', teams)

matchDay = ['All Season']

matchDay_choice = third.selectbox('Choose matchDay:', matchDay)

Viz = ['Corners', 'Throw-In']

Viz_choice = second.selectbox('Choose set piece:', Viz)

eventsPlayers = eventsPlayers.loc[eventsPlayers.team == teams_choice]

cornersData = []

cornersData = search_qualifierOPTA(eventsPlayers, 'CornerTaken')

throwIn = []

throwIn = search_qualifierOPTA(eventsPlayers, 'ThrowIn')

if Viz_choice == 'Corners':

    st.title(f'Corners Analysis')

    cornerPost_choice = st.selectbox('Choose the post:', ['Both', '1st Post', '2nd Post'])

    fig = corners.cornersTaken(cornersData, 'La Liga', teams_choice, matchDay_choice)

    st.pyplot(fig)
    

    if cornerPost_choice == 'Both':
        pass

    elif cornerPost_choice == '1st Post':
        st.header('1st Corner Analysis')
        fig = corners.corners1stPostTaken(cornersData, 'La Liga', teams_choice, matchDay_choice)
        st.pyplot(fig)

    elif cornerPost_choice == '2nd Post':
        st.header('2nd Corner Analysis')
        fig = corners.corners2ndPostTaken(cornersData, 'La Liga', teams_choice, matchDay_choice)
        st.pyplot(fig)

elif Viz_choice == 'Throw-In':

    st.title(f'Throw-In Analysis')

    fig = throw.SetPiece_throwIn(throwIn, 'La Liga', teams_choice, 3, matchDay_choice)

    st.pyplot(fig)