import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import to_rgba
import matplotlib as mpl
import matplotlib.patches as patches

import warnings
warnings.filterwarnings("ignore")

from mplsoccer import Pitch, VerticalPitch, add_image

from soccerplots.utils import add_image

from highlight_text import  ax_text, fig_text

from soccerplots.utils import add_image

from sklearn.cluster import KMeans
from scipy import stats

import math

from pandas.core.common import SettingWithCopyWarning

import warnings
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

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

@st.cache
def load_model():
	  return pd.read_csv('Data/opta/optaData.csv')

eventsPlayers =  load_model()

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


def search_qualifierOPTA(df, list_Name, event):
  cols = ['Match_ID', 'name', 'playerId', 'relatedPlayerId', 'x', 'y', 'endX', 'endY', 'minute', 'second', 'expandedMinute', 'typedisplayName', 'outcomeTypedisplayName', 'qualifiers', 'satisfiedEventsTypes', 'teamId']

  list_Name = pd.DataFrame(columns=cols)

  df.reset_index(inplace=True)

  for idx, row in df.iterrows():
    if event in df['qualifiers'][idx]:
        events = pd.DataFrame([df.iloc[idx][cols].values], columns=cols)
        list_Name = pd.concat([list_Name, events], ignore_index=True)
          
  list_Name = list_Name.loc[~list_Name.index.duplicated(), :]

  return list_Name

#############################################################################################################################################################

def convex_hull(df, x, y, col_Player, col_Event, event, Player, club, title=None):

  color = clubColors.get(club)

  df = df[(df[col_Player] == Player) & (df[col_Event] == event)]

  convex = df[(np.abs(stats.zscore(df[['x','y']])) < 1).all(axis=1)]

  #convex = df[(np.abs(stats.zscore(df[['x','y']])) < .5).all(axis=1)]

  #print(convex)

  # setup pitch
  pitch = VerticalPitch(pitch_type='opta', line_zorder=2,
                pitch_color='#181818', line_color='#efefef')
  
  fig, ax = pitch.draw(figsize=(12, 8))
  fig.set_facecolor('#181818')

  hull = pitch.convexhull(convex[x], convex[y])

  poly = pitch.polygon(hull, ax=ax, edgecolor='white', facecolor=color[0], alpha=0.4, linestyle='--', linewidth=2.5)

  scatter = pitch.scatter(df[x], df[y], ax=ax, edgecolor='black', facecolor=color[0]) 
  scatter = pitch.scatter(x=convex[x].mean(), y=convex[y].mean(), ax=ax, c='white', edgecolor=color[0], s=700, zorder=2)

  #--------------------------------------------------------------------------------------------------------------------------------------------------------------

  #def uniao(nome):
   # if type(nome) == list:
    #  return ' '.join(nome)
    #return nome

 # eventsPlayers['name'] = eventsPlayers['name'].apply(lambda x: uniao(x.split(" ")[:-1])) + eventsPlayers['name'].apply(lambda x: uniao(x.split(" ")[1:]))
  #eventsPlayers['name'] = eventsPlayers['name'][0][0] + eventsPlayers['name'][0][1]

  #pitch.annotate(text=f'{Player}', xytext=(convex[x].mean(), convex[y].mean()), xy=(convex[x].mean(), convex[y].mean()), ha='center', va='center', color='#00659c', ax=ax)
  title = title
  
  ax.set_title(title, fontsize = 20, color='white')

#############################################################################################################################################################

def switchPlay(df, league, club, gameID, playerName):

    if (playerName == 'All Team') & (gameID == 'All Season'):
        passes_Left = df.loc[(df['typedisplayName'] == 'Pass') & (df.y < 50) & (df.endY > 60) & (df.endX > df.x + 15) &
                             (df.team == club)]

    elif (playerName == 'All Season') & (gameID == 'All Season'):
        passes_Left = df.loc[(df['typedisplayName'] == 'Pass') & (df.y < 50) & (df.endY > 60) & (df.endX > df.x + 15) &
                             (df.team == club)]

    elif (playerName == 'All Team') & (gameID != 'All Season'):
        passes_Left = df.loc[(df['typedisplayName'] == 'Pass') & (df.y < 50) & (df.endY > 60) & (df.endX > df.x + 15) &
                             (df.Match_ID == gameID) & (df.team == club)]

    elif (playerName == 'All Season') & (gameID != 'All Season'):
        passes_Left = df.loc[(df['typedisplayName'] == 'Pass') & (df.y < 50) & (df.endY > 60) & (df.endX > df.x + 15) &
                             (df.Match_ID == gameID) & (df.team == club)]

    elif (playerName != 'All Team') & (gameID == 'All Season'):
        passes_Left = df.loc[(df['typedisplayName'] == 'Pass') & (df.y < 50) & (df.endY > 60) & (df.endX > df.x + 15) &
                             (df.name == playerName) & (df.team == club)]

    elif (playerName != 'All Season') & (gameID == 'All Season'):
        passes_Left = df.loc[(df['typedisplayName'] == 'Pass') & (df.y < 50) & (df.endY > 60) & (df.endX > df.x + 15) &
                             (df.name == playerName) & (df.team == club)]

    elif (playerName != 'All Team') & (gameID != 'All Season'):
        passes_Left = df.loc[(df['typedisplayName'] == 'Pass') & (df.y < 50) & (df.endY > 60) & (df.endX > df.x + 15) &
                             (df.Match_ID == gameID) & (df.name == playerName)]

    elif (playerName != 'All Season') & (gameID != 'All Season'):
        passes_Left = df.loc[(df['typedisplayName'] == 'Pass') & (df.y < 50) & (df.endY > 60) & (df.endX > df.x + 15) &
                             (df.Match_ID == gameID) & (df.name == playerName)]

    sucess_Left = passes_Left.loc[passes_Left['outcomeTypedisplayName'] == 'Successful']

    unsucess_Left = passes_Left.loc[passes_Left['outcomeTypedisplayName'] == 'Unsuccessful']

    ###############################################################################################################################################

    if (playerName == 'All Team') & (gameID == 'All Season'):
        passes_Right = df.loc[(df['typedisplayName'] == 'Pass') & (df.y > 50) & (df.endY < 40) & (df.endX > df.x + 15) &
                              (df.team == club)]

    elif (playerName == 'All Season') & (gameID == 'All Season'):
        passes_Right = df.loc[(df['typedisplayName'] == 'Pass') & (df.y > 50) & (df.endY < 40) & (df.endX > df.x + 15) &
                              (df.team == club)]

    elif (playerName == 'All Team') & (gameID != 'All Season'):
        passes_Right = df.loc[(df['typedisplayName'] == 'Pass') & (df.y > 50) & (df.endY < 40) & (df.endX > df.x + 15) &
                              (df.Match_ID == gameID) & (df.team == club)]

    elif (playerName == 'All Season') & (gameID != 'All Season'):
        passes_Right = df.loc[(df['typedisplayName'] == 'Pass') & (df.y > 50) & (df.endY < 40) & (df.endX > df.x + 15) &
                              (df.Match_ID == gameID) & (df.team == club)]

    elif (playerName != 'All Team') & (gameID == 'All Season'):
        passes_Right = df.loc[(df['typedisplayName'] == 'Pass') & (df.y > 50) & (df.endY < 40) & (df.endX > df.x + 15) &
                              (df.name == playerName) & (df.team == club)]

    elif (playerName != 'All Season') & (gameID == 'All Season'):
        passes_Right = df.loc[(df['typedisplayName'] == 'Pass') & (df.y > 50) & (df.endY < 40) & (df.endX > df.x + 15) &
                              (df.name == playerName) & (df.team == club)]

    elif (playerName != 'All Team') & (gameID != 'All Season'):
        passes_Right = df.loc[(df['typedisplayName'] == 'Pass') & (df.y > 50) & (df.endY < 40) & (df.endX > df.x + 15) &
                              (df.Match_ID == gameID) & (df.name == playerName)]

    elif (playerName != 'All Season') & (gameID != 'All Season'):
        passes_Right = df.loc[(df['typedisplayName'] == 'Pass') & (df.y > 50) & (df.endY < 40) & (df.endX > df.x + 15) &
                              (df.Match_ID == gameID) & (df.name == playerName)]

    sucess_Right = passes_Right.loc[passes_Right['outcomeTypedisplayName'] == 'Successful']

    unsucess_Right = passes_Right.loc[passes_Right['outcomeTypedisplayName'] == 'Unsuccessful']

    ###############################################################################################################################################

    if gameID != 'All Season':

        homeAway = df.loc[df.Match_ID == gameID]
        home = homeAway.loc[(homeAway.team == club)]
        away = homeAway.loc[(homeAway.team != club)]

        home = home.team.unique()
        homeName = home[0]
        color = clubColors.get(homeName)

        away = away.team.unique()
        awayName = away[0]

    elif gameID == 'All Season':
        color = clubColors.get(club)

    ###############################################################################################################################################

    fig, ax = plt.subplots(figsize=(18,14))

    pitch = Pitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                  pitch_color='#E8E8E8', line_color='#181818', line_zorder=1, linewidth=5, spot_scale=0.005)

    pitch.draw(ax=ax)

    fig.set_facecolor('#E8E8E8')

    ###############################################################################################################################################

    #Params for the text inside the <> this is a function to highlight text
    highlight_textprops =\
        [{"color": color[0],"fontweight": 'bold'},
         {"color": color[0],"fontweight": 'bold'}]

    fig_text(s = f'<{club}>' + "<'s>" +  ' ' + 'Switch pass map',
             x = 0.52, y = 0.97,
             highlight_textprops = highlight_textprops,
             color='#181818', ha='center', fontsize=50);

    if gameID != 'All Season':
        fig_text(s =f'<{homeName}>' + ' ' + 'vs' + ' ' + f'<{awayName}> |' + ' ' + str(gameID) + ' ' +'| Season 21-22 | @menesesp20',
                x = 0.52, y = 0.9, ha='center', va='center',
                color='#181818', alpha=0.7, fontweight='bold', fontsize=20);

    elif gameID == 'All Season':
        fig_text(s ='| Season 21-22 | @menesesp20',
                x = 0.5, y = 0.9, ha='center', va='center',
                color='#181818', alpha=0.7, fontweight='bold', fontsize=20);        

    fig_text(s = 'Switches attempted:' + ' ' + str(len(passes_Left) + len(passes_Right)),
             x = 0.25, y = 0.78, ha='center', va='center',
             color='#181818', alpha=0.7, fontweight='bold', fontsize=20);

    ###############################################################################################################################################

    pitch.arrows(sucess_Left.x, sucess_Left.y, sucess_Left.endX, sucess_Left.endY,
                 color='#11ff06', ax=ax,
                 width=2, headwidth=5, headlength=5)


    #Criação das setas que simbolizam os passes realizados bem sucedidos
    pitch.arrows(unsucess_Left.x, unsucess_Left.y, unsucess_Left.endX, unsucess_Left.endY,
                 color='#181818', alpha=0.7, ax=ax,
                 width=2, headwidth=5, headlength=5)

    ###############################################################################################################################################

    pitch.arrows(sucess_Right.x, sucess_Right.y, sucess_Right.endX, sucess_Right.endY,
                 color='#11ff06', ax=ax,
                 width=2, headwidth=5, headlength=5,
                 label='Passes Successful')
    
    #Criação das setas que simbolizam os passes realizados bem sucedidos
    pitch.arrows(unsucess_Right.x, unsucess_Right.y, unsucess_Right.endX, unsucess_Right.endY,
                 color='#181818', alpha=0.7, ax=ax,
                 width=2, headwidth=5, headlength=5,
                 label='Passes unsuccessful')

    ###############################################################################################################################################

    #Criação da legenda
    l = ax.legend(bbox_to_anchor=(0.02, 0), loc='upper left', facecolor='#181818', framealpha=0, labelspacing=.7)
    #Ciclo FOR para atribuir a #181818 color na legend
    for text in l.get_texts():
        text.set_color("#181818")

    ###############################################################################################################################################

    # Club Logo
    fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.08, bottom=0.88, width=0.2, height=0.09)

    fig_text(s = 'Attacking Direction',
                 x = 0.5, y = 0.17,
                 color='#181818', fontweight='bold',
                 ha='center', va='center',
                 fontsize=14)

    # ARROW DIRECTION OF PLAY
    ax.annotate('', xy=(0.3, -0.07), xycoords='axes fraction', xytext=(0.7, -0.07), 
            arrowprops=dict(arrowstyle="<-", color='#181818', lw=2))
#############################################################################################################################################################

def Cross(df, league, club, matchDay, playerName=None):

        cross = []

        if 'level_0' in df.columns:
                df.drop(['level_0'], axis=1, inplace=True)
        else:
                pass

        cross = search_qualifierOPTA(df, cross, 'Cross')

        if (playerName != None) & (matchDay != 'All Season'):
                player = cross.loc[(cross.name == playerName) & (cross.x != 99) & (cross.x != 1) & (cross.Match_ID == matchDay)]

        if (playerName != None) & (matchDay == 'All Season'):
                player = cross.loc[(cross.name == playerName) & (cross.x != 99) & (cross.x != 1)]

        elif (playerName == None) & (matchDay == 'All Season'):
                player = cross.loc[(cross.x != 99) & (cross.x != 1)]

        elif (playerName == None) & (matchDay != 'All Season'):
                player = cross.loc[(cross.x != 99) & (cross.x != 1) & (cross.Match_ID == matchDay)]

        pitch = VerticalPitch(pitch_type='opta', line_zorder=2,
                                half=True,
                                pitch_color='#E8E8E8', line_color='#181818')

        fig, ax = pitch.draw(figsize=(15, 10))
        fig.set_facecolor('#E8E8E8')

        pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                                ['#E8E8E8', '#3d0000', '#ff0000'], N=25)

        player['x'] = player['x'].astype(float)
        player['y'] = player['y'].astype(float)

        scatter = pitch.scatter(player['x'], player['y'], ax=ax, edgecolor='#181818', facecolor='#E8E8E8', zorder=2)

        bs = pitch.bin_statistic(player['x'], player['y'], bins=(5, 5))
        heatmap = pitch.heatmap(bs, edgecolors='#E8E8E8', ax=ax, cmap=pearl_earring_cmap)

        ######################################################################################################################

        #ax.axvline(18, c='#ff0000', linestyle='-', LineWidth=2)
        #ax.axvline(38, c='#ff0000', linestyle='-', LineWidth=2)
        #ax.axvline(82, c='#ff0000', linestyle='-', LineWidth=2)
        #ax.axvline(62, c='#ff0000', linestyle='-', LineWidth=2)

        ######################################################################################################################

        ax.axhline(90, c='#E8E8E8', linestyle='-', lw=2.5)
        ax.axhline(80, c='#E8E8E8', linestyle='-', lw=2.5)
        ax.axhline(69, c='#E8E8E8', linestyle='-', lw=2.5)
        ax.axhline(60, c='#E8E8E8', linestyle='-', lw=2.5)

        ######################################################################################################################
        # 90, 80:90, 69:80, 60:69
        # RIGHT 1
        zone1 = player.loc[(player['x'] >= 90) & (player['y'] <= 18)]
        if (round(len(zone1) / len(player), 2) * 100) == 0:
                pass
        else:
                # TOTAL RIGHT 1
                fig_text(s = str((round(len(zone1) / len(player) * 100, 2))) + '%',
                        x = 0.80, y = 0.85,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################

        # RIGHT 2
        zone2 = player.loc[(player['x'] >= 80) & (player['x'] < 90) & (player['y'] <= 18)]
        if (round(len(zone2) / len(player), 2) * 100) == 0:
                pass
        else:
                # TOTAL RIGHT 2
                fig_text(s = str((round(len(zone2) / len(player) * 100, 2))) + '%',
                        x = 0.80, y = 0.67,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################

        # RIGHT 3
        zone3 = player.loc[(player['x'] >= 69) & (player['x'] < 80) & (player['y'] <= 18)]
        if (round(len(zone3) / len(player), 2) * 100) == 0:
                pass
        else:
                # TOTAL RIGHT 3
                fig_text(s = str((round(len(zone3) / len(player) * 100, 2))) + '%',
                        x = 0.80, y = 0.5,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################

        # RIGHT 4
        zone4 = player.loc[(player['x'] >= 60) & (player['x'] < 69) & (player['y'] <= 18)]
        if (round(len(zone4) / len(player), 2) * 100) == 0:
                pass
        else:
                # TOTAL RIGHT 4
                fig_text(s = str((round(len(zone4) / len(player) * 100, 2))) + '%',
                        x = 0.80, y = 0.33,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################
        ######################################################################################################################
        ######################################################################################################################
        # 90, 80:90, 69:80, 60:69

        # MID RIGHT 1
        zone1_1 = player.loc[(player['x'] >= 90) & (player['y'] > 18) & (player['y'] <= 38)]
        if (round(len(zone1_1) / len(player), 2) * 100) == 0:
                pass
        else:
                # MID RIGHT 1
                fig_text(s = str((round(len(zone1_1) / len(player) * 100, 2))) + '%',
                        x = 0.65, y = 0.85,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################

        # MID RIGHT 2
        zone1_2 = player.loc[(player['x'] >= 80) & (player['x'] < 90) & (player['y'] >= 18) & (player['y'] <= 38)]
        if (round(len(zone1_2) / len(player), 2) * 100) == 0:
                pass
        else:
                # MID RIGHT 2
                fig_text(s = str((round(len(zone1_2) / len(player) * 100, 2))) + '%',
                        x = 0.65, y = 0.67,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################

        # MID RIGHT 3
        zone1_3 = player.loc[(player['x'] >= 69) & (player['x'] < 80) & (player['y'] >= 18) & (player['y'] <= 38)]
        if (round(len(zone1_3) / len(player), 2) * 100) == 0:
                pass
        else:
                # MID RIGHT 3
                fig_text(s = str((round(len(zone1_3) / len(player) * 100, 2))) + '%',
                        x = 0.65, y = 0.5,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################

        # MID RIGHT 4
        zone1_4 = player.loc[(player['x'] >= 60) & (player['x'] < 69) & (player['y'] >= 18) & (player['y'] <= 38)]
        if (round(len(zone1_4) / len(player), 2) * 100) == 0:
                pass
        else:
                # MID RIGHT 4
                fig_text(s = str((round(len(zone1_4) / len(player) * 100, 2))) + '%',
                        x = 0.65, y = 0.33,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################
        ######################################################################################################################
        ######################################################################################################################
        # 90, 80:90, 69:80, 60:69

        # MID LEFT 1
        zone2_1 = player.loc[(player['x'] >= 90) & (player['y'] < 82) & (player['y'] >= 68)]
        if (round(len(zone2_1) / len(player), 2) * 100) == 0:
                pass
        else:
                # MID LEFT 1
                fig_text(s = str((round(len(zone2_1) / len(player) * 100, 2))) + '%',
                        x = 0.35, y = 0.85,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################

        # MID LEFT 2
        zone2_2 = player.loc[(player['x'] >= 80) & (player['x'] < 90) & (player['y'] < 82) & (player['y'] >= 68)]
        if (round(len(zone2_2) / len(player), 2) * 100) == 0:
                pass
        else:
                # MID LEFT 2
                fig_text(s = str((round(len(zone2_2) / len(player) * 100, 2))) + '%',
                        x = 0.35, y = 0.67,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################

        # MID LEFT 3
        zone3_3 = player.loc[(player['x'] >= 69) & (player['x'] < 80) & (player['y'] < 82) & (player['y'] >= 68)]
        if (round(len(zone3_3) / len(player), 2) * 100) == 0:
                pass
        else:
                # MID LEFT 3
                fig_text(s = str((round(len(zone3_3) / len(player) * 100, 2))) + '%',
                        x = 0.35, y = 0.5,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################

        # MID LEFT 4
        zone4_4 = player.loc[(player['x'] >= 60) & (player['x'] < 69) & (player['y'] < 82) & (player['y'] >= 68)]
        if (round(len(zone4_4) / len(player), 2) * 100) == 0:
                pass
        else:
                # MID LEFT 4
                fig_text(s = str((round(len(zone4_4) / len(player) * 100, 2))) + '%',
                        x = 0.35, y = 0.33,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################
        ######################################################################################################################
        ######################################################################################################################
        # 90, 80:90, 69:80, 60:69
        # LEFT 1
        zone5 = player.loc[(player['x'] >= 90) & (player['y'] > 82)]
        if (round(len(zone5) / len(player), 2) * 100) == 0:
                pass
        else:
                # LEFT 1
                fig_text(s = str((round(len(zone5) / len(player) * 100, 2))) + '%',
                        x = 0.2, y = 0.85,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################

        # LEFT 2
        zone6 = player.loc[(player['x'] >= 80) & (player['x'] < 90) & (player['y'] >= 82)]
        if (round(len(zone6) / len(player), 2) * 100) == 0:
                pass
        else:
                # LEFT 2
                fig_text(s = str((round(len(zone6) / len(player) * 100, 2))) + '%',
                        x = 0.2, y = 0.67,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################

        # LEFT 3
        zone7 = player.loc[(player['x'] >= 69) & (player['x'] < 80) & (player['y'] >= 82)]
        if (round(len(zone7) / len(player), 2) * 100) == 0:
                pass
        else:
                # LEFT 3
                fig_text(s = str((round(len(zone7) / len(player)* 100, 2))) + '%',
                        x = 0.2, y = 0.5,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################

        # LEFT 4
        zone8 = player.loc[(player['x'] >= 60) & (player['x'] < 69) & (player['y'] >= 82)]
        if (round(len(zone8) / len(player), 2) * 100) == 0:
                pass
        else:
                # LEFT 4
                fig_text(s = str((round(len(zone8) / len(player) * 100, 2))) + '%',
                        x = 0.2, y = 0.33,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=25);
        
        color = clubColors.get(club)

        matchDay = df.Match_ID.unique()
        matchDay = str(matchDay)
        matchDay = matchDay[1]

        #Params for the text inside the <> this is a function to highlight text
        highlight_textprops =\
                [{"color": color[0],"fontweight": 'bold'}]

        if playerName == None:
                fig_text(s ='Where they cross?',
                        x = 0.5, y = 1.12,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=50);

                fig_text(s = 'Season 21-22 | @menesesp20',
                        x = 0.5, y = 1.05,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=16, alpha=0.7);
        else:
                fig_text(s =f'<{playerName}>' + ' ' + 'Crosses',
                        x = 0.54, y = 1.12, highlight_textprops = highlight_textprops ,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=50);

                fig_text(s = 'MatchDay:' + ' ' + matchDay + ' ' + '| Season 21-22 | @menesesp20',
                        x = 0.53, y = 1.05,
                        color='#181818', fontweight='bold', ha='center' ,fontsize=16, alpha=0.7);

        # Club Logo
        fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.12, bottom=1.02, width=0.2, height=0.1)

#############################################################################################################################################################

#Automatização do processo de criação do gráfico de campo de futebol com os passes realizados
def event_playerOffensive(df, col_name, col_outcome, event_name, col_player, player_name, label, title):

  player = df[df[col_player] == player_name]

  event = player[player[col_name] == event_name]

  successful = player[(player[col_name] == event_name) & (player[col_outcome] == 0)]

  #Atribuição do tamanho do gráfico através do ax
  fig, ax = plt.subplots(figsize=(18,14))

  fig.set_facecolor('#181818')
  # setup pitch
  pitch = VerticalPitch(pitch_type='opta', line_zorder=2,
                pitch_color='#181818', line_color='#efefef')
  #Visualizar o gráfico do campo de futebol
  pitch.draw(ax=ax)

  #Criação das setas que simbolizam os passes realizados bem sucedidos
  pitch.scatter(event.x, event.y,
                c='#c70216', marker='*', s=500,
                ax=ax, label=label + ':' + ' ' + f'{len(event)}' + ' ' + '(' + f'{len(successful)}' + ' ' + 'Successful' + ')' )

  #--------------------------------------------------------------------------------------------------------------------------------------------------------------

  #Criação da legenda
  l = ax.legend(bbox_to_anchor=(0, 0), loc='upper left', facecolor='white', framealpha=.05, labelspacing=.7)
  #Ciclo FOR para atribuir a white color na legend
  for text in l.get_texts():
      text.set_color("white")

#############################################################################################################################################################

#Automatização do processo de criação do gráfico de campo de futebol com os passes realizados
def event_playerDefensive(df, col_name, col_outcome, ball_Recovery, Tackle, Interception, Aerial, clearance, col_player, player_name, club):

  color = clubColors.get(club)

  player = df[df[col_player] == player_name]

  ballRecovery = player[player[col_name] == ball_Recovery]

  ballRecovery_successful = player[(player[col_name] == ball_Recovery) & (player[col_outcome] == 0)]

  tackle = player[player[col_name] == Tackle]

  tackle_successful = player[(player[col_name] == Tackle) & (player[col_outcome] == 0)]

  interception = player[player[col_name] == Interception]

  interception_successful = player[(player[col_name] == Interception) & (player[col_outcome] == 0)]

  aerial = player[player[col_name] == Aerial]

  aerial_successful = player[(player[col_name] == Aerial) & (player[col_outcome] == 0)]

  Clearance = player[player[col_name] == clearance]

  clearance_successful = player[(player[col_name] == clearance) & (player[col_outcome] == 0)]

  #--------------------------------------------------------------------------------------------------------------------------------------------------------------

  #Atribuição do tamanho do gráfico através do ax
  fig, ax = plt.subplots(figsize=(18,14))

  fig.set_facecolor('#181818')
  # setup pitch
  pitch = VerticalPitch(pitch_type='opta', line_zorder=2,
                pitch_color='#181818', line_color='#efefef')
  #Visualizar o gráfico do campo de futebol
  pitch.draw(ax=ax)

  #event 1 - Star
  pitch.scatter(ballRecovery.x, ballRecovery.y,
                c=color[0], marker='*', s=500,
                ax=ax, label=ball_Recovery + ':' + ' ' + f'{len(ballRecovery)}')
  
  #event 2 - Star
  pitch.scatter(tackle.x, tackle.y,
                c=color[0], marker='x', s=500,
                ax=ax, label=Tackle + ':' + ' ' + f'{len(tackle)}' + ' ' + '(' + f'{len(tackle_successful)}' + ' ' + 'Successful' + ')' )
  
  #event 3 - Star
  pitch.scatter(interception.x, interception.y,
                c=color[0], marker='H', s=500,
                ax=ax, label=Interception + ':' + ' ' + f'{len(interception)}')
  
  #event 4 - Star
  pitch.scatter(aerial.x, aerial.y,
                c=color[0], marker='^', s=500,
                ax=ax, label=Aerial + ':' + ' ' + f'{len(aerial)}' + ' ' + '(' + f'{len(aerial_successful)}' + ' ' + 'Successful' + ')' )
  
  #event 5 - Star
  pitch.scatter(Clearance.x, Clearance.y,
                c=color[0], marker='p', s=500,
                ax=ax, label=clearance + ':' + ' ' + f'{len(Clearance)}')

#--------------------------------------------------------------------------------------------------------------------------------------------------------------

  legend_properties = {'weight':'bold',
                       'size': 11}

  #Criação da legenda
  l = ax.legend(bbox_to_anchor=(0, 0), loc='upper left', facecolor='white', framealpha=0, labelspacing=1.3, prop=legend_properties)

  #Ciclo FOR para atribuir a white color na legend
  for text in l.get_texts():
      text.set_color("white")


#############################################################################################################################################################

#Automatização do processo de criação do gráfico de campo de futebol com os passes realizados
def convex_hullDefensive(df, player_name, league, club):

  df = df.loc[(df['name'] == player_name) & (df['x'] <= 50) & ((df['typedisplayName'] == 'BallRecovery') |
                                                (df['typedisplayName'] == 'Tackle') |
                                                (df['typedisplayName'] == 'Interception') |
                                                (df['typedisplayName'] == 'Aerial') |
                                                (df['typedisplayName'] == 'Clearance'))]
  #Successful defensive actions
  succ = df.loc[df['outcomeTypedisplayName'] == 'Successful']

  #Unsuccessful defensive actions
  insucc = df.loc[df['outcomeTypedisplayName'] == 'Unsuccessful']
  
  #Tackle rate
  tackle = df.loc[df['typedisplayName'] == 'Tackle']

  tackle_successful = df[(df['typedisplayName'] == 'Tackle') & (df['outcomeTypedisplayName'] == 'Successful')]

  tackle_Rate = round((len(tackle_successful) / len(tackle)) * 100, 2)

  #Aerial rate
  aerial = df[df['typedisplayName'] == 'Aerial']

  aerial_successful = df[(df['typedisplayName'] == 'Aerial') & (df['outcomeTypedisplayName'] == 'Successful')]

  aerial_Rate = round((len(aerial_successful) / len(aerial) * 100) , 2)

  # Plotting the pitch

  fig, ax = plt.subplots(figsize=(18,14))

  pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                        pitch_color='#181818', line_color='white', line_zorder=1, linewidth=5, spot_scale=0.005)

  pitch.draw(ax=ax)

  fig.set_facecolor('#181818')

  convex = df.loc[(np.abs(stats.zscore(df[['x','y']])) < 1).all(axis=1)]

  hull = pitch.convexhull(convex['x'], convex['y'])

  poly = pitch.polygon(hull, ax=ax, edgecolor='white', facecolor='white', alpha=0.3, linestyle='--', linewidth=2.5)

  scatter1 = pitch.scatter(succ['x'], succ['y'], ax=ax, marker='8', edgecolor='white', alpha=0.8, facecolor='none', hatch='//////', linestyle='--', s=150)

  scatter2 = pitch.scatter(insucc['x'], insucc['y'], ax=ax, marker='8', edgecolor='#ff0000', facecolor='none', hatch='//////', linestyle='--',  s=150)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------

  #Params for the text inside the <> this is a function to highlight text
  highlight_textpropsSuccessfu =\
      [{"color": "white","fontweight": 'bold'}
      ]

  #Legend Successfull Actions
  fig_text(s = '<Successfull Actions>',
            x = 0.638, y = 0.68, highlight_textprops = highlight_textpropsSuccessfu,
            fontweight='bold', ha='center', fontsize=12, color='white');
            
#--------------------------------------------------------------------------------------------------------------------------------------------------------------

  #Params for the text inside the <> this is a function to highlight text
  highlight_textpropsUnsuccessful =\
      [{"color": "#ff0000", "fontweight": 'bold', 'alpha' : 0.8}
      ]

  #Legend Unsuccessfull Actions
  fig_text(s = '<Unsuccessfull Actions>',
            x = 0.632, y = 0.66,
            highlight_textprops = highlight_textpropsUnsuccessful,
            fontweight='bold', ha='center',
            fontsize=12, color='white');

#--------------------------------------------------------------------------------------------------------------------------------------------------------------

  #Legend Tackle
  fig_text(s = 'Tackle Rate' + ' ' + f'{tackle_Rate}' + '%',
            x = 0.385, y = 0.68,
            fontweight='bold' ,ha='center',
            fontsize=12, color='white');
  #Legend Aerial     
  fig_text(s = 'Aerial Rate' + ' ' + f'{aerial_Rate}' + '%',
            x = 0.385, y = 0.66,
            fontweight='bold', ha='center',
            fontsize=12, color='white');

  #Defensive Actions included
  fig_text(s = 'Defensive action include' + ' ' + 'BallRecovery,' + ' ' + 'Tackle,' + ' ' + 'Interception,' + ' ' + 'Aerial,' + ' ' + 'Clearance',
            x = 0.512, y = 0.11,
            fontweight='bold', ha='center',
            fontsize=11, color='white');

#--------------------------------------------------------------------------------------------------------------------------------------------------------------

  #Linha média do eixo x
  plt.axhline(df['x'].mean(), c='#ff0000', linestyle='--', LineWidth=2)

  #Defensive Actions included
  fig_text(s = 'Average\nline of\nengagement:' + ' ' + str(round(df['x'].mean(),2 )) + 'm.',
           x = 0.273, y = 0.35,
           fontweight='bold', ha='center',
           fontsize=14, color='white');

#--------------------------------------------------------------------------------------------------------------------------------------------------------------

  #Params for the text inside the <> this is a function to highlight text
  highlight_textprops =\
    [{"color": "white","fontweight": 'bold'}]

  fig_text(s =f'<{player_name}>' + ' ' + 'Defensive Actions',
            x = 0.52, y = 0.97,
            ha='center', va='center',
            highlight_textprops = highlight_textprops, color='white', fontweight='bold',
            fontsize=30);

  fig_text(s ='Season 21-22' + ' ' + league,
            x = 0.52, y = 0.935,
            ha='center', va='center',
            color='white', fontweight='bold',
            fontsize=16);

  # Club Logo
  fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.18, bottom=0.90, width=0.2, height=0.09)


#############################################################################################################################################################


def convex_hull_HeatMap(df, x, y, club, col_Player=None, col_Event=None, event=None, Player=None, label=None):

  color = clubColors.get(club)

  df = df[(df[col_Player] == Player) & (df[col_Event] == event)]

  # setup pitch
  pitch = Pitch(pitch_type='opta', line_zorder=2,
                pitch_color='#181818', line_color='#efefef')

  fig, ax = pitch.draw(figsize=(12, 8))
  fig.set_facecolor('#181818')

  pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                        ['#181818', color[0]], N=10)
  bs = pitch.bin_statistic(df.x, df.y, bins=(12, 8))
  heatmap = pitch.heatmap(bs, edgecolors='#181818', ax=ax, cmap=pearl_earring_cmap)

  #filter that dataframe to exclude outliers. Anything over a z score of 2 will be excluded for the data points
  convex = df[(np.abs(stats.zscore(df[['x','y']])) < .5).all(axis=1)]

  hull = pitch.convexhull(convex[x], convex[y])

  poly = pitch.polygon(hull, ax=ax, edgecolor='white', facecolor='white', alpha=0.3, linestyle='--', linewidth=2.5)

  scatter = pitch.scatter(df[x], df[y], ax=ax, edgecolor='white', facecolor='black', alpha=0.3)

  scatter = pitch.scatter(x=convex[x].mean(), y=convex[y].mean(), ax=ax, c='white', edgecolor=color[0], s=700, zorder=2,
                          label = label)

  #--------------------------------------------------------------------------------------------------------------------------------------------------------------

  legend_properties = {'weight':'bold',
                       'size': 11}

  l = ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.052), facecolor='white', framealpha=0, prop=legend_properties)
  
  #Ciclo FOR para atribuir a white color na legend
  for text in l.get_texts():
      text.set_color("white")

#############################################################################################################################################


def touch_Map(df, col_Game, gameID, x, y, col_Event,  event, league, club, col_Player=None, Player=None):

        color = clubColors.get(club)

        if (Player != None) & (gameID == 'All Season'):
                df = df.loc[(df[col_Player] == Player) & (df[col_Event] == event)]
        
        elif (Player != None) & (gameID != 'All Season'):
                df = df.loc[(df[col_Game] == gameID) & (df[col_Player] == Player) & (df[col_Event] == event)]

        elif gameID == 'All Season':
                df = df.loc[(df[col_Event] == event)]
        else:
                df = df.loc[(df[col_Game] == gameID) & (df['team'] == club) & (df['isTouch'] == True)]

        # Plotting the pitch

        fig, ax = plt.subplots(figsize=(18,14))

        pitch = Pitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                                pitch_color='#181818', line_color='white', line_zorder=3, linewidth=5, spot_scale=0.00)

        pitch.draw(ax=ax)

        fig.set_facecolor('#181818')

        #############################################################################################################################################

        #Params for the text inside the <> this is a function to highlight text
        highlight_textprops =\
        [{"color": color[0], "fontweight": 'bold'}
                ]

        fig_text(s =f'<{club}>' + ' ' + 'Touch Map',
                x = 0.5, y = 0.91, highlight_textprops = highlight_textprops,
                color='white', fontweight='bold', ha='center', va='center', fontsize=48);
        
        fig_text(s ='MatchDay:' + str(gameID) + ' ' +  '| Season 21-22 | @menesesp20',
                x = 0.5, y = 0.85, color='white', fontweight='bold', ha='center', va='center', fontsize=16, alpha=0.7);

        #############################################################################################################################################

        pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                                ['#181818', '#3d0000', color[0]], N=10)
        bs = pitch.bin_statistic(df.x, df.y, bins=(12, 8))
        heatmap = pitch.heatmap(bs, edgecolors='#181818', ax=ax, cmap=pearl_earring_cmap, zorder=2)

        scatter = pitch.scatter(df[x], df[y], ax=ax, edgecolor='white', facecolor='White', alpha=0.1, zorder=2)

        #############################################################################################################################################

        # Club Logo
        fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.11, bottom=0.828, width=0.2, height=0.1)

        fig_text(s = 'Attacking Direction',
                        x = 0.5, y = 0.17,
                        color='white', fontweight='bold',
                        ha='center', va='center',
                        fontsize=14)

        # ARROW DIRECTION OF PLAY
        ax.annotate('', xy=(0.3, -0.07), xycoords='axes fraction', xytext=(0.7, -0.07), 
                arrowprops=dict(arrowstyle="<-", color='white', lw=2))

#############################################################################################################################################################

def field_Tilt(df, gameID, club):
    
    if gameID == 'All Season':
          touch = df.loc[(df['isTouch'] == True) & (df['x'] >=70)].reset_index(drop=True)
    else:
        touch = df.loc[(df['Match_ID'] == gameID) & (df['isTouch'] == True) & (df['x'] >=70)].reset_index(drop=True)

    #############################################################################################################################################

    league = touch.League.unique()
    league = league[0]

    home = touch.home_Team.unique()
    home = home[0]
    color = clubColors.get(home)

    away = touch.away_Team.unique()
    away = away[0]
    color2 = clubColors.get(away)

    home_Passes = df.loc[(df.typedisplayName == 'Pass') & (df.team == home) & (df.Match_ID == gameID)]['typedisplayName'].count()
    away_Passes = df.loc[(df.typedisplayName == 'Pass') & (df.team == away) & (df.Match_ID == gameID)]['typedisplayName'].count()

    passes_Total = df.loc[(df.typedisplayName == 'Pass') & (df.Match_ID == gameID)]['typedisplayName'].count()


    home_Passes = int(home_Passes)
    home_Passes = round((home_Passes / int(passes_Total)) * 100, 2)
    
    away_Passes = int(away_Passes)
    away_Passes = round((away_Passes / int(passes_Total)) * 100, 2)

    #############################################################################################################################################


    fieldTilt_Home = touch.loc[touch.team == home]

    fieldTilt_Home = round((len(fieldTilt_Home) / len(touch)) * 100, 2)

    fieldTilt_Away = touch.loc[touch.team == away]

    fieldTilt_Away = round((len(fieldTilt_Away) / len(touch)) * 100, 2)

    #############################################################################################################################################

    # Plotting the pitch

    fig, ax = plt.subplots(figsize=(18,14))

    pitch = Pitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                         pitch_color='#181818', line_color='white',
                         line_zorder=1, linewidth=5, spot_scale=0.005)

    pitch.draw(ax=ax)

    fig.set_facecolor('#181818')

    #############################################################################################################################################

    ax.axvspan(70, 100, facecolor=color[0], alpha=0.68)

    ax.axvline(70, c='white', ls='--', lw=4)

    #############################################################################################################################################

    ax.scatter( touch['x'] , touch['y'] , s = 100, color='#181818', alpha=0.8, zorder=2)

    #############################################################################################################################################

    #Params for the text inside the <> this is a function to highlight text
    highlight_textprops =\
        [{"color": color[0],"fontweight": 'bold'},
         {"color": color2[0],"fontweight": 'bold'}
         ]

    fig_text(s =f'<{home}>' + ' ' + 'vs' + ' ' + f'<{away}>' + ' ' + 'Field Tilt',
             x = 0.5, y = 0.93,
             ha='center', va='center',
             highlight_textprops = highlight_textprops, 
             color='white', fontweight='bold',
             fontsize=40);
    
    fig_text(s =  league + ' ' + 'MatchDay:' + ' ' + str(gameID) + ' ' + '| Season 21-22 | @menesesp20',
             x = 0.53, y = 0.89,
             color='white', fontweight='bold',
             ha='center', va='center',
             fontsize=20);

    fig_text(s = str(fieldTilt_Home) + ' ',
             x = 0.474, y = 0.225,
             color=color[0], fontweight='bold',
             ha='center', va='center',
             fontsize=30)

    fig_text(s = ' ' + '   ' + ' ',
             x = 0.512, y = 0.225,
             color=color2[0], fontweight='bold',
             ha='center', va='center',
             fontsize=30)
    
    fig_text(s = ' ' + str(fieldTilt_Away),
             x = 0.55, y = 0.225,
             color=color2[0], fontweight='bold',
             ha='center', va='center',
             fontsize=30)


    if (home_Passes < 50) & (fieldTilt_Home > 50):
        #Params for the text inside the <> this is a function to highlight text
        highlight_textprops =\
            [{"color": color[0],"fontweight": 'bold'},
            {"color": color[0],"fontweight": 'bold'},
            {"color": color2[0],"fontweight": 'bold'}]

        fig_text(s = 'Despite' + ' ' + f'<{home}>' + ' ' + 'had less possession' + ' ' + '(' + f'<{str(home_Passes)}%>' + ')' + '\n' +
                 'they had greater ease in penetrating' + '\n' + 'the final third than' + ' ' +  f'<{away}>',
                 highlight_textprops = highlight_textprops,
                 x = 0.29, y = 0.77,
                 color='white', fontweight='bold',
                 ha='center', va='center',
                 fontsize=16)

    elif (away_Passes < 50) & (fieldTilt_Away > 50):
        #Params for the text inside the <> this is a function to highlight text
        highlight_textprops =\
            [{"color": color2[0],"fontweight": 'bold'},
            {"color": color2[0],"fontweight": 'bold'},
            {"color": color[0],"fontweight": 'bold'}]

        fig_text(s = 'Despite' + ' ' + f'<{away}>' + ' ' + 'had less possession' + ' ' + '(' + f'<{str(away_Passes)}%>' + ')' + '\n' +
                 'they had greater ease in penetrating' + '\n' + 'the final third than' + ' ' +  f'<{home}>',
                 highlight_textprops = highlight_textprops,
                 x = 0.29, y = 0.77,
                 color='white', fontweight='bold',
                 ha='center', va='center',
                 fontsize=16)

    elif (home_Passes > 50) & (fieldTilt_Home < 50):
        #Params for the text inside the <> this is a function to highlight text
        highlight_textprops =\
            [{"color": color[0],"fontweight": 'bold'},
            {"color": color[0],"fontweight": 'bold'},
            {"color": color2[0],"fontweight": 'bold'}]

        fig_text(s = 'Despite' + ' ' + f'<{home}>' + ' ' + 'had more possession' + ' ' + '(' + f'<{str(home_Passes)}%>' + ')' + '\n' +
                 'they struggled to penetrate' + '\n' + 'the last third than' + ' ' +  f'<{away}>',
                 highlight_textprops = highlight_textprops,
                 x = 0.29, y = 0.77,
                 color='white', fontweight='bold',
                 ha='center', va='center',
                 fontsize=16)

    elif (away_Passes > 50) & (fieldTilt_Away < 50):
        #Params for the text inside the <> this is a function to highlight text
        highlight_textprops =\
            [{"color": color2[0],"fontweight": 'bold'},
            {"color": color2[0],"fontweight": 'bold'},
            {"color": color[0],"fontweight": 'bold'}]

        fig_text(s = 'Despite' + ' ' + f'<{away}>' + ' ' + 'had more possession' + ' ' + '(' + f'<{str(away_Passes)}%>' + ')' + '\n' +
                 'they struggled to penetrate' + '\n' + 'the last third than' + ' ' +  f'<{home}>',
                 highlight_textprops = highlight_textprops,
                 x = 0.29, y = 0.77,
                 color='white', fontweight='bold',
                 ha='center', va='center',
                 fontsize=16)

    elif (fieldTilt_Home > fieldTilt_Away):
        fig_text(s = f'<{home}>' + ' ' + 'dominated the game with greater dominance' + '\n' + 'of the last third than their opponent' + ' ' + 
                    f'<{away}>.',
                    highlight_textprops = highlight_textprops,
                    x = 0.33, y = 0.77,
                    color='white', fontweight='bold',
                    ha='center', va='center',
                    fontsize=14)

    elif (fieldTilt_Home < fieldTilt_Away):
        highlight_textprops =\
        [{"color": color2[0],"fontweight": 'bold'},
        {"color": color[0],"fontweight": 'bold'}]
        
        fig_text(s = f'<{away}>' + ' ' + 'dominated the game with greater dominance' + '\n' + 'of the last third than their opponent' + ' ' + 
                 f'<{home}>.',
                 highlight_textprops = highlight_textprops,
                 x = 0.33, y = 0.77,
                 color='white', fontweight='bold',
                 ha='center', va='center',
                 fontsize=14)

    #############################################################################################################################################
    
    # Club Logo
    fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.08, bottom=0.858, width=0.2, height=0.1)

    fig_text(s = 'Attacking Direction',
                 x = 0.5, y = 0.17,
                 color='white', fontweight='bold',
                 ha='center', va='center',
                 fontsize=14)

    # ARROW DIRECTION OF PLAY
    ax.annotate('', xy=(0.3, -0.07), xycoords='axes fraction', xytext=(0.7, -0.07), 
            arrowprops=dict(arrowstyle="<-", color='white', lw=2))
#############################################################################################################################################################


#Automatização do processo de criação do gráfico de campo de futebol com os passes realizados
def draw_keyPasses_Dashboard(df, col_qualifier, qualifier_event, col_event, event_name, col_player, col_sub_event, suc, player_name, club):
 
  color = clubColors.get(club)

  df['beginning'] = np.sqrt(np.square(100 - df['x']) + np.square(100 - df['y']))
  df['end'] = np.sqrt(np.square(100 - df['endX']) + np.square(100 - df['endY']))

  df['progressive'] = [(df['end'][x]) / (df['beginning'][x]) < .75 for x in range(len(df.beginning))]

  player = df[df[col_player] == player_name]

  keyPass = player[(player[col_qualifier].str.contains(qualifier_event) == True) & (player[col_event] == event_name)]

  Pass = player[(player[col_event] == event_name)]

  sucess = player[(player[col_event] == event_name) & (player[col_sub_event] == suc)]

  Progressive = Pass[Pass['progressive']==True]

  Progressive = Progressive.loc[(Progressive.x > 99) | (Progressive.x > 1) & (Progressive.y > 55) & (Progressive.y < 99)]

  Pass_percentage = round((len(sucess) / len(Pass)) * 100, 2)

  #--------------------------------------------------------------------------------------------------------------------------------------------------------------

  #Atribuição do tamanho do gráfico através do ax
  fig, ax = plt.subplots(figsize=(18,14))
  fig.set_facecolor('#181818')
  #Criação do campo de futebol
  pitch = VerticalPitch(pitch_type='opta', pitch_color='#181818', line_color='white')
  #Visualizar o gráfico do campo de futebol
  pitch.draw(ax=ax)

  #Criação das setas que simbolizam os passes realizados bem sucedidos
  pitch.arrows(sucess.x, sucess.y, sucess.endX, sucess.endY, color='#5d5e60', ax=ax,
              width=2, headwidth=5, headlength=5, label='Passes' + ':' + ' ' + f'{len(Pass)}' + ' ' + '(' + f'{Pass_percentage}' + '%' + ' ' + 'Completion rate' + ')' )
  
  #Criação das setas que simbolizam os passes realizados falhados
  pitch.arrows(keyPass.x, keyPass.y, keyPass.endX, keyPass.endY, color='#c70216', ax=ax,
              width=2, headwidth=5, headlength=5, label='Key passes' + ':' + ' ' + f'{len(keyPass)}')
  
  #Criação das setas que simbolizam os passes realizados falhados
  pitch.arrows(Progressive.x, Progressive.y, Progressive.endX, Progressive.endY, color='#00659c', ax=ax,
              width=2, headwidth=5, headlength=5, label='Progressive passes' + ':' + ' ' + f'{len(Progressive)}')

  #--------------------------------------------------------------------------------------------------------------------------------------------------------------

  #Criação da legenda
  l = ax.legend(bbox_to_anchor=(0, 0), loc='upper left', facecolor='white', framealpha=0, labelspacing=.7)
  #Ciclo FOR para atribuir a white color na legend
  for text in l.get_texts():
      text.set_color("white")


#############################################################################################################################################################

def cluster_Event(df, teamName, event_name, matchDay, n_clusters, qualifier=False):

  cols_Cluster = ['team', 'Match_ID', 'typedisplayName', 'qualifiers', 'x', 'y', 'endX', 'endY']

  cols_coords = ['x', 'y', 'endX', 'endY']

  df_cluster = df[cols_Cluster]

  if (qualifier != False) & (matchDay != 'All Season'):
    df_cluster = df_cluster.loc[(df_cluster['team'] == teamName) & (df_cluster['Match_ID'] == matchDay) & (df_cluster['qualifiers'].str.contains(event_name) == True)].reset_index()
  
  elif (qualifier != False) & (matchDay == 'All Season'):
    df_cluster = df_cluster.loc[(df_cluster['team'] == teamName) & (df_cluster['qualifiers'].str.contains(event_name) == True)].reset_index()
  
  elif (qualifier == False) & (matchDay != 'All Season'):
    df_cluster = df_cluster.loc[(df_cluster['team'] == teamName) & (df_cluster['Match_ID'] == matchDay) & (df_cluster['typedisplayName'] == event_name)].reset_index()
  
  elif (qualifier == False) & (matchDay == 'All Season'):
    df_cluster = df_cluster.loc[(df_cluster['team'] == teamName) & (df_cluster['typedisplayName'] == event_name)].reset_index()

  df_cluster.drop(['index'], axis=1, inplace=True)

  X = np.array(df_cluster[cols_coords])
  kmeans = KMeans(n_clusters = n_clusters, random_state=100)
  kmeans.fit(X)
  df_cluster['cluster'] = kmeans.predict(X)

  return df_cluster

#############################################################################################################################################################

def GoalKick(df, league, club, n_cluster, matchDay):

        #################################################################################################################################################
        
        goalKick = cluster_Event(df, club, 'GoalKick', matchDay, n_cluster, True)

        #################################################################################################################################################

        # Plotting the pitch

        fig, ax = plt.subplots(figsize=(18,14))

        pitch = Pitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                        pitch_color='#181818', line_color='white',
                        line_zorder=1, linewidth=5, spot_scale=0.00)

        pitch.draw(ax=ax)

        fig.set_facecolor('#181818')

        #################################################################################################################################################

        # Title of our plot

        fig.suptitle('How do they come out playing?', fontsize=50, color='white',
                     fontweight = "bold", x=0.53, y=0.95)

        fig_text(s = "GoalKick | Season 21-22 | Made by: @Menesesp20",
                x = 0.5, y = 0.9,
                color='white', fontweight='bold', ha='center' ,fontsize=16);

        #################################################################################################################################################

        # Key Passes Cluster
        for x in range(len(goalKick['cluster'])):
            
                # First
                if goalKick['cluster'][x] == 3:
                        pitch.arrows(xstart=goalKick['x'][x], ystart=goalKick['y'][x],
                                    xend=goalKick['endX'][x], yend=goalKick['endY'][x],
                                    color='#ea04dc', alpha=0.8,
                                    lw=3, zorder=2,
                                    ax=ax)
                        
                # Second
                if goalKick['cluster'][x] == 2:
                        pitch.arrows(xstart=goalKick['x'][x], ystart=goalKick['y'][x],
                                    xend=goalKick['endX'][x], yend=goalKick['endY'][x],
                                    color='#2d92df', alpha=0.8,
                                    lw=3, zorder=2,
                                    ax=ax)
                
                # Third
                if goalKick['cluster'][x] == 1:
                        pitch.arrows(xstart=goalKick['x'][x], ystart=goalKick['y'][x],
                                    xend=goalKick['endX'][x], yend=goalKick['endY'][x],
                                    color='#fb8c04', alpha=0.8,
                                    lw=3, zorder=2,
                                    ax=ax)

        #################################################################################################################################################

        fig_text(s = 'Most frequent zone',
                 x = 0.8, y = 0.79,
                 color='#ea04dc', fontweight='bold', ha='center' ,fontsize=12);

        fig_text(s = 'Second most frequent zone',
                 x = 0.8, y = 0.76,
                 color='#2d92df', fontweight='bold', ha='center' ,fontsize=12);

        fig_text(s = 'Third most frequent zone',
                 x = 0.8, y = 0.73,
                 color='#fb8c04', fontweight='bold', ha='center' ,fontsize=12);

        # Club Logo
        fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.1, bottom=0.865, width=0.2, height=0.1)

        fig_text(s = 'Attacking Direction',
                        x = 0.5, y = 0.17,
                        color='white', fontweight='bold',
                        ha='center', va='center',
                        fontsize=14)

        # ARROW DIRECTION OF PLAY
        ax.annotate('', xy=(0.3, -0.07), xycoords='axes fraction', xytext=(0.7, -0.07), 
                arrowprops=dict(arrowstyle="<-", color='white', lw=2))

#############################################################################################################################################################

def xT(df):
  eventsPlayers_xT = df

  #Import xT Grid, turn it into an array, and then get how many rows and columns it has
  @st.cache
  def load_model():
          xT = pd.read_csv('xT/xT_Grid.csv', header=None)
          return xT
  
  xT = load_model()
  xT = np.array(xT)
  xT_rows, xT_cols = xT.shape

  eventsPlayers_xT['x1_bin'] = pd.cut(eventsPlayers_xT['x'], bins=xT_cols, labels=False)
  eventsPlayers_xT['y1_bin'] = pd.cut(eventsPlayers_xT['y'], bins=xT_rows, labels=False)
  eventsPlayers_xT['x2_bin'] = pd.cut(eventsPlayers_xT['endX'], bins=xT_cols, labels=False)
  eventsPlayers_xT['y2_bin'] = pd.cut(eventsPlayers_xT['endY'], bins=xT_rows, labels=False)

  eventsPlayers_xT = eventsPlayers_xT[['name', 'team', 'home_Team', 'away_Team', 'Match_ID', 'minute', 'second', 'teamId', 'x', 'y', 'typedisplayName', 'qualifiers', 'endX', 'endY', 'x1_bin', 'y1_bin', 'x2_bin', 'y2_bin']]

  eventsPlayers_xT['start_zone_value'] = eventsPlayers_xT[['x1_bin', 'y1_bin']].apply(lambda x: xT[x[1]][x[0]], axis=1)
  eventsPlayers_xT['end_zone_value'] = eventsPlayers_xT[['x2_bin', 'y2_bin']].apply(lambda x: xT[x[1]][x[0]], axis=1)

  eventsPlayers_xT['xT'] = round(eventsPlayers_xT['end_zone_value'] - eventsPlayers_xT['start_zone_value'], 2)

  eventsPlayers_xT.drop(eventsPlayers_xT.index[0], axis=0, inplace=True)

  eventsPlayers_xT.drop_duplicates(inplace=True)

  eventsPlayers_xT.reset_index(inplace=True)

  eventsPlayers_xT.drop(['index'], axis=1, inplace=True)

  xT_Total = round(eventsPlayers_xT['xT'].sum(), 2)

  xT_Total

  return eventsPlayers_xT

#############################################################################################################################################################


def mainStats(df):
    Goals = []

    FieldTilt = []

    DeepCompletions = []

    op_BoxPasses = []

    Zone14_Touches = []

    HalfSpacesLeft_Touches = []

    HalfSpacesRight_Touches = []

    xT_Count = []

    Passes_Completion = []

    Progressive_Passes = []

    BuildUp = []

    ##############################################################################################################################################################

    #Criação da lista de equipas
    Teams = df['team'].unique()

    Teams = Teams.tolist()

    ##############################################################################################################################################################

    xTDF = xT(df)

    ##############################################################################################################################################################

    sucess = df[(df['typedisplayName'] == 'Pass') & (df['outcomeTypedisplayName'] == 'Successful') & (df['x'] != 99.5)]

    insucess = df[(df['typedisplayName'] == 'Pass') & (df['outcomeTypedisplayName'] == 'Unsuccessful') & (df['x'] != 99.5)]

    Passes = pd.concat([sucess, insucess], axis=0, ignore_index=True)[['name', 'team', 'x', 'y', 'endX', 'endY', 'outcomeTypedisplayName', 'Match_ID']]

    radius = 20

    Passes['initialDistancefromgoal'] = np.sqrt(((100 - Passes['x'])**2) + ((50 - Passes['y'])**2))

    Passes['finalDistancefromgoal'] = np.sqrt(((100 - Passes['endX'])**2) + ((50 - Passes['endY'])**2))

    Passes['deepCompletion'] = np.where(((Passes['finalDistancefromgoal'] <= radius) & (Passes['initialDistancefromgoal'] >= radius)), 'True', 'False')

    deepcompletion =  Passes.loc[(((Passes['deepCompletion']=='True') & (Passes['outcomeTypedisplayName']!='Unsuccessful')))]

    ##############################################################################################################################################################

    df['beginning'] = np.sqrt(np.square(100 - df['x']) + np.square(100 - df['y']))
    df['end'] = np.sqrt(np.square(100 - df['endX']) + np.square(100 - df['endY']))

    df['progressive'] = [(df['end'][x]) / (df['beginning'][x]) < .75 for x in range(len(df.beginning))]

    progressive = df.loc[df['progressive'] == True]

    ##############################################################################################################################################################

    zone14 = df[(df.endX <= 83) &
                        (df.endX >= 75) &
                        (df.endY <= 66) &
                        (df.endY >= 35) &
                        (df.typedisplayName == 'Pass')]


    halfspaceleft = df[(df.endY <= 83) &
                                (df.endY >= 65) &
                                (df.endX >= 78) &
                                (df.typedisplayName == 'Pass')]

    halfspaceright = df[(df.endY >= 17) &
                                (df.endY <= 33) &
                                (df.endX >= 78) &
                                (df.typedisplayName == 'Pass')]

    ##############################################################################################################################################################

    #Criação dos dataFrames para cada evento
    xT_Sum = xTDF

    DeepCompletions_Sum = deepcompletion

    Progressive_Passes_Sum = progressive

    zone14_Sum = zone14

    halfSpaceLeft_Sum = halfspaceleft

    halfSpaceRight_Sum = halfspaceright

    fieldTilt_Sum = eventsPlayers.loc[(eventsPlayers.isTouch == True) & (eventsPlayers.x >=70)]

    BuildUp_Sum = eventsPlayers.loc[(eventsPlayers.typedisplayName == 'Pass') & (eventsPlayers.x < 50)]

    op_box_Sum = eventsPlayers.loc[(eventsPlayers['endX'] >= 83) & (eventsPlayers['endY'] >= 21.1) & (eventsPlayers['endY'] <= 78.9)]

    goals_Sum = eventsPlayers.loc[(eventsPlayers.typedisplayName == 'Goal')]

    passes_Sum = eventsPlayers.loc[(eventsPlayers.typedisplayName == 'Pass')]


    #Ciclo For de atribuição dos valores a cada jogador
    for team in Teams:
        xT_Count.append(xT_Sum.loc[xT_Sum['team'] == team, 'xT'].sum())
        Goals.append(goals_Sum.loc[goals_Sum['team'] == team, 'typedisplayName'].count())
        Passes_Completion.append(passes_Sum.loc[passes_Sum['team'] == team, 'typedisplayName'].count())
        BuildUp.append(BuildUp_Sum.loc[BuildUp_Sum['team'] == team, 'typedisplayName'].count())
        FieldTilt.append(fieldTilt_Sum.loc[(fieldTilt_Sum['team'] == team), 'isTouch'].count())
        Progressive_Passes.append(Progressive_Passes_Sum.loc[(Progressive_Passes_Sum['team'] == team), 'progressive'].count())
        op_BoxPasses.append(op_box_Sum.loc[(op_box_Sum['team'] == team), 'typedisplayName'].count())
        DeepCompletions.append(DeepCompletions_Sum.loc[(DeepCompletions_Sum['team'] == team), 'deepCompletion'].count())
        Zone14_Touches.append(zone14_Sum.loc[(zone14_Sum['team'] == team), 'typedisplayName'].count())
        HalfSpacesLeft_Touches.append(halfSpaceLeft_Sum.loc[(halfSpaceLeft_Sum['team'] == team), 'typedisplayName'].count())
        HalfSpacesRight_Touches.append(halfSpaceRight_Sum.loc[(halfSpaceRight_Sum['team'] == team), 'typedisplayName'].count())

    data = {
        'Team' : Teams,
        'Goals' : Goals,
        'Passes Completion' : Passes_Completion,
        'Progressive Passes' : Progressive_Passes,
        'BuildUp' : BuildUp,
        'Field Tilt' : FieldTilt,
        'Op.Box Passes' : op_BoxPasses,
        'Zone14 Touches' : Zone14_Touches,
        'Half Spaces Left' : HalfSpacesLeft_Touches,
        'Half Spaces Right' : HalfSpacesRight_Touches,
        'Deep Completions' : DeepCompletions,
        'xT' : xT_Count
    }


    data = pd.DataFrame(data)

    return data

#############################################################################################################################################################

def mainTable(df, league):
    # first, we'll create a new figure and axis object

    df = mainStats(df).sort_values('Team', ascending=False)

    fig, ax = plt.subplots(figsize=(15,10))

    fig.set_facecolor('#181818')

    rows = 19
    cols = 22

    #Criação da lista de jogadores
    Teams = df['Team'].tolist()

    # Goals
    Goals = df['Goals'].tolist()

    # % PASSES
    Passes_Completion = df['Passes Completion'].tolist()

    # PROGRESSIVE PASSES
    Progressive_Passes = df['Progressive Passes'].tolist()

    # BUILD UP PASSES
    BuildUp = df['BuildUp'].tolist()

    # Op.Box Passes

    Box_Passes = df['Op.Box Passes'].tolist()

    # Zone14_Touches

    Zone14_Touches = df['Zone14 Touches'].tolist()

    # Half_Spaces_Left

    Half_Spaces_Left = df['Half Spaces Left'].tolist()

    # Half_Spaces_Right

    Half_Spaces_Right = df['Half Spaces Right'].tolist()

    # Deep_Completions

    Deep_Completions = df['Deep Completions'].tolist()

    # xT

    df['xT'] = round(df['xT'], 2)
    xt = df['xT'].tolist()

    data = {
        'Teams' : Teams,
        'Goals' : Goals,
        'Passes Completion' : Passes_Completion,
        'Progressive Passes' : Progressive_Passes,
        'BuildUp' : BuildUp,
        'Op.Box Passes': Box_Passes,
        'Zone14 Touches' : Zone14_Touches,
        'Half Spaces Left' : Half_Spaces_Left,
        'Half Spaces Right' : Half_Spaces_Right,
        'Deep Completions' : Deep_Completions,
        'xT' : xt
    }

    data = pd.DataFrame(data)

    data = data.to_dict('index')


    for i in range(len(data)):
        d = data[i]

        ax.text(x=.1, y=i, s=d['Teams'], va='center', ha='left', weight='bold', size=20, color='white')
        # shots column - this is my "main" column, hence bold text

        ax.text(x=6.5, y=i, s=d['Goals'], va='center', ha='right', size=20, color='white')

        ax.text(x=9.9, y=i, s=d['Passes Completion'], va='center', ha='right', size=20, color='white')

        ax.text(x=14.5, y=i, s=d['Progressive Passes'], va='center', ha='right', size=20, color='white')

        ax.text(x=19.9, y=i, s=d['BuildUp'], va='center', ha='right', size=20, color='white')

        ax.text(x=23.7, y=i, s=d['Op.Box Passes'], va='center', ha='right', size=20, color='white')

        ax.text(x=28.5, y=i, s=d['Zone14 Touches'], va='center', ha='right', size=20, color='white')

        ax.text(x=35, y=i, s=d['Half Spaces Left'], va='center', ha='right', size=20, color='white')

        ax.text(x=40.5, y=i, s=d['Half Spaces Right'], va='center', ha='right', size=20, color='white')

        ax.text(x=46.2, y=i, s=d['Deep Completions'], va='center', ha='right', size=20, color='white')

        ax.text(x=50, y=i, s=d['xT'], va='center', ha='right', size=20, color='white')


    ax.text(1.2, 20.3, 'Teams', weight='bold', ha='left', size=21, color='#ff0000')

    ax.text(5.3, 20.3, 'Goals', weight='bold', ha='left', size=21, color='#ff0000')

    ax.text(8, 20.3, '% Passes', weight='bold', ha='left', size=21, color='#ff0000')

    ax.text(11.3, 20.3, 'Progressive Passes', weight='bold', ha='left', size=21, color='#ff0000')

    ax.text(18, 20.3, 'BuildUp', weight='bold', ha='left', size=21, color='#ff0000')

    ax.text(21, 20.3, 'Op.Box Passes', weight='bold', ha='left', size=21, color='#ff0000')

    ax.text(26, 20.3, 'Zone 14 Touches', weight='bold', ha='left', size=21, color='#ff0000')

    ax.text(32, 20.3, 'Half Spaces. L', weight='bold', ha='left', size=21, color='#ff0000')

    ax.text(37.8, 20.3, 'Half Spaces. R', weight='bold', ha='left', size=21, color='#ff0000')

    ax.text(43, 20.3, 'Deep Completions', weight='bold', ha='left', size=21, color='#ff0000')

    ax.text(49.3, 20.3, 'xT', weight='bold', ha='left', size=21, color='#ff0000')

    for row in range(rows):
        ax.plot(
            [0, cols + 2],
            [row -.5, row - .5],
            ls=':',
            lw='.5',
            c='#181818'
        )

    for i in range(len(data)):
        d = data[i]

        add_image(image='Images/Clubs/' + league + '/' + 'Athletic Club' + '.png', fig=fig, left=0.075, bottom=0.88, width=0.1, height=0.04)

        add_image(image='Images/Clubs/' + league + '/' + 'Atlético Madrid' + '.png', fig=fig, left=0.075, bottom=0.838, width=0.1, height=0.04)

        add_image(image='Images/Clubs/' + league + '/' + 'Cadiz' + '.png', fig=fig, left=0.075, bottom=0.798, width=0.1, height=0.04)

        add_image(image='Images/Clubs/' + league + '/' + 'Celta Vigo' + '.png', fig=fig, left=0.075, bottom=0.76, width=0.1, height=0.04)

        add_image(image='Images/Clubs/' + league + '/' + 'Deportivo Alavés' + '.png', fig=fig, left=0.075, bottom=0.728, width=0.1, height=0.0303)

        add_image(image='Images/Clubs/' + league + '/' + 'Elche' + '.png', fig=fig, left=0.075, bottom=0.688, width=0.1, height=0.032)

        add_image(image='Images/Clubs/' + league + '/' + 'Espanyol' + '.png', fig=fig, left=0.075, bottom=0.652, width=0.1, height=0.035)

        add_image(image='Images/Clubs/' + league + '/' + 'FC Barcelona' + '.png', fig=fig, left=0.075, bottom=0.614, width=0.1, height=0.033)

        add_image(image='Images/Clubs/' + league + '/' + 'Getafe' + '.png', fig=fig, left=0.075, bottom=0.574, width=0.1, height=0.033)

        add_image(image='Images/Clubs/' + league + '/' + 'Granada' + '.png', fig=fig, left=0.075, bottom=0.532, width=0.1, height=0.033)

        add_image(image='Images/Clubs/' + league + '/' + 'Levante' + '.png', fig=fig, left=0.075, bottom=0.497, width=0.1, height=0.033)

        add_image(image='Images/Clubs/' + league + '/' + 'Mallorca' + '.png', fig=fig, left=0.075, bottom=0.464, width=0.1, height=0.035)

        add_image(image='Images/Clubs/' + league + '/' + 'Osasuna' + '.png', fig=fig, left=0.075, bottom=0.425, width=0.1, height=0.035)

        add_image(image='Images/Clubs/' + league + '/' + 'Rayo Vallecano' + '.png', fig=fig, left=0.075, bottom=0.388, width=0.1, height=0.035)

        add_image(image='Images/Clubs/' + league + '/' + 'Real Betis' + '.png', fig=fig, left=0.075, bottom=0.353, width=0.1, height=0.035)

        add_image(image='Images/Clubs/' + league + '/' + 'Real Madrid' + '.png', fig=fig, left=0.075, bottom=0.315, width=0.1, height=0.035)

        add_image(image='Images/Clubs/' + league + '/' + 'Real Sociedad' + '.png', fig=fig, left=0.075, bottom=0.273, width=0.1, height=0.035)

        add_image(image='Images/Clubs/' + league + '/' + 'Sevilla' + '.png', fig=fig, left=0.075, bottom=0.235, width=0.1, height=0.035)

        add_image(image='Images/Clubs/' + league + '/' + 'Valencia' + '.png', fig=fig, left=0.075, bottom=0.20, width=0.1, height=0.035)

        add_image(image='Images/Clubs/' + league + '/' + 'Villarreal CF' + '.png', fig=fig, left=0.075, bottom=0.16, width=0.1, height=0.035)
    

    add_image(image='Images/Leagues/' + league + '.png', fig=fig, left=0.08, bottom=0.93, width=0.1, height=0.08)

    ax.axis('off')

#############################################################################################################################################################
        
def heatMap_xT(df, league, club, matchDay, player=None):

        color = clubColors.get(club)

        xTDF = xT(df)

        if (player == None) & (matchDay == 'All Season'):
                xTheatMap = xTDF.loc[(xTDF.team == club)]

        elif (player == None) & (matchDay != 'All Season'):
                xTheatMap = xTDF.loc[(xTDF.team == club) & (xTDF.Match_ID == matchDay)]

        elif (player != None) & (matchDay != 'All Season'):
                xTheatMap = xTDF.loc[(xTDF.name == player) & (xTDF.Match_ID == matchDay)]

        elif (player != None) & (matchDay == 'All Season'):
                xTheatMap = xTDF.loc[(xTDF.name == player)]

        # setup pitch
        pitch = Pitch(pitch_type='opta', line_zorder=2,
                        pitch_color='#181818', line_color='#efefef')

        fig, ax = pitch.draw(figsize=(12, 8))
        fig.set_facecolor('#181818')

        pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                                ['#181818', color[0]], N=10)

        xTheatHeat = xTheatMap.loc[xTheatMap.xT > 0]
        bs = pitch.bin_statistic(xTheatHeat.x, xTheatHeat.y, bins=(15, 10))
        pitch.heatmap(bs, edgecolors='#181818', ax=ax, cmap=pearl_earring_cmap)

        # Club Logo
        fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0, bottom=0.98, width=0.2, height=0.15)

        # TITLE
        if player == None:
                fig_text(s = 'Where' + ' ' + club + ' ' + 'generate the most xT',
                        x = 0.54, y = 1.1, color='white', fontweight='bold', ha='center' ,fontsize=29.5);
        else:
                fig_text(s = 'Where' + ' ' + player + ' ' + 'generate the most xT',
                        x = 0.54, y = 1.1, color='white', fontweight='bold', ha='center' ,fontsize=27);             
        # TOTAL xT
        fig_text(s = str(round(sum(xTheatMap.xT), 2)) + ' ' + 'xT Generated', 
                x = 0.51, y = 1.02, color='white', fontweight='bold', ha='center' ,fontsize=18);

        fig_text(s = 'Attacking Direction',
                        x = 0.5, y = 0.05,
                        color='white', fontweight='bold',
                        ha='center', va='center',
                        fontsize=14)

        # ARROW DIRECTION OF PLAY
        ax.annotate('', xy=(0.3, -0.03), xycoords='axes fraction', xytext=(0.7, -0.03), 
                arrowprops=dict(arrowstyle="<-", color='white', lw=2))

#############################################################################################################################################################


def pitchZonesActions(df, colEvent, eventName, league, club, playerName=None):

        color = clubColors.get(club)

        if playerName != None:
                player = df.loc[(eventsPlayers[colEvent] == eventName) &( df.name == playerName)]
        else:
                player = df.loc[eventsPlayers[colEvent] == eventName]

        pitch = VerticalPitch(pitch_type='opta', line_zorder=2,
                                pitch_color='#181818', line_color='#efefef')

        fig, ax = pitch.draw(figsize=(15, 10))
        fig.set_facecolor('#181818')

        pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                                ['#181818', color[0]], N=9)

        scatter = pitch.scatter(player.x, player.y, ax=ax, edgecolor='white', facecolor='black', alpha=0.5, zorder=2)

        bs = pitch.bin_statistic(player.x, player.y, bins=(3, 3))
        heatmap = pitch.heatmap(bs, edgecolors='#181818', ax=ax, cmap=pearl_earring_cmap)

        ######################################################################################################################

        # RIGHT UP

        zone7 = player.loc[(player.x >= 65) & (player.y <= 35)]

        # CENTER UP

        zone8 = player.loc[(player.x >= 65) & (player.y >= 35) & (player.y <= 65)]

        # LEFT UP

        zone9 = player.loc[(player.x >= 65) & (player.y >= 65)]


        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone7) / len(player)) * 100, 2)) + '%',
                 x = 0.63, y = 0.80, color='white', fontweight='bold', ha='center' ,fontsize=25);

        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone8) / len(player)) * 100, 2)) + '%',
                 x = 0.5, y = 0.80, color='white', fontweight='bold', ha='center' ,fontsize=25);

        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone9) / len(player)) * 100, 2)) + '%',
                 x = 0.38, y = 0.80, color='white', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################

        # RIGHT MIDDLE

        zone4 = player.loc[(player.x >= 35) & (player.x <= 65) & (player.y <= 35)]

        # CENTER MIDDLE

        zone5 = player.loc[(player.x >= 35) & (player.x <= 65) & (player.y >= 35) & (player.y <= 65)]

        # LEFT MIDDLE

        zone6 = player.loc[(player.x >= 35) & (player.x <= 65) & (player.y >= 65)]


        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone4) / len(player)) * 100, 2)) + '%',
                 x = 0.63, y = 0.515, color='white', fontweight='bold', ha='center' ,fontsize=25);

        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone5) / len(player)) * 100, 2)) + '%',
                 x = 0.5, y = 0.515, color='white', fontweight='bold', ha='center' ,fontsize=25);

        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone6) / len(player)) * 100, 2)) + '%',
                 x = 0.38, y = 0.515, color='white', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################

        # RIGHT DOWM

        zone1 = player.loc[(player.x <= 35) & (player.y <= 35)]

        # CENTER DOWN

        zone2 = player.loc[(player.x <= 35) & (player.y >= 35) & (player.y <= 65)]

        # LEFT DOWM

        zone3 = player.loc[(player.x <= 35) & (player.y >= 65)]

        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone1) / len(player)) * 100, 2)) + '%',
                 x = 0.63, y = 0.23, color='white', fontweight='bold', ha='center' ,fontsize=25);

        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone2) / len(player)) * 100, 2)) + '%',
                 x = 0.5, y = 0.23, color='white', fontweight='bold', ha='center' ,fontsize=25);

        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone3) / len(player)) * 100, 2)) + '%',
                 x = 0.38, y = 0.23, color='white', fontweight='bold', ha='center' ,fontsize=25);

        # Club Logo
        fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.23, bottom=0.975, width=0.2, height=0.1)

        # TITLE
        fig_text(s =  playerName,
                x = 0.5, y = 1.06, color='white', fontweight='bold',
                ha='center', va='center',
                fontsize=40);

        # TITLE
        fig_text(s =  'Recovery ball percentage per zone',
                 x = 0.5, y = 1, color='white', fontweight='bold', ha='center', va='center', fontsize=12);


#############################################################################################################################################################

def sides(xTDF, club, matchDay):

    if matchDay == 'All Season':
        xTDF = xTDF.loc[(xTDF.team == club)]
    elif matchDay != 'All Season':
        xTDF = xTDF.loc[(xTDF.team == club) & (xTDF.Match_ID == matchDay)]

    left_xT = xTDF[(xTDF['y'] >= 67) & (xTDF['x'] >= 55)]
    left_xT['side'] = 'Left'

    center_xT = xTDF[(xTDF['y'] < 67) & (xTDF['y'] > 33) & (xTDF['x'] >= 55)]
    center_xT['side'] = 'Center'

    right_xT = xTDF[(xTDF['y'] <= 33) & (xTDF['x'] >= 55)]
    right_xT['side'] = 'Right'

    sides = pd.concat([left_xT, center_xT, right_xT], axis=0)

    return sides


#############################################################################################################################################################

def dataFrame_xTFlow(df):

    leftfinal3rd = []
    centerfinal3rd = []
    rightfinal3rd = []

    leftfinal3rd.append(df.loc[(df['side'] == 'Left'), 'xT'].sum())
    centerfinal3rd.append(df.loc[(df['side'] == 'Center'), 'xT'].sum())
    rightfinal3rd.append(df.loc[(df['side'] == 'Right'), 'xT'].sum())

    data = {
        'left_xT' : leftfinal3rd,
        'center_xT' : centerfinal3rd,
        'right_xT' : rightfinal3rd
    }
    
    df = pd.DataFrame(data)
    
    return df


#############################################################################################################################################################

def finalThird(df, league, club, matchDay, n_cluster):

        if matchDay != 'All Season':
                # DATAFRAME WITH ALL PASSES IN THE FINAL THIRD
                final3rd = df.loc[(df['typedisplayName'] == 'Pass') & (df['team'] == club) &
                              (df['x'] >= 55) & (df['Match_ID'] == matchDay)][['name', 'x', 'y', 'endY', 'endX', 'typedisplayName', 'teamId', 'outcomeTypedisplayName', 'qualifiers']]

        elif matchDay == 'All Season':
                # DATAFRAME WITH ALL PASSES IN THE FINAL THIRD
                final3rd = df.loc[(df['typedisplayName'] == 'Pass') & (df['team'] == club) &
                              (df['x'] >= 55)][['name', 'x', 'y', 'endY', 'endX', 'typedisplayName', 'teamId', 'outcomeTypedisplayName', 'qualifiers']]

        # DATAFRAME WITH ALL PASSES IN THE LEFT FINAL THIRD
        #67 LEFT, RIGHT 33, MID BEETWEN THEM
        leftfinal3rd = final3rd[(final3rd['y'] >= 67)]

        # PERCENTAGE OF ATTACKS IN THE LEFT SIDE
        leftfinal3rdTotal = round((len(leftfinal3rd) / len(final3rd)) * 100 ,1)

        leftfinal3rdTotal

        # DATAFRAME WITH ALL PASSES IN THE CENTER FINAL THIRD
        centerfinal3rd = final3rd[(final3rd['y'] < 67) & (final3rd['y'] > 33)]

        # PERCENTAGE OF ATTACKS IN THE CENTER SIDE
        centerfinal3rdTotal = round((len(centerfinal3rd) / len(final3rd)) * 100 ,1)

        centerfinal3rdTotal

        # DATAFRAME WITH ALL PASSES IN THE RIGHT FINAL THIRD
        rightfinal3rd = final3rd[(final3rd['y'] <= 33)]

        # PERCENTAGE OF ATTACKS IN THE RIGHT SIDE
        rightfinal3rdTotal = round((len(rightfinal3rd) / len(final3rd)) * 100 ,1)

        rightfinal3rdTotal

        #################################################################################################################################################

        final3rd_Cluster = cluster_Event(df, club, 'KeyPass', matchDay, n_cluster, True)

        #################################################################################################################################################

        xTDF = xT(df)

        DFSides = sides(xTDF, club, matchDay)

        xT_Sides = dataFrame_xTFlow(DFSides)

        #################################################################################################################################################

        # Plotting the pitch

        fig, ax = plt.subplots(figsize=(18,14))

        pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                        pitch_color='white', line_color='#181818', half = True,
                        line_zorder=2, linewidth=5,
                        spot_scale=0.0005)

        pitch.draw(ax=ax)

        fig.set_facecolor('white')

        #################################################################################################################################################

        if matchDay != 'All Season':
                Title = df.loc[df['Match_ID'] == matchDay]

                home = Title.loc[(Title.team == club)]
                away = Title.loc[(Title.team != club)]
                
                home = home.team.unique()
                homeName = home[0]
                color = clubColors.get(homeName)

                away = away.team.unique()
                awayName = away[0]
                color2 = clubColors.get(awayName)

        #################################################################################################################################################

        if matchDay != 'All Season':
                #Params for the text inside the <> this is a function to highlight text
                highlight_textprops =\
                        [{"color": color[0],"fontweight": 'bold'},
                        {"color": color2[0],"fontweight": 'bold'}
                        ]

                fig_text(s =f'<{homeName}>' + ' ' + 'vs' + ' ' + f'<{awayName}>',
                         x = 0.53, y = 0.98, ha='center', va='center',
                         highlight_textprops = highlight_textprops ,
                         color='#181818', fontweight='bold',
                         fontsize=50);
                
                fig_text(s =  league + ' ' + '|' + ' ' + 'MatchDay:' + ' ' + str(matchDay) + ' ' + '| Season 21-22 | @menesesp20',
                         x = 0.51, y = 0.94,
                         color='#181818', fontweight='bold',
                         ha='center', va='center',
                         fontsize=18);

        #################################################################################################################################################

        elif matchDay == 'All Season':
                # Title of our plot
                fig.suptitle(club + ' ' + 'Open Play',
                             fontsize=50, color='#181818',
                             fontweight = "bold",
                             x=0.525, y=1)

                fig_text(s = "Key Passes | Season 21-22 | Made by: @Menesesp20",
                         x = 0.51, y = 0.95,
                         color='#181818', fontweight='bold',
                         ha='center',
                         fontsize=16);

        #################################################################################################################################################
        # RIGHT
        fig_text(s = str(rightfinal3rdTotal) + ' ' + '%',
                x = 0.777, y = 0.43,
                color='black', fontweight='bold', ha='center' ,fontsize=35);

        # xT Right

        ax.scatter( 14 , 63.3 , marker ='d', lw=2, edgecolor='black', facecolor='None', s = 10000, zorder=3)

        fig_text(s =str(round(xT_Sides.right_xT[0], 2)),
                x = 0.77, y = 0.35,
                color='black', fontweight='bold', ha='center' ,fontsize=28);

        #################################################################################################################################################
        # LEFT
        fig_text(s = str(leftfinal3rdTotal) + ' ' + '%',
                x = 0.283, y = 0.43,
                color='black', fontweight='bold', ha='center' ,fontsize=35);

        # xT Left
        ax.scatter( 83 , 63.3 , marker ='d', lw=2, edgecolor='black', facecolor='None', s = 10000, zorder=3)

        fig_text(s = str(round(xT_Sides.left_xT[0], 2)),
                x = 0.275, y = 0.35,
                color='black', fontweight='bold', ha='center' ,fontsize=27);

        #################################################################################################################################################
        # CENTER
        fig_text(s = str(centerfinal3rdTotal) + ' ' + '%',
                x = 0.525, y = 0.43,
                color='black', fontweight='bold', ha='center' ,fontsize=35);

        # xT Center

        ax.scatter( 49.5 , 63.3 , marker ='d', lw=2, edgecolor='black', facecolor='None', s = 10000, zorder=3)

        fig_text(s = str(round(xT_Sides.center_xT[0], 2)),
                x = 0.515, y = 0.35,
                color='black', fontweight='bold', ha='center' ,fontsize=28);

        #################################################################################################################################################

        left =  str(leftfinal3rdTotal)
        center = str(centerfinal3rdTotal)
        right = str(rightfinal3rdTotal)

        if right > left > center:

                # LEFT ZONE
                rectangleLeft = patches.Rectangle([67, 50], width=33, height=50, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.5, zorder=1 )

                # CENTER ZONE
                rectangleCenter = patches.Rectangle([33.1, 50], width=33.8, height=55, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.3, zorder=1 )

                # RIGHT ZONE
                rectangleRight = patches.Rectangle([0, 50], width=33, height=50, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.8, zorder=1)

        elif left > right > center:

                # LEFT ZONE
                rectangleLeft = patches.Rectangle([67, 50], width=33, height=50, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.8, zorder=1 )

                # CENTER ZONE
                rectangleCenter = patches.Rectangle([33.1, 50], width=33.8, height=55, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.3, zorder=1 )

                # RIGHT ZONE
                rectangleRight = patches.Rectangle([0, 50], width=33, height=50, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.5, zorder=1)

        ##################################################################################################################

        elif center > right > left:

                # LEFT ZONE
                rectangleLeft = patches.Rectangle([67, 50], width=33, height=50, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.3, zorder=1 )

                # CENTER ZONE
                rectangleCenter = patches.Rectangle([33.1, 50], width=33.8, height=55, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.8, zorder=1 )

                # RIGHT ZONE
                rectangleRight = patches.Rectangle([0, 50], width=33, height=50, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.5, zorder=1)

        elif right > center > left:

                # LEFT ZONE
                rectangleLeft = patches.Rectangle([67, 50], width=33, height=50, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.3, zorder=1 )

                # CENTER ZONE
                rectangleCenter = patches.Rectangle([33.1, 50], width=33.8, height=55, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.5, zorder=1 )

                # RIGHT ZONE
                rectangleRight = patches.Rectangle([0, 50], width=33, height=50, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.8, zorder=1)

        ##################################################################################################################

        elif center > left > right:

                # LEFT ZONE
                rectangleLeft = patches.Rectangle([67, 50], width=33, height=50, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.5, zorder=1 )

                # CENTER ZONE
                rectangleCenter = patches.Rectangle([33.1, 50], width=33.8, height=55, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.8, zorder=1 )

                # RIGHT ZONE
                rectangleRight = patches.Rectangle([0, 50], width=33, height=50, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.3, zorder=1)

        elif center > left > right:

                # LEFT ZONE
                rectangleLeft = patches.Rectangle([67, 50], width=33, height=50, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.8, zorder=1 )

                # CENTER ZONE
                rectangleCenter = patches.Rectangle([33.1, 50], width=33.8, height=55, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.5, zorder=1 )

                # RIGHT ZONE
                rectangleRight = patches.Rectangle([0, 50], width=33, height=50, linewidth = 2, linestyle='-',
                                edgecolor='black', facecolor='#ff0000', alpha=0.3, zorder=1)


        # ADD RECTANGLES
        ax.add_patch(rectangleLeft)
        ax.add_patch(rectangleCenter)
        ax.add_patch(rectangleRight)
        #################################################################################################################################################

        # Key Passes Cluster
        if matchDay == 'All Season':
                for x in range(len(final3rd_Cluster['cluster'])):
                
                        if final3rd_Cluster['cluster'][x] == 5:
                                pitch.arrows(xstart=final3rd_Cluster['x'][x], ystart=final3rd_Cluster['y'][x],
                                        xend=final3rd_Cluster['endX'][x], yend=final3rd_Cluster['endY'][x],
                                        color='#ea04dc', alpha=0.5,
                                        lw=3, zorder=2,
                                        ax=ax)
                                
                        if final3rd_Cluster['cluster'][x] == 6:
                                pitch.arrows(xstart=final3rd_Cluster['x'][x], ystart=final3rd_Cluster['y'][x],
                                        xend=final3rd_Cluster['endX'][x], yend=final3rd_Cluster['endY'][x],
                                        color='#2d92df', alpha=0.5,
                                        lw=3, zorder=2,
                                        ax=ax)
                        
                        if final3rd_Cluster['cluster'][x] == 7:
                                pitch.arrows(xstart=final3rd_Cluster['x'][x], ystart=final3rd_Cluster['y'][x],
                                        xend=final3rd_Cluster['endX'][x], yend=final3rd_Cluster['endY'][x],
                                        color='#fb8c04', alpha=0.5,
                                        lw=3, zorder=2,
                                        ax=ax)
        elif matchDay != 'All Season':
                for x in range(len(final3rd_Cluster['cluster'])):
        
                        if final3rd_Cluster['cluster'][x] == 0:
                                pitch.arrows(xstart=final3rd_Cluster['x'][x], ystart=final3rd_Cluster['y'][x],
                                        xend=final3rd_Cluster['endX'][x], yend=final3rd_Cluster['endY'][x],
                                        color='#ea04dc', alpha=0.5,
                                        lw=3, zorder=2,
                                        ax=ax)
                                
                        if final3rd_Cluster['cluster'][x] == 2:
                                pitch.arrows(xstart=final3rd_Cluster['x'][x], ystart=final3rd_Cluster['y'][x],
                                        xend=final3rd_Cluster['endX'][x], yend=final3rd_Cluster['endY'][x],
                                        color='#2d92df', alpha=0.5,
                                        lw=3, zorder=2,
                                        ax=ax)
                        
                        if final3rd_Cluster['cluster'][x] == 1:
                                pitch.arrows(xstart=final3rd_Cluster['x'][x], ystart=final3rd_Cluster['y'][x],
                                        xend=final3rd_Cluster['endX'][x], yend=final3rd_Cluster['endY'][x],
                                        color='#fb8c04', alpha=0.5,
                                        lw=3, zorder=2,
                                        ax=ax)

        #################################################################################################################################################

        # Club Logo
        fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.07, bottom=0.91, width=0.2, height=0.1)

        # END NOTE
        fig_text(s = 'The values inside the diamond are the xT value for each third',
                 x = 0.5, y = 0.125,
                 color='#181818', fontweight='bold', ha='center' ,fontsize=16);

        fig_text(s = 'xT values based on Karun Singhs model',
                 x = 0.765, y = 0.875,
                 color='#181818', fontweight='bold', ha='center' ,fontsize=12);


#############################################################################################################################################################


def halfspaces_Zone14(Game, league, club, GameID=None):

        color = clubColors.get(club)

        if GameID != None:
            Game = Game.loc[(Game['Match_ID'] == GameID) & (Game['team'] == club)]
        elif GameID == None:
            Game = Game.loc[(Game['team'] == club)]

        fig, ax = plt.subplots(figsize=(18,15))

        pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                        pitch_color='#181818', line_color='white',
                        line_zorder=2, linewidth=5, spot_scale=0.00)

        pitch.draw(ax=ax)

        fig.set_facecolor('#181818')
        ###################################################################################################################################

        fig.suptitle('Athletic Club', fontsize=32, color='white', fontweight = "bold", x=0.5, y=0.95, ha='center', va='center')

        fig_text(s = 'Half Spaces & Zone 14 | Season 21-22 | @menesesp20',
                 x = 0.5, y = 0.91, color='white', ha='center', va='center', fontweight = "bold", fontsize=10);

        ###################################################################################################################################

        ZONE14 = patches.Rectangle([20.8, 68], width=58, height=15, linewidth = 2, linestyle='-',
                                edgecolor='white', facecolor='#eb00e5', alpha=0.5, zorder=1 )

        HalfSpaceLeft = patches.Rectangle([67, 67.8], width=20, height=78, linewidth = 2, linestyle='-',
                                edgecolor='white', facecolor='#2894e5', alpha=0.5, zorder=1 )

        HalfSpaceRight = patches.Rectangle([13, 67.8], width=20, height=78, linewidth = 2, linestyle='-',
                                edgecolor='white', facecolor='#2894e5', alpha=0.5, zorder=1 )

        ###################################################################################################################################

        # HALF SPACE LEFT

        halfspaceleft = Game[(Game.endY <= 83) & (Game.endY >= 65) &
                                        (Game.endX >= 78) &
                                        (Game.typedisplayName == 'Pass')][['name', 'teamId', 'typedisplayName', 'qualifiers', 'x', 'y', 'endX', 'endY']]

        pitch.arrows(xstart=halfspaceleft['x'], ystart=halfspaceleft['y'],
                                            xend=halfspaceleft['endX'], yend=halfspaceleft['endY'],
                                            color='#2894e5', alpha=0.3,
                                            lw=3, zorder=2,
                                            ax=ax)

        ###################################################################################################################################

        # ZONE14

        zone14 = Game[(Game.endX <= 83) & (Game.endX >= 75) &
                                (Game.endY <= 66) & (Game.endY >= 35) &
                                (Game.typedisplayName == 'Pass')][['name', 'teamId', 'typedisplayName', 'qualifiers', 'x', 'y', 'endX', 'endY']]

        pitch.arrows(xstart=zone14['x'], ystart=zone14['y'],
                                            xend=zone14['endX'], yend=zone14['endY'],
                                            color='#2894e5', alpha=0.3,
                                            lw=3, zorder=2,
                                            ax=ax)

        ###################################################################################################################################

        # HALF SPACE RIGHT

        halfspaceright = Game[(Game.endY >= 17) & (Game.endY <= 33) &
                                (Game.endX >= 78) &
                                (Game.typedisplayName == 'Pass')][['name', 'teamId', 'typedisplayName', 'qualifiers', 'x', 'y', 'endX', 'endY']]

        pitch.arrows(xstart=halfspaceright['x'], ystart=halfspaceright['y'],
                                            xend=halfspaceright['endX'], yend=halfspaceright['endY'],
                                            color='#2894e5', alpha=0.3,
                                            lw=3, zorder=2,
                                            ax=ax)

        ###################################################################################################################################

        ax.add_patch(ZONE14)
        ax.add_patch(HalfSpaceLeft)
        ax.add_patch(HalfSpaceRight)

        ###################################################################################################################################

        # Club Logo
        fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.24, bottom=0.885, width=0.2, height=0.07)


#############################################################################################################################################################

def pitchZonesActions(df, colEvent, eventName, league, club, playerName=None):

        color = clubColors.get(club)

        if playerName != None:
          player = df.loc[(eventsPlayers[colEvent] == eventName) & (df.name == playerName)]
        else:
          player = df.loc[(eventsPlayers[colEvent] == eventName) & (df.team == club)]

        pitch = VerticalPitch(pitch_type='opta', line_zorder=2,
                                pitch_color='#181818', line_color='#efefef')

        fig, ax = pitch.draw(figsize=(15, 10))
        fig.set_facecolor('#181818')

        pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                                ['#181818', color[0]], N=9)

        scatter = pitch.scatter(player.x, player.y, ax=ax, edgecolor='white', facecolor='black', alpha=0.5, zorder=2)

        bs = pitch.bin_statistic(player.x, player.y, bins=(3, 3))
        heatmap = pitch.heatmap(bs, edgecolors='#181818', ax=ax, cmap=pearl_earring_cmap)

        ######################################################################################################################

        # RIGHT UP

        zone7 = player.loc[(player.x >= 65) & (player.y <= 35)]

        # CENTER UP

        zone8 = player.loc[(player.x >= 65) & (player.y >= 35) & (player.y <= 65)]

        # LEFT UP

        zone9 = player.loc[(player.x >= 65) & (player.y >= 65)]


        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone7) / len(player)) * 100, 2)) + '%',
                 x = 0.63, y = 0.80, color='white', fontweight='bold', ha='center' ,fontsize=25);

        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone8) / len(player)) * 100, 2)) + '%',
                 x = 0.5, y = 0.80, color='white', fontweight='bold', ha='center' ,fontsize=25);

        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone9) / len(player)) * 100, 2)) + '%',
                 x = 0.38, y = 0.80, color='white', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################

        # RIGHT MIDDLE

        zone4 = player.loc[(player.x >= 35) & (player.x <= 65) & (player.y <= 35)]

        # CENTER MIDDLE

        zone5 = player.loc[(player.x >= 35) & (player.x <= 65) & (player.y >= 35) & (player.y <= 65)]

        # LEFT MIDDLE

        zone6 = player.loc[(player.x >= 35) & (player.x <= 65) & (player.y >= 65)]


        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone4) / len(player)) * 100, 2)) + '%',
                 x = 0.63, y = 0.515, color='white', fontweight='bold', ha='center' ,fontsize=25);

        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone5) / len(player)) * 100, 2)) + '%',
                 x = 0.5, y = 0.515, color='white', fontweight='bold', ha='center' ,fontsize=25);

        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone6) / len(player)) * 100, 2)) + '%',
                 x = 0.38, y = 0.515, color='white', fontweight='bold', ha='center' ,fontsize=25);

        ######################################################################################################################

        # RIGHT DOWM

        zone1 = player.loc[(player.x <= 35) & (player.y <= 35)]

        # CENTER DOWN

        zone2 = player.loc[(player.x <= 35) & (player.y >= 35) & (player.y <= 65)]

        # LEFT DOWM

        zone3 = player.loc[(player.x <= 35) & (player.y >= 65)]

        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone1) / len(player)) * 100, 2)) + '%',
                 x = 0.63, y = 0.23, color='white', fontweight='bold', ha='center' ,fontsize=25);

        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone2) / len(player)) * 100, 2)) + '%',
                 x = 0.5, y = 0.23, color='white', fontweight='bold', ha='center' ,fontsize=25);

        # TOTAL PER ZONE
        fig_text(s = str(round((len(zone3) / len(player)) * 100, 2)) + '%',
                 x = 0.38, y = 0.23, color='white', fontweight='bold', ha='center' ,fontsize=25);

        # Club Logo
        fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.23, bottom=0.975, width=0.2, height=0.1)

        if playerName != None:
          # TITLE
          fig_text(s =  playerName,
                   x = 0.5, y = 1.06, color='white', fontweight='bold', ha='center', va='center', fontsize=40);
        else:
          # TITLE
          fig_text(s =  club,
                   x = 0.5, y = 1.06, color='white', fontweight='bold', ha='center', va='center', fontsize=40);

        # TITLE
        fig_text(s = 'Recovery ball percentage per zone',
                x = 0.5, y = 1, color='white', fontweight='bold', ha='center', va='center', fontsize=12);


#############################################################################################################################################################


def passing_network(data, matchDay, league, team, after, isDashboard=None, axx=None):

        ###########################################################################################################################
        network = data.loc[(data['team'] == team) & (data['Match_ID'] == matchDay)]

        network = network.sort_values(['minute', 'second'], ascending=True)

        passes = network.loc[(network['typedisplayName'] == 'Pass') & (network['outcomeTypedisplayName'] == 'Successful')]

        ###########################################################################################################################

        if after == False:

                subs = network.loc[network['typedisplayName'] == 'SubstitutionOff']
                subs = subs['minute']
                firstSub = subs.min()

                df_pas = passes.loc[(passes['minute'] < firstSub)]
                df_pas['passer'] = df_pas['Abreviation']
                df_pas['recipient'] = df_pas['Abreviation'].shift(-1)
        elif after == True:

                subs = network.loc[network['typedisplayName'] == 'SubstitutionOff']
                subs = subs['minute']
                firstSub = subs.min()

                df_pas = passes.loc[(passes['minute'] > firstSub)]
                df_pas['passer'] = df_pas['Abreviation']
                df_pas['recipient'] = df_pas['Abreviation'].shift(-1)
        ###########################################################################################################################

        avg = df_pas.groupby('passer').agg({'x':['mean'], 'y':['mean', 'count']})
        avg.columns = ['x_avg', 'y_avg', 'count']

        ###########################################################################################################################

        btw = df_pas.groupby(['passer', 'recipient']).id.count().reset_index()
        btw.rename({'id':'pass_count'}, axis='columns', inplace=True)

        merg1 = btw.merge(avg, left_on='passer', right_index=True)
        pass_btw = merg1.merge(avg, left_on='recipient', right_index=True, suffixes=['', '_end'])

        pass_btw = pass_btw.loc[pass_btw['pass_count'] > 1]

        ##################################################################################################################################################################

        if isDashboard == None:
                size=1000
                radius = math.sqrt(size)/2.
                arrow = mpl.patches.FancyArrowPatch(posA=(pass_btw.x_avg, pass_btw.y_avg), 
                                                posB=(pass_btw.x_avg_end, pass_btw.y_avg_end), 
                                                arrowstyle='-|>', mutation_scale=20, shrinkA=radius, shrinkB=radius)


                #Make arrows less transparent if they have a higher count, totally optional of course
                min_transparency = 0.3
                color = np.array(to_rgba('white'))
                color = np.tile(color, (len(pass_btw), 1))
                c_transparency = pass_btw.pass_count / pass_btw.pass_count.max()
                c_transparency = (c_transparency * (1 - min_transparency)) + min_transparency
                color[:, 3] = c_transparency

                fig, ax = plt.subplots(figsize=(18,14))

                pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                                pitch_color='#181818', line_color='white',
                                line_zorder=1, linewidth=5, spot_scale=0.005)

                pitch.draw(ax=ax)

                fig.set_facecolor('#181818')

                #plot arrows
                def pass_line_template(ax, x, y, end_x, end_y, line_color):
                        ax.annotate('', xy=(end_y, end_x), xytext=(y, x), zorder=2,
                        arrowprops=dict(arrowstyle='-|>', linewidth=4, color='#c7d5cc', alpha=.85))
                
                def pass_line_template_shrink(ax, x, y, end_x, end_y, line_color, dist_delta=1):
                        dist = math.hypot(end_x - x, end_y - y)
                        angle = math.atan2(end_y-y, end_x-x)
                        upd_x = x + (dist - dist_delta) * math.cos(angle)
                        upd_y = y + (dist - dist_delta) * math.sin(angle)
                        pass_line_template(ax, x, y, upd_x, upd_y, line_color=line_color)
                        
                
                for index, row in pass_btw.iterrows():
                        pass_line_template_shrink(ax,row['x_avg'],row['y_avg'],row['x_avg_end'],row['y_avg_end'], color)

                #plot nodes
                pass_nodes = pitch.scatter(avg.x_avg, avg.y_avg, s=450,
                                        color='#ff0000', edgecolors="#010101", linewidth=2, ax=ax, zorder=3)


                #Uncomment these next two lines to get each node labeled with the player id. Check to see if anything looks off, and make note of each player if you're going to add labeles later like their numbers
                for index, row in avg.iterrows():
                        pitch.annotate(row.name, xy=(row.x_avg, row.y_avg), c='white', va='center', ha='center', size=16, fontweight='bold', ax=ax)


                ##################################################################################################################################################################

                df = data.loc[(data.Match_ID == matchDay)]

                home = df.home_Team.unique()
                homeName = home[0]
                color = clubColors.get(homeName)


                away = df.away_Team.unique()
                awayName = away[0]
                color2 = clubColors.get(awayName)

                ##################################################################################################################################################################

                #Params for the text inside the <> this is a function to highlight text
                highlight_textprops =\
                        [{"color": color[0],"fontweight": 'bold'},
                        {"color": color2[0],"fontweight": 'bold'}]

                fig_text(s = f'<{homeName}>' + ' ' + 'vs' + ' ' + f'<{awayName}>',
                        x = 0.52, y = 1,
                        color='white', fontweight='bold', ha='center',
                        highlight_textprops = highlight_textprops,
                        fontsize=32);

                fig_text(s = 'Passing Network' + ' ' + '|' + ' ' + 'MatchDay' + ' ' + str(matchDay) + '| Season 2021 - 22 | @menesesp20',
                        x = 0.52, y = 0.96,
                        color='white', fontweight='bold', ha='center',
                        fontsize=14);

                # Club Logo
                fig = add_image(image='Images/Clubs/' + league + '/' + team + '.png', fig=fig, left=0.20, bottom=0.91, width=0.2, height=0.1)

        ##################################################################################################################################################################

        if isDashboard != None:

                pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                                pitch_color='#181818', line_color='white',
                                line_zorder=1, linewidth=5, spot_scale=0.005)

                pitch.draw(ax=axx)

                size=1000
                radius = math.sqrt(size)/2.
                arrow = mpl.patches.FancyArrowPatch(posA=(pass_btw.x_avg, pass_btw.y_avg), 
                                                posB=(pass_btw.x_avg_end, pass_btw.y_avg_end), 
                                                arrowstyle='-|>', mutation_scale=20, shrinkA=radius, shrinkB=radius)


                #Make arrows less transparent if they have a higher count, totally optional of course
                min_transparency = 0.3
                color = np.array(to_rgba('white'))
                color = np.tile(color, (len(pass_btw), 1))
                c_transparency = pass_btw.pass_count / pass_btw.pass_count.max()
                c_transparency = (c_transparency * (1 - min_transparency)) + min_transparency
                color[:, 3] = c_transparency

                pitch = VerticalPitch(pitch_type='opta',pad_top=0.1, pad_bottom=0.5,
                                pitch_color='#181818', line_color='white',
                                line_zorder=1, linewidth=5, spot_scale=0.005)

                pitch.draw(ax=axx)

                #plot arrows
                def pass_line_template(axx, x, y, end_x, end_y, line_color):
                        axx.annotate('', xy=(end_y, end_x), xytext=(y, x), zorder=2,
                        arrowprops=dict(arrowstyle='-|>', linewidth=4, color='#c7d5cc', alpha=.85))
                
                def pass_line_template_shrink(axx, x, y, end_x, end_y, line_color, dist_delta=1):
                        dist = math.hypot(end_x - x, end_y - y)
                        angle = math.atan2(end_y-y, end_x-x)
                        upd_x = x + (dist - dist_delta) * math.cos(angle)
                        upd_y = y + (dist - dist_delta) * math.sin(angle)
                        pass_line_template(axx, x, y, upd_x, upd_y, line_color=line_color)
                        
                
                for index, row in pass_btw.iterrows():
                        pass_line_template_shrink(axx, row['x_avg'],row['y_avg'],row['x_avg_end'],row['y_avg_end'], color)

                #plot nodes
                pass_nodes = pitch.scatter(avg.x_avg, avg.y_avg, s=280,
                                        color='#ff0000', edgecolors="#010101", linewidth=2, ax=axx, zorder=3)


                #Uncomment these next two lines to get each node labeled with the player id. Check to see if anything looks off, and make note of each player if you're going to add labeles later like their numbers
                for index, row in avg.iterrows():
                        pitch.annotate(row.name, xy=(row.x_avg, row.y_avg), c='white', va='center', ha='center', size=12, fontweight='bold', ax=axx)


#############################################################################################################################################################

def dashboardPassingNetwork(data, matchDay, league, club):

        df = data.loc[(data.Match_ID == matchDay)]

        home = df.home_Team.unique()
        homeName = home[0]
        color = clubColors.get(homeName)


        away = df.away_Team.unique()
        awayName = away[0]
        color2 = clubColors.get(awayName)

        fig  = plt.figure(figsize=(15, 10), dpi = 90)
        grid = plt.GridSpec(12, 12)

        a1 = fig.add_subplot(grid[0:10, 0:6])
        a2 = fig.add_subplot(grid[0:10, 6:12])
        
        #################################################################################################################################################

        #Params for the text inside the <> this is a function to highlight text
        highlight_textprops =\
        [{"color": color[0],"fontweight": 'bold'},
         {"color": color2[0],"fontweight": 'bold'}]

        # Club Logo
        add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.05, bottom=0.943, width=0.2, height=0.12)

        fig.set_facecolor('#181818')

        title = f'<{homeName}>' + ' ' + 'vs' + ' ' + f'<{awayName}>'

        if len(title) >= 30:
                fig_text(s = title,
                        x = 0.52, y = 1.05,
                        color='white', fontweight='bold', ha='center',
                        highlight_textprops = highlight_textprops,
                        fontsize=40);

                fig_text(s = 'MatchDay' + ' ' + str(matchDay) + '| Season 2021 - 22 | @menesesp20',
                        x = 0.5, y = 0.99,
                        color='white', fontweight='bold', ha='center' ,fontsize=12, alpha=0.5);

        elif len(title) <= 30:
                fig_text(s = title,
                        x = 0.5, y = 1.05,
                        color='white', fontweight='bold', ha='center',
                        highlight_textprops = highlight_textprops,
                        fontsize=40);
        
                fig_text(s = 'MatchDay' + ' ' + str(matchDay) + '| Season 2021 - 22 | @menesesp20',
                        x = 0.5, y = 0.99,
                        color='white', fontweight='bold', ha='center' ,fontsize=12, alpha=0.5);

        fig_text(s = 'Before Sub',
                 x = 0.32, y = 0.91, color='white', fontweight='bold', ha='center' ,fontsize=16);

        fig_text(s = 'After Sub',
                 x = 0.71, y = 0.91, color='white', fontweight='bold', ha='center' ,fontsize=16);

        #################################################################################################################################################
        # 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE

        passing_network(data, matchDay, 'La Liga', club, False, True, a1)

        #################################################################################################################################################
        # 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE

        passing_network(data, matchDay, 'La Liga', club, True, True, a2)



#Automatização do processo de criação do gráfico de campo de futebol com os passes realizados
def convex_hullDefensive(df, player_name, league, club):

  df = df.loc[(df['name'] == player_name) & (df['x'] <= 50) & ((df['typedisplayName'] == 'BallRecovery') |
                                                (df['typedisplayName'] == 'Tackle') |
                                                (df['typedisplayName'] == 'Interception') |
                                                (df['typedisplayName'] == 'Aerial') |
                                                (df['typedisplayName'] == 'Clearance'))]
  #Successful defensive actions
  succ = df.loc[df['outcomeTypedisplayName'] == 'Successful']

  #Unsuccessful defensive actions
  insucc = df.loc[df['outcomeTypedisplayName'] == 'Unsuccessful']
  
  #Tackle rate
  tackle = df.loc[df['typedisplayName'] == 'Tackle']

  tackle_successful = df[(df['typedisplayName'] == 'Tackle') & (df['outcomeTypedisplayName'] == 'Successful')]

  tackle_Rate = round((len(tackle_successful) / len(tackle)) * 100, 2)

  #Aerial rate
  aerial = df[df['typedisplayName'] == 'Aerial']

  aerial_successful = df[(df['typedisplayName'] == 'Aerial') & (df['outcomeTypedisplayName'] == 'Successful')]

  aerial_Rate = round((len(aerial_successful) / len(aerial) * 100) , 2)

  # Plotting the pitch

  fig, ax = plt.subplots(figsize=(18,14))

  pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                        pitch_color='#181818', line_color='white',
                        line_zorder=1, linewidth=5, spot_scale=0.005)

  pitch.draw(ax=ax)

  fig.set_facecolor('#181818')

  convex = df.loc[(np.abs(stats.zscore(df[['x','y']])) < 1).all(axis=1)]

  hull = pitch.convexhull(convex['x'], convex['y'])

  poly = pitch.polygon(hull, ax=ax, edgecolor='white', facecolor='white', alpha=0.3, linestyle='--', linewidth=2.5)

  scatter1 = pitch.scatter(succ['x'], succ['y'], ax=ax, marker='8', edgecolor='white', alpha=0.8, facecolor='none', hatch='//////', linestyle='--', s=150)

  scatter2 = pitch.scatter(insucc['x'], insucc['y'], ax=ax, marker='8', edgecolor='#ff0000', facecolor='none', hatch='//////', linestyle='--',  s=150)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------

  #Params for the text inside the <> this is a function to highlight text
  highlight_textpropsSuccessfu =\
      [{"color": "white","fontweight": 'bold'}
      ]

  #Legend Successfull Actions
  fig_text(s = '<Successfull Actions>',
            x = 0.638, y = 0.68, highlight_textprops = highlight_textpropsSuccessfu,
            fontweight='bold', ha='center', fontsize=12, color='white');
            
#--------------------------------------------------------------------------------------------------------------------------------------------------------------

  #Params for the text inside the <> this is a function to highlight text
  highlight_textpropsUnsuccessful =\
      [{"color": "#ff0000", "fontweight": 'bold', 'alpha' : 0.8}
      ]

  #Legend Unsuccessfull Actions
  fig_text(s = '<Unsuccessfull Actions>',
            x = 0.632, y = 0.66,
            highlight_textprops = highlight_textpropsUnsuccessful,
            fontweight='bold', ha='center',
            fontsize=12, color='white');

#--------------------------------------------------------------------------------------------------------------------------------------------------------------

  #Legend Tackle
  fig_text(s = 'Tackle Rate' + ' ' + f'{tackle_Rate}' + '%',
            x = 0.385, y = 0.68,
            fontweight='bold' ,ha='center',
            fontsize=12, color='white');
  #Legend Aerial     
  fig_text(s = 'Aerial Rate' + ' ' + f'{aerial_Rate}' + '%',
            x = 0.385, y = 0.66,
            fontweight='bold', ha='center',
            fontsize=12, color='white');

  #Defensive Actions included
  fig_text(s = 'Defensive action include' + ' ' + 'BallRecovery,' + ' ' + 'Tackle,' + ' ' + 'Interception,' + ' ' + 'Aerial,' + ' ' + 'Clearance',
            x = 0.512, y = 0.11,
            fontweight='bold', ha='center',
            fontsize=11, color='white');

#--------------------------------------------------------------------------------------------------------------------------------------------------------------

  #Linha média do eixo x
  plt.axhline(df['x'].mean(), c='#ff0000', linestyle='--', LineWidth=2)

  #Defensive Actions included
  fig_text(s = 'Average\nline of\nengagement:' + ' ' + str(round(df['x'].mean(),2 )) + 'm.',
           x = 0.273, y = 0.35,
           fontweight='bold', ha='center',
           fontsize=14, color='white');

#--------------------------------------------------------------------------------------------------------------------------------------------------------------

  #Params for the text inside the <> this is a function to highlight text
  highlight_textprops =\
    [{"color": "white","fontweight": 'bold'}]

  fig_text(s =f'<{player_name}>' + ' ' + 'Defensive Actions',
            x = 0.52, y = 0.97,
            ha='center', va='center',
            highlight_textprops = highlight_textprops, color='white', fontweight='bold',
            fontsize=30);

  fig_text(s ='Season 21-22' + ' ' + league,
            x = 0.52, y = 0.935,
            ha='center', va='center',
            color='white', fontweight='bold',
            fontsize=16);

  # Club Logo
  fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.18, bottom=0.90, width=0.2, height=0.09)


#############################################################################################################################################################

















































