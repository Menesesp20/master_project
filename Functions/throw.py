import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

from mplsoccer import Pitch, VerticalPitch, Radar, FontManager, add_image

from soccerplots.utils import add_image

from highlight_text import  ax_text, fig_text

from soccerplots.utils import add_image

from sklearn.cluster import KMeans

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

#############################################################################################################################################################

<<<<<<< HEAD
<<<<<<< HEAD
from Functions.data import getDataOPTA
from Functions.data import getDataWyScout

#############################################################################################################################################################

eventsPlayers = getDataOPTA()
=======
@st.cache
def data():
    eventsPlayers = pd.read_csv('Data/opta/optaData.csv')
    return eventsPlayers

eventsPlayers = data()
>>>>>>> parent of 73d9b2d (update)
=======
@st.cache
def data():
    eventsPlayers = pd.read_csv('Data/opta/optaData.csv')
    return eventsPlayers

eventsPlayers = data()
>>>>>>> parent of 73d9b2d (update)
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
              'Cadiz' : ['#f9e310', '#0045a8'],
              ###################################
              'Corinthians' : ['#ff0000', '#e8e8e8'],
              'Avai' : ['#00679a', '#e8e8e8'],
              'Flamengo' : ['#ff0000', '#181818'],
              'Palmeiras' : ['#046434', '#e8e8e8'],
              ###################################
              'Manchester City' : ['#7bb1d8', '#062e63'],
              'Liverpool' : ['#d40424', '#e2e1ab']}

#############################################################################################################################################################

def search_qualifierOPTA(df, event):
  cols = ['Match_ID', 'name', 'x', 'y', 'endX', 'endY',
          'minute', 'second',
          'typedisplayName', 'outcomeTypedisplayName',
          'qualifiers', 'satisfiedEventsTypes',
          'teamId', 'team']

  list_Name = pd.DataFrame(columns=cols)

  df.reset_index(inplace=True)

  for idx, row in df.iterrows():
    if event in df['qualifiers'][idx]:
        events = pd.DataFrame([df.iloc[idx][cols].values], columns=cols)
        list_Name = pd.concat([list_Name, events], ignore_index=True)
          
  list_Name = list_Name.loc[~list_Name.index.duplicated(), :]

  return list_Name

corners = []

corners = search_qualifierOPTA(eventsPlayers, 'CornerTaken')

cols_Cluster = ['team', 'typedisplayName', 'qualifiers', 'x', 'y', 'endX', 'endY']

cols_coords = ['x', 'y', 'endX', 'endY']

def cluster_Event(df, cols, teamNome, event_type, event_name, cols_coords, n_clusters, qualifier=None):

  df_cluster = df[cols]

  if qualifier != None:
    df_cluster = df_cluster[(df_cluster['team'] == teamNome) & (df_cluster['x'] < 99.5) &
                            (df[qualifier].str.contains(event_name) == True)].reset_index()
  else:
    df_cluster = df_cluster[(df_cluster['team'] == teamNome) & (df[event_type] == event_name)].reset_index()

  df_cluster.drop(['index'], axis=1, inplace=True)

  X = np.array(df_cluster[cols_coords])
  kmeans = KMeans(n_clusters = n_clusters, random_state=100)
  kmeans.fit(X)
  df_cluster['cluster'] = kmeans.predict(X)

  return df_cluster

def SetPiece_throwIn(df, league, club, n_Cluster, match=None):

        cols_coords = ['x', 'y', 'endX', 'endY']

        if (match == 'All Season'):
                match = df.copy()
        elif (match != 'All Season'):
                match = df.loc[df['Match_ID'] == match]
        elif match == None:
                match = df.copy()

        #################################################################################################################################################

        # DEFEND SIDE
        defendLeft = match.loc[(match.x < 35) & (match.y > 50)]

        defendRight = match.loc[(match.x < 35) & (match.y < 50)]

        # MIDDLE SIDE
        middleLeft = match.loc[(match.x > 35) & (match.x < 65) & (match.y > 50)]

        middleRight = match.loc[(match.x > 35) & (match.x < 65) & (match.y < 50)]

        # ATTACK SIDE
        attackLeft = match.loc[(match.x > 65) & (match.y > 50)]

        attackRight = match.loc[(match.x > 65) & (match.y < 50)]

        #################################################################################################################################################

        # Plotting the pitch

        fig, ax = plt.subplots(figsize=(21,15))

        pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                              pitch_color='#E8E8E8', line_color='#181818',
                              line_zorder=1, linewidth=5, spot_scale=0.00)

        pitch.draw(ax=ax)

        fig.set_facecolor('#E8E8E8')

        #################################################################################################################################################

        # Title of our plot - WITH ANGLES BOTTOM: 0.98, 0.93

        fig.suptitle(club + ' ' + "Throw-In's", fontsize=32, color='#181818', fontweight = "bold", x=0.5, y=0.955, ha='center', va='center')

        Title = fig_text(s = 'Season 21-22 | Made by: @Menesesp20',
                         x = 0.5, y = 0.91,
                         color='#181818', fontweight='bold', ha='center', va='center', fontsize=11);

        #################################################################################################################################################
        # DEFEND SIDE CLUSTER
        defendLeft_Cluster = cluster_Event(defendLeft, cols_Cluster, club, 'typedisplayName', 'Pass', cols_coords, n_Cluster)

        defendLeft_Cluster['cluster'].value_counts().reset_index(drop=True)

        defendRight_Cluster = cluster_Event(defendRight, cols_Cluster, club, 'typedisplayName', 'Pass', cols_coords, n_Cluster)

        defendRight_Cluster['cluster'].value_counts().reset_index(drop=True)

        #################################################################################################################################################

        # MIDDLE SIDE CLUSTER
        middleLeft_Cluster = cluster_Event(middleLeft, cols_Cluster, club, 'typedisplayName', 'Pass', cols_coords, n_Cluster)

        middleLeft_Cluster['cluster'].value_counts().reset_index(drop=True)

        middleRight_Cluster = cluster_Event(middleRight, cols_Cluster, club, 'typedisplayName', 'Pass', cols_coords, n_Cluster)

        middleRight_Cluster['cluster'].value_counts().reset_index(drop=True)

        #################################################################################################################################################

        # ATTACK SIDE CLUSTER
        attackLeft_Cluster = cluster_Event(attackLeft, cols_Cluster, club, 'typedisplayName', 'Pass', cols_coords, n_Cluster)

        attackLeft_Cluster['cluster'].value_counts().reset_index(drop=True)

        attackRight_Cluster = cluster_Event(attackRight, cols_Cluster, club, 'typedisplayName', 'Pass', cols_coords, n_Cluster)

        attackRight_Cluster['cluster'].value_counts().reset_index(drop=True)

        ####################################################################################################################################################
        # DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND
        #################################################################################################################################################
        if defendLeft_Cluster.shape[0] == 0:
                pass
        else:
                for x in range(len(defendLeft_Cluster['cluster'])):
                        
                        if defendLeft_Cluster['cluster'][x] == 0:
                                pitch.arrows(xstart=defendLeft_Cluster['x'][x], ystart=defendLeft_Cluster['y'][x],
                                        xend=defendLeft_Cluster['endX'][x], yend=defendLeft_Cluster['endY'][x],
                                        color='#eb00e5',
                                        lw=3, zorder=2,
                                        ax=ax)
        ####################################################################################################################################################
        # DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND DEFEND
        ####################################################################################################################################################

        if defendRight_Cluster.shape[0] == 0:
                pass
        else:
                for x in range(len(defendRight_Cluster['cluster'])):
                        
                        if defendRight_Cluster['cluster'][x] == 0:
                                pitch.arrows(xstart=defendRight_Cluster['x'][x], ystart=defendRight_Cluster['y'][x],
                                        xend=defendRight_Cluster['endX'][x], yend=defendRight_Cluster['endY'][x],
                                        color='#2894e5',
                                        lw=3, zorder=2,
                                        ax=ax)

        ####################################################################################################################################################
        # MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE
        ####################################################################################################################################################

        if middleLeft_Cluster.shape[0] == 0:
                pass
        else:
                for x in range(len(middleLeft_Cluster['cluster'])):
                        
                        if middleLeft_Cluster['cluster'][x] == 0:
                                pitch.arrows(xstart=middleLeft_Cluster['x'][x], ystart=middleLeft_Cluster['y'][x],
                                        xend=middleLeft_Cluster['endX'][x], yend=middleLeft_Cluster['endY'][x],
                                        color='#ffe506',
                                        lw=3, zorder=2,
                                        ax=ax)

        ####################################################################################################################################################
        # MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE MIDDLE
        ####################################################################################################################################################

        if middleRight_Cluster.shape[0] == 0:
                pass
        else:
                for x in range(len(middleRight_Cluster['cluster'])):
                        
                        if middleRight_Cluster['cluster'][x] == 0:
                                pitch.arrows(xstart=middleRight_Cluster['x'][x], ystart=middleRight_Cluster['y'][x],
                                        xend=middleRight_Cluster['endX'][x], yend=middleRight_Cluster['endY'][x],
                                        color='#ffe506',
                                        lw=3, zorder=2,
                                        ax=ax)

        ####################################################################################################################################################
        # ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK
        ####################################################################################################################################################
        if attackLeft_Cluster.shape[0] == 0:
                pass
        else:
                for x in range(len(attackLeft_Cluster['cluster'])):
                        
                        if attackLeft_Cluster['cluster'][x] == 0:
                                pitch.arrows(xstart=attackLeft_Cluster['x'][x], ystart=attackLeft_Cluster['y'][x],
                                        xend=attackLeft_Cluster['endX'][x], yend=attackLeft_Cluster['endY'][x],
                                        color='#eb00e5',
                                        lw=3, zorder=2,
                                        ax=ax)
                                        
        #################################################################################################################################################
        # ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK  ATTACK
        #################################################################################################################################################

        if attackRight_Cluster.shape[0] == 0:
                pass
        else:
                for x in range(len(attackRight_Cluster['cluster'])):
                        
                        if attackRight_Cluster['cluster'][x] == 0:
                                pitch.arrows(xstart=attackRight_Cluster['x'][x], ystart=attackRight_Cluster['y'][x],
                                        xend=attackRight_Cluster['endX'][x], yend=attackRight_Cluster['endY'][x],
                                        color='#2894e5',
                                        lw=3, zorder=2,
                                        ax=ax)

        #################################################################################################################################################

        fig_text(s = 'Blue - Right Side',
                 x = 0.648, y = 0.10,
                 color='#2894e5', fontweight='bold', ha='center' ,fontsize=12);

        fig_text(s = 'Purple - Left Side',
                 x = 0.38, y = 0.10,
                 color='#eb00e5', fontweight='bold', ha='center' ,fontsize=12);

        fig_text(s = 'Yellow - Middle Side',
                 x = 0.518, y = 0.10,
                 color='#ffe506', fontweight='bold', ha='center' ,fontsize=12);

        #################################################################################################################################################

        ax.axhline(35,c='white', ls='--', lw=4)
        ax.axhline(65,c='white', ls='--', lw=4)

        #################################################################################################################################################

        # ATTACK
        #fig_text(s = '12',
        #        x = 0.512, y = 0.683,
        #        fontfamily = 'medium', color='Black', fontweight='bold', ha='center' ,fontsize=30);

        #ax.scatter( 50 , 27 , marker = 'p', s = 12000, color='white', alpha=0.8, lw=3)

        # MIDDLE

        #fig_text(s = '12',
        #        x = 0.512, y = 0.518,
        #        fontfamily = 'medium', color='Black', fontweight='bold', ha='center' ,fontsize=30);

        #ax.scatter( 50 , 50 , marker = 'p', s = 12000, color='white', alpha=0.8, lw=3)

        # DEFENSE

        #fig_text(s = '12',
        #        x = 0.512, y = 0.348,
        #        fontfamily = 'medium', color='Black', fontweight='bold', ha='center' ,fontsize=30);

        #ax.scatter( 50 , 72 , marker = 'p', s = 12000, color='white', alpha=0.8, lw=3)

        # Club Logo - WITH ANGLES BOTTOM: 0.89, LEFT:0.14
        fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.259, bottom=0.887, width=0.2, height=0.06)

