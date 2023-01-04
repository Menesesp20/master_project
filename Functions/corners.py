import pandas as pd
import numpy as np


import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

from mplsoccer import VerticalPitch, add_image

from soccerplots.utils import add_image

from highlight_text import fig_text

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
from . import data as d

eventsPlayers = d.getDataOPTA()
eventsPlayers['isTouch'] = eventsPlayers['isTouch'].astype(bool)

#For loop to create a new column in the DataFrame
teamName = []
for id in eventsPlayers['teamId']:
    if id == 1237:
        teamName.append('Corinthians')
    elif id == 4619:
        teamName.append('Avai')
    elif id == 1239:
        teamName.append('Flamengo')
    elif id == 1234:
        teamName.append('Palmeiras')
    elif id == 167:
        teamName.append('Man City')
    elif id == 52:
        teamName.append('Real Madrid')
    elif id == 26:
        teamName.append('Liverpool')
    elif id == 839:
        teamName.append('Villarreal')
    elif id == 53:
        teamName.append('Athletic Club')
    elif id == 52:
        teamName.append('Real Madrid')
    elif id == 65:
        teamName.append('FC Barcelona')
    elif id == 63:
        teamName.append('Atlético Madrid')
    elif id == 67:
        teamName.append('Sevilla')
    elif id == 54:
        teamName.append('Real Betis')
    elif id == 68:
        teamName.append('Real Sociedad')
    elif id == 839:
        teamName.append('Villarreal')
    elif id == 55:
        teamName.append('Valencia')
    elif id == 131:
        teamName.append('Osasuna')
    elif id == 62:
        teamName.append('Celta Vigo')
    elif id == 70:
        teamName.append('Espanyol')
    elif id == 64:
        teamName.append('Rayo Vallecano')
    elif id == 819:
        teamName.append('Getafe')
    elif id == 833:
        teamName.append('Elche')
    elif id == 925:
        teamName.append('Granada')
    elif id == 1354:
        teamName.append('Cadiz')
    elif id == 51:
        teamName.append('Mallorca')
    elif id == 832:
        teamName.append('Levante')
    elif id == 60:
        teamName.append('Deportivo Alavés')
        
eventsPlayers['team'] = teamName

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
              'Flamengo' : ['#ff0000', '#E8E8E8'],
              'Palmeiras' : ['#046434', '#e8e8e8'],
              ###################################
              'Manchester City' : ['#7bb1d8', '#062e63'],
              'Liverpool' : ['#d40424', '#e2e1ab']}


#############################################################################################################################################################

def search_qualifierOPTA(df, list_Name, event):
  cols = df.columns

  list_Name = pd.DataFrame(columns=cols)

  df.reset_index(inplace=True)

  for idx, row in df.iterrows():
    if event in df['qualifiers'][idx]:
        events = pd.DataFrame([df.iloc[idx][cols].values], columns=cols)
        list_Name = pd.concat([list_Name, events], ignore_index=True)
          
  list_Name = list_Name.loc[~list_Name.index.duplicated(), :]

  return list_Name


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


def cornersTaken(df, league, club, matchDay):

        if 'level_0' in df.columns:
                df.drop(['level_0'], axis=1, inplace=True)
        else:
                pass
        
        cornersData = []

        df_Corner = search_qualifierOPTA(df, cornersData, 'CornerTaken')

        right_corner = df_Corner.loc[df_Corner.y < 50]

        left_corner = df_Corner.loc[df_Corner.y > 50]

        #################################################################################################################################################

        # Plotting the pitch

        fig, ax = plt.subplots(figsize=(18,14))

        pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                        pitch_color='#E8E8E8', line_color='#E8E8E8', half = True, line_zorder=1, linewidth=5, spot_scale=0.00)

        pitch.draw(ax=ax)

        fig.set_facecolor('#E8E8E8')

        #################################################################################################################################################

        # Title of our plot - WITH ANGLES BOTTOM: 0.98, 0.93

        fig.suptitle(club + ' ' + 'Corners', fontsize=40, color='#E8E8E8', fontweight = "bold", x=0.5, y=0.955, ha='center', va='center')

        Title = fig_text(s = 'Season 21-22 | Made by: @Menesesp20',
                         x = 0.5, y = 0.91,
                         color='#E8E8E8', fontweight='bold', ha='center', va='center', fontsize=16);

        #################################################################################################################################################

        firstCorner_L_Cluster = cluster_Event(left_corner, club, 'Pass', matchDay, 3, False)

        firstCorner_L_Cluster['cluster'].value_counts().reset_index(drop=True)

        #################################################################################################################################################

        firstCorner_R_Cluster = cluster_Event(right_corner, club, 'Pass', matchDay, 3, False)

        firstCorner_R_Cluster['cluster'].value_counts().reset_index(drop=True)

        #################################################################################################################################################

        # RIGHT SIDE CLUSTER
        for x in range(len(firstCorner_R_Cluster['cluster'])):

                if firstCorner_R_Cluster['cluster'][x] == 0:
                        pitch.arrows(xstart=firstCorner_R_Cluster['x'][x], ystart=firstCorner_R_Cluster['y'][x],
                                xend=firstCorner_R_Cluster['endX'][x], yend=firstCorner_R_Cluster['endY'][x],
                                color='#eb00e5', alpha=0.7,
                                lw=3, zorder=2,
                                ax=ax)
        # CIRCLE                            
        ax.scatter( 40 , 95 , s = 20000, color='#eb00e5', alpha=0.5, lw=3)

        ax.annotate('', xy=(18, 84), xytext=(5, 84),
                size=14, color = '#eb00e5', fontweight = "bold",
                arrowprops=dict(arrowstyle="->", color='#eb00e5', lw=3))

        fig_text(s = 'Most frequent zone',
                 x = 0.794, y = 0.66,
                 color='#eb00e5', fontweight='bold', ha='center', va='center', fontsize=12);

        #################################################################################################################################################

        # LEFT SIDE CLUSTER
        for x in range(len(firstCorner_L_Cluster['cluster'])):        
                if firstCorner_L_Cluster['cluster'][x] == 1:
                        pitch.arrows(xstart=firstCorner_L_Cluster['x'][x], ystart=firstCorner_L_Cluster['y'][x],
                                xend=firstCorner_L_Cluster['endX'][x], yend=firstCorner_L_Cluster['endY'][x],
                                color='#2894e5', alpha=0.7,
                                lw=3, zorder=2,
                                ax=ax)
        # CIRCLE                            
        ax.scatter( 60 , 95 , s = 20000, color='#2894e5', alpha=0.5, lw=3)

        ax.annotate('', xy=(83, 84), xytext=(95, 84),
                size=14, color = '#2894e5', fontweight = "bold",
                arrowprops=dict(arrowstyle="->", color='#2894e5', lw=3))

        fig_text(s = 'Most frequent zone',
                 x = 0.23, y = 0.66,
                 color='#2894e5', fontweight='bold', ha='center', va='center', fontsize=12);

        #################################################################################################################################################

        # PENTAGON RIGHT                          
        ax.scatter( 40 , 65 , marker = 'p', s = 20000, color='#eb00e5', alpha=0.5, lw=3)

        fig_text(s =  str(len(firstCorner_R_Cluster)),
                        x = 0.584, y = 0.378,
                        color='#E8E8E8', fontweight='bold', ha='center' ,fontsize=30);

        #################################################################################################################################################

        # PENTAGON LEFT                           
        ax.scatter( 60 , 65 , marker = 'p', s = 20000, color='#2894e5', alpha=0.5, lw=3)

        fig_text(s = str(len(firstCorner_L_Cluster)),
                 x = 0.44, y = 0.378,
                 color='#E8E8E8', fontweight='bold', ha='center' ,fontsize=30);

        #################################################################################################################################################

        # Club Logo - WITH ANGLES BOTTOM: 0.89, LEFT:0.14
        fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.08, bottom=0.87, width=0.2, height=0.1)

        #################################################################################################################################################

        # Angle Left Logo
        #fig = add_image(image='angleLeft.png', fig=fig, left=0.082, bottom=0.842, width=0.2, height=0.1)

        # ANGLE LEFT VALUE
        #fig_text(s = '4.6°',
        #                x = 0.179, y = 0.887,
        #                fontfamily = 'medium', color='#E8E8E8', fontweight='bold', ha='center' ,fontsize=15);

        #################################################################################################################################################

        # Angle Right Logo
        #fig = add_image(image='angleRight.png', fig=fig, left=0.7425, bottom=0.842, width=0.2, height=0.1)

        # ANGLE RIGHT VALUE
        #fig_text(s = '1.8°',
        #                x = 0.846, y = 0.887,
        #                fontfamily = 'medium', color='#E8E8E8', fontweight='bold', ha='center' ,fontsize=15);

        fig_text(s = 'The values inside pentagon are the total of corners made by each side',
                x = 0.338, y = 0.129,
                color='#E8E8E8', fontweight='bold', ha='center' ,fontsize=12);


def corners1stPostTaken(df, league, club, matchDay):
        
        if 'level_0' in df.columns:
                df.drop(['level_0'], axis=1, inplace=True)
        else:
                pass
        
        cornersData = []

        df_Corner = search_qualifierOPTA(df, cornersData, 'CornerTaken')

        right_corner = df_Corner.loc[df_Corner.y < 50]

        left_corner = df_Corner.loc[df_Corner.y > 50]

        #################################################################################################################################################

        # Plotting the pitch

        fig, ax = plt.subplots(figsize=(18,14))

        pitch = VerticalPitch(pitch_type='opta',pad_top=0.1, pad_bottom=0.5,
                        pitch_color='#E8E8E8', line_color='#E8E8E8', half = True, line_zorder=1, linewidth=5, spot_scale=0.00)

        pitch.draw(ax=ax)

        fig.set_facecolor('#E8E8E8')

        #################################################################################################################################################

        # Title of our plot - WITH ANGLES BOTTOM: 0.98, 0.93

        fig.suptitle(club + ' ' + '1st Post Corners', fontsize=40, color='#E8E8E8',
                      fontweight = "bold", x=0.525, y=0.955)

        Title = fig_text(s = 'Season 21-22 | Made by: @Menesesp20',
                         x = 0.5, y = 0.91,
                         color='#E8E8E8', fontweight='bold', ha='center' ,fontsize=16);

        #################################################################################################################################################

        firstCorner_L = left_corner.loc[(left_corner.endY >= 55) & (left_corner.endY <= 79)]

        firstCorner_L_Cluster = cluster_Event(firstCorner_L, club, 'Pass', matchDay, 3, False)

        firstCorner_L_Cluster['cluster'].value_counts().reset_index(drop=True)

        #################################################################################################################################################

        firstCorner_R = right_corner.loc[(right_corner.endY <= 45) & (right_corner.endY >= 21)]

        firstCorner_R_Cluster = cluster_Event(firstCorner_R, club, 'Pass', matchDay, 3, False)

        firstCorner_R_Cluster['cluster'].value_counts().reset_index(drop=True)

        #################################################################################################################################################

        # RIGHT SIDE CLUSTER
        for x in range(len(firstCorner_R_Cluster['cluster'])):

                if firstCorner_R_Cluster['cluster'][x] == 2:
                        pitch.arrows(xstart=firstCorner_R_Cluster['x'][x], ystart=firstCorner_R_Cluster['y'][x],
                                xend=firstCorner_R_Cluster['endX'][x], yend=firstCorner_R_Cluster['endY'][x],
                                color='#eb00e5', alpha=0.7,
                                lw=3, zorder=2,
                                ax=ax)
        # CIRCLE                            
        ax.scatter( 40 , 95 , s = 20000, color='#eb00e5', alpha=0.5, lw=3)

        ax.annotate('', xy=(18, 84), xytext=(5, 84),
                size=14, color = '#eb00e5', fontweight = "bold",
                arrowprops=dict(arrowstyle="->", color='#eb00e5', lw=3))

        fig_text(s = 'Most frequent zone',
                x = 0.794, y = 0.66,
                fontfamily = 'medium', color='#eb00e5', fontweight='bold', ha='center' ,fontsize=12);

        #################################################################################################################################################

        # LEFT SIDE CLUSTER
        for x in range(len(firstCorner_L_Cluster['cluster'])):        
                if firstCorner_L_Cluster['cluster'][x] == 0:
                        pitch.arrows(xstart=firstCorner_L_Cluster['x'][x], ystart=firstCorner_L_Cluster['y'][x],
                                xend=firstCorner_L_Cluster['endX'][x], yend=firstCorner_L_Cluster['endY'][x],
                                color='#2894e5', alpha=0.7,
                                lw=3, zorder=2,
                                ax=ax)
        # CIRCLE                            
        ax.scatter( 60 , 95 , s = 20000, color='#2894e5', alpha=0.5, lw=3)

        ax.annotate('', xy=(83, 84), xytext=(95, 84),
                size=14, color = '#2894e5', fontweight = "bold",
                arrowprops=dict(arrowstyle="->", color='#2894e5', lw=3))

        fig_text(s = 'Most frequent zone',
                x = 0.23, y = 0.66,
                color='#2894e5', fontweight='bold', ha='center' ,fontsize=12);

        #################################################################################################################################################

        # PENTAGON RIGHT                          
        ax.scatter( 40 , 65 , marker = 'p', s = 20000, color='#eb00e5', alpha=0.5, lw=3)

        # VALUE FIRST CORNER MOST FREQUENT ON RIGHT SIDE
        len1stCornerR = len(firstCorner_R_Cluster.loc[firstCorner_R_Cluster['cluster']==0])

        firstCornerR =  int((len1stCornerR / len(firstCorner_R_Cluster) * 100))

        fig_text(s =  str(firstCornerR) + '%',
                        x = 0.584, y = 0.378,
                        color='#E8E8E8', fontweight='bold', ha='center' ,fontsize=28);

        #################################################################################################################################################

        # PENTAGON LEFT                           
        ax.scatter( 60 , 65 , marker = 'p', s = 20000, color='#2894e5', alpha=0.5, lw=3)

        # VALUE FIRST CORNER MOST FREQUENT ON LEFT SIDE
        len1stCornerL = len(firstCorner_L_Cluster.loc[firstCorner_L_Cluster['cluster']==0])

        firstCornerL = int((len1stCornerL / len(firstCorner_L_Cluster) * 100))

        fig_text(s = str(firstCornerL) + '%',
                        x = 0.44, y = 0.378,
                        color='#E8E8E8', fontweight='bold', ha='center' ,fontsize=28);

        #################################################################################################################################################

        # Club Logo - WITH ANGLES BOTTOM: 0.89, LEFT:0.14
        fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.12, bottom=0.87, width=0.2, height=0.1)

        #################################################################################################################################################

        # Angle Left Logo
        #fig = add_image(image='angleLeft.png', fig=fig, left=0.082, bottom=0.842, width=0.2, height=0.1)

        # ANGLE LEFT VALUE
        #fig_text(s = '4.6°',
        #                x = 0.179, y = 0.887,
        #                fontfamily = 'medium', color='#E8E8E8', fontweight='bold', ha='center' ,fontsize=15);

        #################################################################################################################################################

        # Angle Right Logo
        #fig = add_image(image='angleRight.png', fig=fig, left=0.7425, bottom=0.842, width=0.2, height=0.1)

        # ANGLE RIGHT VALUE
        #fig_text(s = '1.8°',
        #                x = 0.846, y = 0.887,
        #                fontfamily = 'medium', color='#E8E8E8', fontweight='bold', ha='center' ,fontsize=15);

        fig_text(s = 'The values inside pentagon are the percentage of corners made by each side for the circle area',
                x = 0.407, y = 0.14,
                color='#E8E8E8', fontweight='bold', ha='center' ,fontsize=12);


def corners2ndPostTaken(df, league, club, matchDay):
        
        if 'level_0' in df.columns:
                df.drop(['level_0'], axis=1, inplace=True)
        else:
                pass
        
        cornersData = []

        df_Corner = search_qualifierOPTA(df, cornersData, 'CornerTaken')

        right_corner = df_Corner.loc[df_Corner.y < 50]

        left_corner = df_Corner.loc[df_Corner.y > 50]

        #################################################################################################################################################

        # Plotting the pitch

        fig, ax = plt.subplots(figsize=(18,14))

        pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                        pitch_color='#E8E8E8', line_color='#E8E8E8', half = True, line_zorder=1, linewidth=5, spot_scale=0.00)

        pitch.draw(ax=ax)

        fig.set_facecolor('#E8E8E8')

        #################################################################################################################################################

        # Title of our plot - WITH ANGLES BOTTOM: 0.98, 0.93

        fig.suptitle(club + ' ' + '2nd Post Corners', fontsize=40, color='#E8E8E8',
        fontweight = "bold", x=0.525, y=0.955)

        Title = fig_text(s = 'Season 21-22 | Made by: @Menesesp20',
                        x = 0.5, y = 0.91,
                        color='#E8E8E8', fontweight='bold', ha='center' ,fontsize=16);

        #################################################################################################################################################

        secondCorner_L = left_corner.loc[(left_corner.endY <= 55) & (left_corner.endY >= 21) & (left_corner.endX >= 90)]
        if secondCorner_L.shape[0] == 0:
                pass
        else:
                secondCorner_L_Cluster = cluster_Event(secondCorner_L, club, 'Pass', matchDay, 3, False)

                secondCorner_L_Cluster['cluster'].value_counts().reset_index(drop=True)

                # LEFT SIDE CLUSTER
                for x in range(len(secondCorner_L_Cluster['cluster'])):        
                        if secondCorner_L_Cluster['cluster'][x] == 1:
                                pitch.arrows(xstart=secondCorner_L_Cluster['x'][x], ystart=secondCorner_L_Cluster['y'][x],
                                        xend=secondCorner_L_Cluster['endX'][x], yend=secondCorner_L_Cluster['endY'][x],
                                        color='#2894e5', alpha=0.7,
                                        lw=3, zorder=2,
                                        ax=ax)
                
                # CIRCLE 2nd Post                           
                ax.scatter( 40 , 95 , s = 20000, color='#2894e5', alpha=0.5, lw=3)

                # PENTAGON LEFT                           
                ax.scatter( 60 , 65 , marker = 'p', s = 20000, color='#2894e5', alpha=0.5, lw=3)

                len2ndCornerL = len(secondCorner_L_Cluster.loc[secondCorner_L_Cluster['cluster']==0])

                secondCornerL = int((len2ndCornerL / len(secondCorner_L_Cluster) * 100))

                fig_text(s = str(secondCornerL) + '%',
                                x = 0.44, y = 0.378,
                                fontfamily = 'medium', color='#E8E8E8', fontweight='bold', ha='center' ,fontsize=28);

        #################################################################################################################################################

        secondCorner_R = right_corner.loc[(right_corner.endY <= 75) & (right_corner.endY >= 55) & (right_corner.endX >= 90)]
        if secondCorner_R.shape[0] == 0:
                pass
        else:
                secondCorner_R_Cluster = cluster_Event(secondCorner_R, club, 'Pass', matchDay, 3, False)
                
                secondCorner_R_Cluster['cluster'].value_counts().reset_index(drop=True)

                # RIGHT SIDE CLUSTER
                for x in range(len(secondCorner_R_Cluster['cluster'])):

                        if secondCorner_R_Cluster['cluster'][x] == 1:
                                pitch.arrows(xstart=secondCorner_R_Cluster['x'][x], ystart=secondCorner_R_Cluster['y'][x],
                                        xend=secondCorner_R_Cluster['endX'][x], yend=secondCorner_R_Cluster['endY'][x],
                                        color='#eb00e5', alpha=0.7,
                                        lw=3, zorder=2,
                                        ax=ax)
                                        
                # CIRCLE 1st Post                           
                ax.scatter( 60 , 95 , s = 20000, color='#eb00e5', alpha=0.5, lw=3)            

                # PENTAGON RIGHT                          
                ax.scatter( 40 , 65 , marker = 'p', s = 20000, color='#eb00e5', alpha=0.5, lw=3)

                len2ndCornerR = len(secondCorner_R_Cluster.loc[secondCorner_R_Cluster['cluster']==0])

                secondCornerR = int((len2ndCornerR / len(secondCorner_R_Cluster) * 100))

                fig_text(s =  str(secondCornerR) + '%',
                                x = 0.584, y = 0.378,
                                color='#E8E8E8', fontweight='bold', ha='center' ,fontsize=30);


        #################################################################################################################################################

        # MOST FREQUENT ZONES ARROWS
        ax.annotate('', xy=(18, 84), xytext=(5, 84),
                size=14, color = '#eb00e5', fontweight = "bold",
                arrowprops=dict(arrowstyle="->", color='#eb00e5', lw=3))

        fig_text(s = 'Most frequent zone',
                x = 0.794, y = 0.66,
                color='#eb00e5', fontweight='bold', ha='center' ,fontsize=12);

        #################################################################################################################################################

        # MOST FREQUENT ZONES ARROWS
        ax.annotate('', xy=(83, 84), xytext=(95, 84),
                size=14, color = '#2894e5', fontweight = "bold",
                arrowprops=dict(arrowstyle="->", color='#2894e5', lw=3))

        fig_text(s = 'Most frequent zone',
                x = 0.23, y = 0.66,
                color='#2894e5', fontweight='bold', ha='center' ,fontsize=12);

        #################################################################################################################################################

        # Club Logo - WITH ANGLES BOTTOM: 0.89, LEFT:0.14
        fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.12, bottom=0.87, width=0.2, height=0.1)

        #################################################################################################################################################

        # Angle Left Logo
        #fig = add_image(image='angleLeft.png', fig=fig, left=0.082, bottom=0.842, width=0.2, height=0.1)

        # ANGLE LEFT VALUE
        #fig_text(s = '4.6°',
        #                x = 0.179, y = 0.887,
        #                fontfamily = 'medium', color='#E8E8E8', fontweight='bold', ha='center' ,fontsize=15);

        #################################################################################################################################################

        # Angle Right Logo
        #fig = add_image(image='angleRight.png', fig=fig, left=0.7425, bottom=0.842, width=0.2, height=0.1)

        # ANGLE RIGHT VALUE
        #fig_text(s = '1.8°',
        #                x = 0.846, y = 0.887,
        #                fontfamily = 'medium', color='#E8E8E8', fontweight='bold', ha='center' ,fontsize=15);

        fig_text(s = 'The values inside pentagon are the percentage of corners made by each side for the circle area',
                x = 0.407, y = 0.129,
                color='#E8E8E8', fontweight='bold', ha='center' ,fontsize=12);


