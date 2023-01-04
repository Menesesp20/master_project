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

import Scouting as sc
import radar as rd

from Functions import player as pl

#############################################################################################################################################################

def search_qualifierOPTA(df, list_Name, event):
  cols = ['Match_ID', 'name', 'x', 'y',
          'endX', 'endY', 'minute', 'second', 'typedisplayName', 'outcomeTypedisplayName',
          'qualifiers', 'satisfiedEventsTypes', 'teamId', 'team']

  list_Name = pd.DataFrame(columns=cols)

  df.reset_index(inplace=True)

  for idx, row in df.iterrows():
    if event in df['qualifiers'][idx]:
        events = pd.DataFrame([df.iloc[idx][cols].values], columns=cols)
        list_Name = pd.concat([list_Name, events], ignore_index=True)
          
  list_Name = list_Name.loc[~list_Name.index.duplicated(), :]

  return list_Name

#############################################################################################################################################################

scouting_choice = st.sidebar.selectbox('Choose what you want to assess:', ['Player Radar', 'Player Similarity', 'Player Role', 'Player Dashboard', 'Scouting Report'])

if scouting_choice == 'Player Radar':

#############################################################################################################################################################

    continent = ['Europe 1st tier', 'Europe 2nd Tier', 'South America', 'North America', 'Asian']

    continent_choice = st.sidebar.selectbox('Choose continent:', continent)

    st.title(f'Player Radar')

    first, second, third = st.columns(3)

    if continent_choice == 'Europe 1st tier':

        leagues = ['La Liga', 'Premier League', 'Serie A', 'Ligue 1', 'Bundesliga']

        leaguesCompare = ['La Liga', 'Premier League', 'Serie A', 'Ligue 1', 'Bundesliga']

        leagues_choice = first.selectbox('Choose league:', leagues)

    elif continent_choice == 'Europe 2nd tier':

        leagues = ['Liga Bwin', 'First Divison Belgium', 'Super Liga Turkey', 'Super Liga Serbia', 'Super Liga Denamark', 'Eredivisie']

        leaguesCompare = ['Liga Bwin', 'First Divison Belgium', 'Super Liga Turkey', 'Super Liga Serbia', 'Super Liga Denamark', 'Eredivisie']

        leagues_choice = first.selectbox('Choose league:', leagues)

    elif continent_choice == 'South America':

        leagues = ['Liga Profesional Argentina', 'Liga BetPlay Colombia', 'Brasileirao']

        leaguesCompare = ['Liga Profesional Argentina', 'Liga BetPlay Colombia', 'Brasileirao']

        leagues_choice = first.selectbox('Choose league:', leagues)

    elif continent_choice == 'North America':

        leagues = ['Liga Mexico', 'MLS']

        leaguesCompare = ['Liga Mexico', 'MLS']

        leagues_choice = first.selectbox('Choose league:', leagues)

    elif continent_choice == 'Asia':

        leagues = ['J1 League', 'K League 1']

        leaguesCompare = ['J1 League', 'K League 1']

        leagues_choice = first.selectbox('Choose league:', leagues)

    df1 = df.loc[df.Comp == leagues_choice]

    clubs = df1.Team.unique()

    clubs = clubs.tolist()

    clubs.insert(0, 'Athletic Bilbao')

    teams_choice = second.selectbox('Choose team:', clubs)

    Club = df1.loc[df1.Team == teams_choice]

    players = Club.Player.unique()
    players = players.tolist()
    players.insert(0, 'Iker Muniain')

    players_choice = third.selectbox('Choose player :', players)

    st.sidebar.title(f'Compare Players')

    compare = ['No', 'Yes']

    compare_choice = st.sidebar.selectbox('Do you want to campare?', compare)

    Role = ['Center Back', 'Full Back', 'Defensive Midfield', 'Midfield', 'Offensive Midfield', 'Winger', 'Forward']

    Role_choice = st.selectbox('Choose the role you want to analyze the player', Role)

    center_Back = ['Non-penalty goals/90', 'Offensive duels %', 'Progressive runs/90',
                    'Passes %', 'Forward passes %', 'Forward passes/90', 'Progressive passes/90',
                'PAdj Interceptions', 'PAdj Sliding tackles', 'Defensive duels/90', 'Defensive duels %',
                'Aerial duels/90', 'Aerial duels %', 'Shots blocked/90']

    full_Back = ['Successful dribbles %', 'Touches in box/90', 'Offensive duels %', 'Progressive runs/90', 'Crosses/90', 'Deep completed crosses/90',
                'Passes %', 'Deep completions/90', 'Progressive passes/90', 'Key passes/90', 'Third assists/90',
                'PAdj Interceptions', 'Defensive duels %', 'Aerial duels/90', 'Aerial duels %']

    defensive_Midfield  = ['xG/90', 'Shots', 'Progressive runs/90', 'Successful dribbles %',
                        'Passes %', 'Forward passes %', 'Forward passes/90', 'Progressive passes/90','PAdj Sliding tackles',
                        'PAdj Interceptions', 'Aerial duels %', 'Defensive duels %', 'Offensive duels %']

    Midfield  = ['xG/90', 'Shots', 'Progressive runs/90', 'Successful dribbles %',
                'Passes %', 'Forward passes %', 'Forward passes/90', 'Progressive passes/90',
                'Key passes/90', 'Second assists/90', 'Assists', 'xA',
                'PAdj Interceptions', 'Aerial duels %', 'Defensive duels %',]

    offensive_Midfield = ['xG/90', 'Goals/90', 'Progressive runs/90', 'Successful dribbles %',
                        'xA/90', 'Deep completions/90', 'Passes to penalty area/90',
                        'Touches in box/90', 'Key passes/90', 'Passes final 1/3 %',
                        'Passes penalty area %', 'Progressive passes/90',
                        'Succ defensive actions/90', 'PAdj Interceptions', 'Aerial duels %', 'Defensive duels %']

    offensive_Midfield_BS = ['Successful dribbles %', 'xA/90', 'Deep completions/90', 'Passes to penalty area/90',
                        'Key passes/90', 'Passes final 1/3 %']

    Winger = ['Successful dribbles %', 'Goals', 'xG/90',
            'xA/90', 'Touches in box/90', 'Dribbles/90', 'Passes to penalty area/90', 'Key passes/90',
            'Progressive runs/90', 'Crosses/90', 'Deep completed crosses/90',
            'Offensive duels/90', 'PAdj Interceptions']

    Forward = ['Goals', 'xG/90', 'Shots on target, %', 'Goal conversion, %',
            'Successful dribbles %', 'xA/90', 'Touches in box/90', 'Dribbles/90',
            'Offensive duels/90', 'PAdj Interceptions', 'Aerial duels/90', 'Aerial duels %']

    if compare_choice == 'No':

        if Role_choice == 'Center Back':
            fig = sc.PizzaChart(df, center_Back, players_choice, leagues_choice)

            st.pyplot(fig)

        elif Role_choice == 'Full Back':
            fig = sc.PizzaChart(df, full_Back, players_choice, leagues_choice)

            st.pyplot(fig)

        elif Role_choice == 'Defensive Midfield':
            fig = sc.PizzaChart(df, defensive_Midfield, players_choice, leagues_choice)

            st.pyplot(fig)

        elif Role_choice == 'Midfield':
            fig = sc.PizzaChart(df, Midfield, players_choice, leagues_choice)

            st.pyplot(fig)

        elif Role_choice == 'Offensive Midfield':
            fig = sc.PizzaChart(df, offensive_Midfield, players_choice, leagues_choice)

            st.pyplot(fig)

        elif Role_choice == 'Winger':
            fig = sc.PizzaChart(df, Winger, players_choice, leagues_choice)
            st.pyplot(fig)

        elif Role_choice == 'Forward':
            fig = sc.PizzaChart(df, Forward, players_choice, leagues_choice)
            st.pyplot(fig)

    #############################################################################################################################################################

        attributes = ['Creation', 'Offensive', 'Defensive']

        attributes_choice = st.selectbox('Choose which attributes you want to analyze the player', attributes)

        if attributes_choice == 'Defensive':

            defensive = center_Back

            offensive = Forward

            creation = offensive_Midfield

            st.title(players_choice + ' ' + attributes_choice + ' ' + f'Attributes')

            fig = sc.beeswarm(df, players_choice, defensive)

            st.pyplot(fig)

        elif attributes_choice == 'Offensive':

            defensive = center_Back

            offensive = Forward

            creation = offensive_Midfield

            st.title(players_choice + ' ' + attributes_choice + ' ' + f'Attributes')

            fig = sc.beeswarm(df, players_choice, offensive)

            st.pyplot(fig)

        elif attributes_choice == 'Creation':

            defensive = center_Back

            offensive = Forward

            creation = offensive_Midfield

            st.title(players_choice + ' ' + attributes_choice + ' ' + f'Attributes')

            fig = sc.beeswarm(df, players_choice, creation)

            st.pyplot(fig)


#############################################################################################################################################################

    elif compare_choice == 'Yes':

        first, second, third = st.columns(3)

        leaguesCompare_choice = first.selectbox('Choose league to compare:', leaguesCompare)

        df2 = df.loc[df.Comp == leaguesCompare_choice]

        teamsCompare = df2.Team.unique()

        teamsCompare_choice = second.selectbox('Choose team to compare:', teamsCompare)

        ClubCompare = df2[df2.Team == teamsCompare_choice]

        playersCompare = ClubCompare.Player.unique()

        playersCompare_choice = third.selectbox('Choose player to compare :', playersCompare)

        if Role_choice == 'Center Back':
            fig = rd.radar_chart_compare(df, players_choice, playersCompare_choice, center_Back)

            st.pyplot(fig)

        elif Role_choice == 'Full Back':
            fig = rd.radar_chart_compare(df, players_choice, playersCompare_choice, full_Back)

            st.pyplot(fig)

        elif Role_choice == 'Defensive Midfield':
            fig = rd.radar_chart_compare(df, players_choice, playersCompare_choice, defensive_Midfield)

            st.pyplot(fig)

        elif Role_choice == 'Midfield':
            fig = rd.radar_chart_compare(df, players_choice, playersCompare_choice, Midfield)

            st.pyplot(fig)

        elif Role_choice == 'Offensive Midfield':
            fig = rd.radar_chart_compare(df, players_choice, playersCompare_choice, offensive_Midfield)
            st.pyplot(fig)

        elif Role_choice == 'Winger':
            fig = rd.radar_chart_compare(df, players_choice, playersCompare_choice, Winger)
            st.pyplot(fig)

        elif Role_choice == 'Forward':
            fig = rd.radar_chart_compare(df, players_choice, playersCompare_choice, Forward)
            st.pyplot(fig)

        #############################################################################################################################################################

            

elif scouting_choice == 'Player Similarity':

    first, second, third, four = st.columns(4)

    leagues = ['La Liga', 'Premier League', 'Serie A', 'Ligue 1', 'Bundesliga']

    leagues_choice = first.selectbox('Choose league:', leagues)

    df = df.loc[df.Comp == leagues_choice]

    teams = df.Team.unique()

    teams_choice = second.selectbox('Choose team:', teams)

    Club = df[df.Team == teams_choice]

    players = Club.Player.unique()

    players_choice = third.selectbox('Choose player :', players)

    center_Back = ['Non-penalty goals/90', 'Offensive duels %', 'Progressive runs/90',
                    'Passes %', 'Forward passes %', 'Forward passes/90', 'Progressive passes/90',
                'PAdj Interceptions', 'PAdj Sliding tackles', 'Defensive duels/90', 'Defensive duels %',
                'Aerial duels/90', 'Aerial duels %', 'Shots blocked/90']

    full_Back = ['Successful dribbles %', 'Touches in box/90', 'Offensive duels %', 'Progressive runs/90', 'Crosses/90', 'Deep completed crosses/90',
                'Passes %', 'Deep completions/90', 'Progressive passes/90', 'Key passes/90', 'Third assists/90',
                'PAdj Interceptions', 'Defensive duels %', 'Aerial duels/90', 'Aerial duels %']

    defensive_Midfield  = ['xG/90', 'Shots', 'Progressive runs/90', 'Successful dribbles %',
                        'Passes %', 'Forward passes %', 'Forward passes/90', 'Progressive passes/90','PAdj Sliding tackles',
                        'PAdj Interceptions', 'Aerial duels %', 'Defensive duels %', 'Offensive duels %']

    Midfield  = ['xG/90', 'Shots', 'Progressive runs/90', 'Successful dribbles %',
                'Passes %', 'Forward passes %', 'Forward passes/90', 'Progressive passes/90',
                'Key passes/90', 'Second assists/90', 'Assists', 'xA',
                'PAdj Interceptions', 'Aerial duels %', 'Defensive duels %']

    offensive_Midfield = ['xG/90', 'Goals/90', 'Progressive runs/90', 'Successful dribbles %',
                        'xA/90', 'Deep completions/90', 'Passes to penalty area/90',
                        'Touches in box/90', 'Key passes/90', 'Passes final 1/3 %',
                        'Passes penalty area %', 'Progressive passes/90',
                        'Succ defensive actions/90', 'PAdj Interceptions', 'Aerial duels %', 'Defensive duels %']

    Winger = ['Successful dribbles %', 'Goals', 'xG/90',
            'xA/90', 'Touches in box/90', 'Dribbles/90', 'Passes to penalty area/90', 'Key passes/90',
            'Progressive runs/90', 'Crosses/90', 'Deep completed crosses/90',
            'Offensive duels/90', 'PAdj Interceptions']

    Forward = ['Goals', 'xG/90', 'Shots on target, %', 'Goal conversion, %',
            'Successful dribbles %', 'xA/90', 'Touches in box/90', 'Dribbles/90',
            'Offensive duels/90', 'PAdj Interceptions', 'Aerial duels/90', 'Aerial duels %']

    role_choice = four.selectbox('Choose role :', ['Winger', 'Full Back', 'Defensive Midfield', 'Midfield', 'Offensive Midfield', 'Center Back', 'Forward'])

    @st.cache
    def load_model():
        df = pd.read_csv('Data/WyScout/WyScout.csv')
        return df

    df = load_model()

    df.drop_duplicates(subset=['Player'], keep='first', inplace=True)

    df.drop(['Team within selected timeframe', 'On loan'], axis=1, inplace=True)

    df['Market value'] = [str(x) for x in df['Market value']]


    age = df.Age.unique()
    age = age.tolist()
    age = sorted(age)
    age.insert(0, 'All')
    age.remove(0.0)

    Age_choice = st.sidebar.selectbox('Choose age :', age)

    comp = df.Comp.unique()
    comp = comp.tolist()
    comp = sorted(comp)
    comp.insert(0, 'All leagues')

    comp_choice = st.sidebar.selectbox('Choose competition :', comp)

    market = df['Market value'].unique()
    market = market.tolist()
    market = sorted(market)
    mini = min(market)
    maxi = max(market)

    start_value, end_value = st.sidebar.select_slider(
        'Select the market value range ',
        options=market,
        value=(mini, maxi))

    fig = sc.similarityDashboard(df, Age_choice, start_value, end_value, comp_choice, players_choice, role_choice)

    st.pyplot(fig)


elif scouting_choice == 'Scouting Report':

    first, second, third, four = st.columns(4)

    continent = ['Europe 1st tier', 'Europe 2nd Tier', 'South America', 'North America', 'Asian']

    continent_choice = st.sidebar.selectbox('Choose continent:', continent)

    if continent_choice == 'Europe 1st tier':

        leagues = ['La Liga', 'Premier League', 'Serie A', 'Ligue 1', 'Bundesliga']

        leaguesCompare = ['La Liga', 'Premier League', 'Serie A', 'Ligue 1', 'Bundesliga']

        leagues_choice = first.selectbox('Choose league:', leagues)

    elif continent_choice == 'Europe 2nd tier':

        leagues = ['Liga Bwin', 'First Divison Belgium', 'Super Liga Turkey', 'Super Liga Serbia', 'Super Liga Denamark', 'Eredivisie']

        leaguesCompare = ['Liga Bwin', 'First Divison Belgium', 'Super Liga Turkey', 'Super Liga Serbia', 'Super Liga Denamark', 'Eredivisie']

        leagues_choice = first.selectbox('Choose league:', leagues)

    elif continent_choice == 'South America':

        leagues = ['Liga Profesional Argentina', 'Liga BetPlay Colombia', 'Brasileirao']

        leaguesCompare = ['Liga Profesional Argentina', 'Liga BetPlay Colombia', 'Brasileirao']

        leagues_choice = first.selectbox('Choose league:', leagues)

    elif continent_choice == 'North America':

        leagues = ['Liga Mexico', 'MLS']

        leaguesCompare = ['Liga Mexico', 'MLS']

        leagues_choice = first.selectbox('Choose league:', leagues)

    elif continent_choice == 'Asia':

        leagues = ['J1 League', 'K League 1']

        leaguesCompare = ['J1 League', 'K League 1']

        leagues_choice = first.selectbox('Choose league:', leagues)

    df1 = df.loc[df.Comp == leagues_choice]

    clubs = df1.Team.unique()

    clubs = clubs.tolist()

    teams_choice = second.selectbox('Choose team:', clubs)

    Club = df1.loc[df1.Team == teams_choice]

    players = Club.Player.unique()
    players = players.tolist()

    players_choice = third.selectbox('Choose player :', players)

    dfReport = df.copy()

    dfReport = sc.szcore_df(dfReport)

    sc.playerAbility(dfReport)

    sc.playerRole(dfReport)

    sc.rating(dfReport)

    offensive_Player = four.selectbox('Is an offensive player? :', ['Yes', 'No'])

    if offensive_Player == 'Yes':
        fig = dfSimilar = sc.scoutReport(dfReport, players_choice, leagues_choice, False, False)
    elif offensive_Player == 'No':
        fig = dfSimilar = sc.scoutReport(dfReport, players_choice, leagues_choice, False, True)

    st.pyplot(fig)

elif scouting_choice == 'Player Role':

    first, second, third, four = st.columns(4)

    continent = ['Europe 1st tier', 'Europe 2nd Tier', 'South America', 'North America', 'Asian']

    continent_choice = st.sidebar.selectbox('Choose continent:', continent)

    if continent_choice == 'Europe 1st tier':

        leagues = ['Ligue 1', 'La Liga', 'Premier League', 'Serie A', 'Bundesliga']

        leaguesCompare = ['La Liga', 'Premier League', 'Serie A', 'Ligue 1', 'Bundesliga']

        leagues_choice = first.selectbox('Choose league:', leagues)

    elif continent_choice == 'Europe 2nd tier':

        leagues = ['Liga Bwin', 'First Divison Belgium', 'Super Liga Turkey', 'Super Liga Serbia', 'Super Liga Denamark', 'Eredivisie']

        leaguesCompare = ['Liga Bwin', 'First Divison Belgium', 'Super Liga Turkey', 'Super Liga Serbia', 'Super Liga Denamark', 'Eredivisie']

        leagues_choice = first.selectbox('Choose league:', leagues)

    elif continent_choice == 'South America':

        leagues = ['Liga Profesional Argentina', 'Liga BetPlay Colombia', 'Brasileirao']

        leaguesCompare = ['Liga Profesional Argentina', 'Liga BetPlay Colombia', 'Brasileirao']

        leagues_choice = first.selectbox('Choose league:', leagues)

    elif continent_choice == 'North America':

        leagues = ['Liga Mexico', 'MLS']

        leaguesCompare = ['Liga Mexico', 'MLS']

        leagues_choice = first.selectbox('Choose league:', leagues)

    elif continent_choice == 'Asia':

        leagues = ['J1 League', 'K League 1']

        leaguesCompare = ['J1 League', 'K League 1']

        leagues_choice = first.selectbox('Choose league:', leagues)

    df1 = df.loc[df.Comp == leagues_choice]

    clubs = df1.Team.unique()

    clubs = clubs.tolist()
    clubs.insert(0, 'PSG')

    teams_choice = second.selectbox('Choose team:', clubs)

    Club = df1.loc[df1.Team == teams_choice]

    players = Club.Player.unique()
    players = players.tolist()
    players.insert(0, 'L. Messi')

    players_choice = third.selectbox('Choose player :', players)

    role = ['Midfielder', 'Forward', 'Center Back', 'Full Back']

    role_choice = four.selectbox('Choose team:', role)

    dfRole = df.copy()

    dfRole = sc.szcore_df(dfRole)

    sc.playerAbility(dfRole)

    sc.playerRole(dfRole)

    sc.rating(dfRole)

    fig = sc.role_Chart(dfRole, players_choice, role_choice)

    st.pyplot(fig)

elif scouting_choice == 'Player Dashboard':

    first, second, third = st.columns(3)

    league = ['La Liga', 'Ligue 1', 'Serie A', 'Bundesliga', 'Premier League']

    leagues_choice = first.selectbox('Choose league:', league)

    df1 = eventsPlayers.loc[eventsPlayers.League == leagues_choice]

    clubs = df1.team.unique()

    clubs = clubs.tolist()
    clubs.remove('Athletic Club')
    clubs.insert(0, 'Athletic Club')

    teams_choice = second.selectbox('Choose team:', clubs)

    Club = df1.loc[df1.team == teams_choice]

    players = Club.name.unique()
    players = players.tolist()

    players_choice = third.selectbox('Choose player :', players)

    position_Choice = second.selectbox('Choose what dashboard you want to see:', ['Offensive', 'Defensive'])

    matchDay = eventsPlayers.Match_ID.unique()

    matchDay = matchDay.tolist()

    matchDay = sorted(matchDay)
    matchDay_choice = first.selectbox('Choose MatchDay:', matchDay)

    if position_Choice == 'Offensive':

        fig = pl.dashboardOffensive(eventsPlayers, leagues_choice, teams_choice, players_choice, matchDay_choice)

        st.pyplot(fig)

    elif position_Choice == 'Defensive':

        fig = pl.dashboardDeffensive(eventsPlayers, leagues_choice, teams_choice, matchDay_choice, players_choice)

        st.pyplot(fig)
















