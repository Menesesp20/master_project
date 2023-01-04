import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl

import warnings
warnings.filterwarnings("ignore")

from mplsoccer import Pitch, VerticalPitch, Radar, FontManager, add_image

from soccerplots.utils import add_image

from highlight_text import  ax_text, fig_text

from soccerplots.utils import add_image

#############################################################################################################################################################

import matplotlib.pyplot as plt
from matplotlib import font_manager

font_path = 'Fonts/Gagalin-Regular.otf'
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

#Courier New

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()

#############################################################################################################################################################

import streamlit as st
from Functions import data as d
#############################################################################################################################################################

df = d.getDataOPTA()
df['isTouch'] = df['isTouch'].astype(bool)
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
              'Cadiz' : ['#f9e310', '#0045a8'],
              ###################################
              'Corinthians' : ['#ff0000', '#e8e8e8'],
              'Avai' : ['#00679a', '#e8e8e8'],
              'Flamengo' : ['#ff0000', '#181818'],
              'Palmeiras' : ['#046434', '#e8e8e8'],
              ###################################
              'Manchester City' : ['#7bb1d8', '#062e63'],
              'Liverpool' : ['#d40424', '#e2e1ab']}

def dataFrame_xTFlow(df, n):

    eventsPlayers = pd.read_csv('Data/opta/optaData.csv')

    eventsPlayers['isTouch'] = eventsPlayers['isTouch'].astype(bool)

    home_Team = df['home_Team'].unique()

    home_Team[0]

    away_Team = df['away_Team'].unique()

    away_Team[0]

    df_Home = df.loc[df.team == home_Team[0]]

    df_Away = df.loc[df.team == away_Team[0]]

    goal_Home = eventsPlayers.loc[(eventsPlayers.team == home_Team[0]) & (eventsPlayers.typedisplayName == 'Goal') & (eventsPlayers.Match_ID == n)]['typedisplayName'].count()

    goal_Away = eventsPlayers.loc[(eventsPlayers.team == away_Team[0]) & (eventsPlayers.typedisplayName == 'Goal') & (eventsPlayers.Match_ID == n)]['typedisplayName'].count()

    home_xT = []
    away_xT = []

    #Criação da lista de jogadores
    Minutes = range(df['minute'].min(), df['minute'].max())

    #Ciclo For de atribuição dos valores a cada jogador
    for minute in Minutes:
        home_xT.append(df_Home.loc[df_Home['minute'] == minute, 'xT'].sum())
        away_xT.append(df_Away.loc[df_Away['minute'] == minute, 'xT'].sum())
    data = {
        'Minutes' : Minutes,
        'Home' : home_Team[0],
        'Away' : away_Team[0],
        'Goal_Home' : goal_Home,
        'Goal_Away' : goal_Away,
        'home_xT' : home_xT,
        'away_xT' : away_xT
        }

    df = pd.DataFrame(data)
    return df


def xT_Flow(df, league, club):

    df['xTH'] = df['home_xT'].rolling(window = 5, min_periods = 0).mean()

    df['xTH'] = round(df['xTH'], 2)

    df['xTA'] = df['away_xT'].rolling(window = 5, min_periods = 0).mean()

    df['xTA'] = round(df['xTA'], 2)

    #Drop rows with NaN values
    df = df.dropna(axis=0, subset=['xTH', 'xTA'])

    fig, ax = plt.subplots(figsize=(20,12))

    #Set color background outside the graph
    fig.set_facecolor('#1e1e1e')

    #Set color background inside the graph
    ax.set_facecolor('#1e1e1e')

    df['xTH'] = df['home_xT'].rolling(window = 5, min_periods = 0).mean()

    df['xTA'] = df['away_xT'].rolling(window = 5, min_periods = 0).mean()

    home = df.Home.unique()
    homeName = home[0]
    color = clubColors.get(homeName)

    away = df.Away.unique()
    awayName = away[0]
    color2 = clubColors.get(awayName)

    Goal_Home = df.Goal_Home.unique()
    Goal_Home = Goal_Home[0]
  
    Goal_Away = df.Goal_Away.unique()
    Goal_Away = Goal_Away[0]

    ax.fill_between(df.Minutes, df['xTH'], 0,
                    where=(df['xTH'] > df['xTA']),
                    interpolate=True, color=color[0], edgecolor='white', lw=3)

    #ax.fill(df.Minutes, df['xTH'], "r", df.Minutes, df['xTA'], "b")

    ax.fill_between(df.Minutes, -abs(df['xTA']), 0,
                    where=(df['xTA'] > df['xTH']),
                    interpolate=True, color=color2[0], edgecolor='white', lw=3)

    #Params for the text inside the <> this is a function to highlight text
    highlight_textprops =\
          [{"color": color[0], "fontweight": 'bold'},
            {"color": color[0], "fontweight": 'bold'},
            {"color":  color2[0], "fontweight": 'bold'},
            {"color":  color2[0], "fontweight": 'bold'}
          ]

    #Title
    Title = fig_text(s = f'<{homeName}>' + ' ' + f'<{Goal_Home}>' + ' ' + '-' + ' ' + f'<{Goal_Away}>' + ' ' + f'<{awayName}>',
                     x = 0.44, y = 0.95, highlight_textprops = highlight_textprops, fontweight='bold', ha='center', va='center', fontsize=40, color='white');

    fig_text(s = 'La Liga 21-22 | xT values based on Karun Singhs model |  xT flow graph | Created by: @menesesp20',
             x = 0.55, y = 0.90, fontweight='bold', ha='center', va='center', fontsize=16, color='white', alpha=0.4);

    # Half Time Line
    halfTime = 45

    ax.axvline(halfTime, color='white', ls='--', lw=2.5)

    diferencialLine = 0

    ax.axhline(diferencialLine, color='white', ls='-', lw=3)

    fig_text(s = 'HALF TIME',
             x = 0.515, y = 0.85,
             fontweight='bold',
             ha='center',fontsize=16, color='white');


    #Atribuição da cor e tamanho das tick labels, the left=False retires the ticks
    ax.tick_params(axis='x', colors='white', labelsize=16)
    ax.tick_params(axis='y', colors='white', labelsize=16, left = False)

    #Setg the color of the line in the spines and retire the spines from the top and right sides
    ax.spines['bottom'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    #Bold the labels
    mpl.rcParams["font.weight"] = "bold"
    mpl.rcParams["axes.labelweight"] = "bold"

    # Club Logo
    fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.08, bottom=0.875, width=0.2, height=0.1)


def dataFrame_touchFlow(df, n):

    eventsPlayers = pd.read_csv('Data/opta/optaData.csv')

    eventsPlayers['isTouch'] = eventsPlayers['isTouch'].astype(bool)

    home_Team = df['home_Team'].unique()

    home_Team[0]

    away_Team = df['away_Team'].unique()

    away_Team[0]

    df_Home = df.loc[df.team == home_Team[0]]

    df_Away = df.loc[df.team == away_Team[0]]

    goal_Home = eventsPlayers.loc[(eventsPlayers.team == home_Team[0]) & (eventsPlayers.typedisplayName == 'Goal') & (eventsPlayers.Match_ID == n)]['typedisplayName'].count()

    goal_Away = eventsPlayers.loc[(eventsPlayers.team != away_Team[0]) & (eventsPlayers.typedisplayName == 'Goal') & (eventsPlayers.Match_ID == n)]['typedisplayName'].count()

    home_Touches = []
    away_Touches = []

    mini = df['minute'].min()
    maxi = df['minute'].max()

    #Criação da lista de jogadores
    Minutes = range(mini, maxi)

    #Ciclo For de atribuição dos valores a cada jogador
    for minute in Minutes:
        home_Touches.append(df_Home.loc[df_Home['minute'] == minute, 'isTouch'].sum())
        away_Touches.append(df_Away.loc[df_Away['minute'] == minute, 'isTouch'].sum())

    data = {
        'Minutes' : Minutes,
        'Home' : home_Team[0],
        'Away' : away_Team[0],
        'Goal_Home' : goal_Home,
        'Goal_Away' : goal_Away,
        'home_Touches' : home_Touches,
        'away_Touches' : away_Touches
        }

    df = pd.DataFrame(data)
    return df


def touch_Flow(df, league, club):

    df['touchHome'] = df['home_Touches'].rolling(window = 5, min_periods = 0).mean()

    df['touchHome'] = round(df['touchHome'], 2)

    df['touchAway'] = df['away_Touches'].rolling(window = 5, min_periods = 0).mean()

    df['touchAway'] = round(df['touchAway'], 2)

    #Drop rows with NaN values
    df = df.dropna(axis=0, subset=['touchHome', 'away_Touches'])

    fig, ax = plt.subplots(figsize=(20,12))

    #Set color background outside the graph
    fig.set_facecolor('#1e1e1e')

    #Set color background inside the graph
    ax.set_facecolor('#1e1e1e')

    home = df.Home.unique()
    homeName = home[0]
    color = clubColors.get(homeName)
  
    away = df.Away.unique()
    awayName = away[0]
    color2 = clubColors.get(awayName)

    Goal_Home = df.Goal_Home.unique()
    Goal_Home = Goal_Home[0]
  
    Goal_Away = df.Goal_Away.unique()
    Goal_Away = Goal_Away[0]

    ax.fill_between(df.Minutes, df['touchHome'], 0,
                    where=(df['touchHome'] > df['touchAway']),
                    interpolate=True, color=color[0], edgecolor='white', lw=3)

    ax.fill_between(df.Minutes, -abs(df['touchAway']), 0,
                    where=(df['touchAway'] > df['touchHome']),
                    interpolate=True, color=color2[0], edgecolor='white', lw=3)

    #Params for the text inside the <> this is a function to highlight text
    highlight_textprops =\
          [{"color": color[0],"fontweight": 'bold'},
            {"color": color[0],"fontweight": 'bold'},
            {"color": color2[0],"fontweight": 'bold'},
            {"color": color2[0],"fontweight": 'bold'}
          ]

    #Title
    Title = fig_text(s = f'<{homeName}>' + ' ' + f'<{Goal_Home}>' + ' ' + '-' + ' ' + f'<{Goal_Away}>' + ' ' + f'<{awayName}>',
                     x = 0.44, y = 0.95, highlight_textprops = highlight_textprops,
                     fontweight='bold', ha='center',fontsize=40, color='white');

    fig_text(s = 'La Liga 21-22 | Touches Final 3rd flow graph | Created by: @menesesp20',
             x = 0.55, y = 0.90,
             fontweight='bold',
             ha='center',fontsize=16, color='white', alpha=0.4);

    # Half Time Line
    halfTime = 45

    ax.axvline(halfTime, color='white', ls='--', lw=2.5)

    diferencialLine = 0

    ax.axhline(diferencialLine, color='white', ls='-', lw=3)

    fig_text(s = 'HALF TIME',
             x = 0.525, y = 0.85,
             fontweight='bold',
             ha='center',fontsize=16, color='white');

    #Atribuição da cor e tamanho das tick labels, the left=False retires the ticks
    ax.tick_params(axis='x', colors='white', labelsize=16)
    ax.tick_params(axis='y', colors='white', labelsize=16, left = False)

    #Setg the color of the line in the spines and retire the spines from the top and right sides
    ax.spines['bottom'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    #Bold the labels
    mpl.rcParams["font.weight"] = "bold"
    mpl.rcParams["axes.labelweight"] = "bold"

    # Club Logo
    fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.08, bottom=0.875, width=0.2, height=0.1)