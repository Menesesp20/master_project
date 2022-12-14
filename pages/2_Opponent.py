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

import matplotlib.pyplot as plt

from matplotlib import font_manager

font_path = 'Fonts/Gagalin-Regular.otf'
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

#Courier New

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()

import streamlit as st

#############################################################################################################################################################

#############################################################################################################################################################
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
eventsPlayers['isTouch'] = eventsPlayers['isTouch'].astype(bool)

# DICTIONARY OF COLORS

clubColors = {'Atlético Madrid' : ['#e23829', '#262e62'],
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
              'Deportivo Alavés' : ['#062494', '#e8e8e8'],
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

from Functions import dashboard as ds
from Functions import player as pl
from Functions import Game as fc

#############################################################################################################################################################
    
graphs = ['Passing Network', 'Heat Map', 'xT Heat Map', 'Goal kicks', 'Crosses', 'Switch Play', 'xT Field', 'Area Covered Front Players']

graphs_choice = st.sidebar.selectbox('What do you want to analyze?', graphs)

if graphs_choice == 'Goal kicks':

    first, second = st.columns(2)

    leagues = eventsPlayers.League.unique()

    leagues = leagues.tolist()

    league_choice = first.selectbox('Choose league:', leagues)

    clubDF = eventsPlayers.loc[eventsPlayers.League == league_choice]

    teams = clubDF.team.unique()

    teams = teams.tolist()

    teams.remove('Athletic Club')

    teams_choice = second.selectbox('Choose team:', teams)

    fig = fc.GoalKick(teams_choice, league_choice, 'WhoScored')

    st.pyplot(fig)

elif graphs_choice == 'Area Covered Front Players':

    first, second, third = st.columns(3)

    leagues = ['La Liga', 'Premier League', 'Ligue 1', 'Serie A', 'Bundesliga', 'Mundial']

    league_choice = first.selectbox('Choose league:', leagues)

    clubDF = eventsPlayers.loc[eventsPlayers.League == league_choice]

    teams = clubDF.team.unique()

    teams = teams.tolist()

    teams.remove('Athletic Club')

    teams_choice = second.selectbox('Choose team:', teams)

    club = eventsPlayers[eventsPlayers.team == teams_choice]

    players = club.name.unique()
    players = players.tolist()

    players_choice = first.selectbox('Choose player :', players)

    players2 = club.name.unique()
    players2 = players2.tolist()

    players_choice2 = second.selectbox('Choose player 2 :', players2)

    players3 = club.name.unique()
    players3 = players3.tolist()

    players_choice3 = third.selectbox('Choose player 3 :', players3)

    matchDay = eventsPlayers.Match_ID.unique()

    matchDay = matchDay.tolist()

    matchDay = sorted(matchDay)

    matchDay.append('All Season')

    matchDay.insert(0, 'All Season')

    matchDay_choice = third.selectbox('Choose MatchDay:', matchDay)

    fig = pl.dashboardTerritory(eventsPlayers, league_choice, teams_choice, matchDay_choice, players_choice, players_choice2, players_choice3)
    
    st.pyplot(fig)

elif graphs_choice == 'xT Field':

    st.title('Where do they create the most danger?')

    first, second, third = st.columns(3)

    leagues = ['La Liga', 'Premier League', 'Ligue 1', 'Serie A', 'Bundesliga', 'Mundial']

    league_choice = first.selectbox('Choose league:', leagues)

    clubDF = eventsPlayers.loc[eventsPlayers.League == league_choice]

    teams = clubDF.team.unique()

    teams = teams.tolist()

    teams.remove('Athletic Club')

    teams_choice = second.selectbox('Choose team:', teams)

    matchDay = eventsPlayers.Match_ID.unique()

    matchDay = matchDay.tolist()
    
    matchDay = sorted(matchDay)

    matchDay.append('All Season')

    matchDay.insert(0, 'All Season')

    matchDay_choice = third.selectbox('Choose MatchDay:', matchDay)

    fig = ds.finalThird(eventsPlayers, league_choice, teams_choice, matchDay_choice, 10)

    st.pyplot(fig)

elif graphs_choice == 'Crosses':

    first, second, third, fourth = st.columns(4)

    leagues = ['La Liga', 'Premier League', 'Ligue 1', 'Serie A', 'Bundesliga', 'Mundial']

    league_choice = first.selectbox('Choose league:', leagues)

    clubDF = eventsPlayers.loc[eventsPlayers.League == league_choice]

    teams = clubDF.team.unique()

    teams = teams.tolist()

    teams.remove('Athletic Club')

    teams_choice = second.selectbox('Choose team:', teams)

    club = eventsPlayers[eventsPlayers.team == teams_choice]

    players = club.name.unique()

    players = players.tolist()

    players.append('All Team')

    players.insert(0, 'All Team')

    players_choice = third.selectbox('Choose player:', players)

    matchWeek = eventsPlayers.Match_ID.unique()

    matchWeek = matchWeek.tolist()

    matchWeek.sort()

    matchDay_choice = fourth.selectbox('Choose MatchDay:', matchWeek)

    if players_choice != 'All Team':
        fig = ds.Cross(eventsPlayers, league_choice, teams_choice, matchDay_choice, players_choice)
    
        st.pyplot(fig)

    elif players_choice == 'All Team':
        fig = ds.Cross(eventsPlayers, league_choice, teams_choice, matchDay_choice)
    
        st.pyplot(fig)

elif graphs_choice == 'Switch Play':

    first, second, third, fourth = st.columns(4)

    leagues = ['La Liga', 'Premier League', 'Ligue 1', 'Serie A', 'Bundesliga', 'Mundial']

    league_choice = first.selectbox('Choose league:', leagues)

    clubDF = eventsPlayers.loc[eventsPlayers.League == league_choice]

    teams = clubDF.team.unique()

    teams = teams.tolist()

    teams.remove('Athletic Club')

    teams_choice = second.selectbox('Choose team:', teams)

    club = eventsPlayers[eventsPlayers.team == teams_choice]

    players = club.name.unique()

    players = players.tolist()

    players.append('All Team')

    players.insert(0, 'All Team')

    players_choice = third.selectbox('Choose player:', players)

    matchWeek = eventsPlayers.Match_ID.unique()

    matchWeek = matchWeek.tolist()

    matchWeek.sort()
    
    matchDay_choice = fourth.selectbox('Choose MatchDay:', matchWeek)

    fig = ds.switchPlay(eventsPlayers, league_choice, teams_choice, matchDay_choice, players_choice)

    st.pyplot(fig)

elif graphs_choice == 'Heat Map':

    first, second, third = st.columns(3)

    teams = eventsPlayers.team.unique()

    teams = teams.tolist()

    teams.remove('Athletic Club')

    teams_choice = first.selectbox('Choose team:', teams)

    matchWeek = eventsPlayers.Match_ID.unique()

    matchWeek = matchWeek.tolist()

    matchWeek.sort()
    
    matchDay_choice = second.selectbox('Choose MatchDay:', matchWeek)

    leagues = ['La Liga', 'Premier League', 'Ligue 1', 'Serie A', 'Bundesliga', 'Mundial']

    league_choice = third.selectbox('Choose league:', leagues)

    fig = fc.touch_Map(teams_choice, league_choice, matchDay_choice)

    st.pyplot(fig)

elif graphs_choice == 'xT Heat Map':

    st.title('Where are we creating more danger?')

    first, second, third = st.columns(3)

    teams = eventsPlayers.team.unique()

    teams = teams.tolist()

    teams.remove('Athletic Club')

    teams_choice = first.selectbox('Choose team:', teams)

    club = eventsPlayers[eventsPlayers.team == teams_choice]

    matchWeek = eventsPlayers.Match_ID.unique()

    matchWeek = matchWeek.tolist()

    matchWeek.sort()
    
    matchDay_choice = second.selectbox('Choose MatchDay:', matchWeek)

    leagues = ['La Liga', 'Premier League', 'Ligue 1', 'Serie A', 'Bundesliga', 'Mundial']

    league_choice = third.selectbox('Choose league:', leagues)

    fig = fc.heatMap_xT(teams_choice, league_choice, matchDay_choice)

    st.pyplot(fig)

elif graphs_choice == 'Passing Network':

    first, second, third = st.columns(3)

    leagues = ['La Liga', 'Premier League', 'Ligue 1', 'Serie A', 'Bundesliga', 'Mundial']

    league_choice = first.selectbox('Choose league:', leagues)

    clubDF = eventsPlayers.loc[eventsPlayers.League == league_choice]

    teams = clubDF.team.unique()

    teams = teams.tolist()

    teams.remove('Athletic Club')

    teams_choice = second.selectbox('Choose team:', teams)

    matchWeek = eventsPlayers.Match_ID.unique()

    matchWeek = matchWeek.tolist()

    matchWeek.sort()
    
    matchDay_choice = third.selectbox('Choose MatchDay:', matchWeek)

    fig = fc.passing_networkWhoScored(teams_choice, league_choice, matchDay_choice, afterSub=None)

    st.pyplot(fig)