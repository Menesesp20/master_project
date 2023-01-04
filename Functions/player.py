import pandas as pd
import numpy as np
import sys

import matplotlib.pyplot as plt

from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as patches

import warnings
warnings.filterwarnings("ignore")

from mplsoccer import Pitch, VerticalPitch, Radar, FontManager, add_image

from soccerplots.utils import add_image

from highlight_text import  ax_text, fig_text

from soccerplots.utils import add_image

from scipy import stats

from pandas.core.common import SettingWithCopyWarning

import warnings
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

sys.path.append('Functions')
from Functions import dashboard as ds
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

from data import getDataOPTA
from data import getDataWyScout

#############################################################################################################################################################

eventsPlayers = getDataOPTA()
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


def opponentHalf(df, player_name, league, club, matchDay):

  color = ['#FF0000', '#181818']

  df['beginning'] = np.sqrt(np.square(100 - df['x']) + np.square(100 - df['y']))
  df['end'] = np.sqrt(np.square(100 - df['endX']) + np.square(100 - df['endY']))

  df['progressive'] = [(df['end'][x]) / (df['beginning'][x]) < .75 for x in range(len(df.beginning))]

  df = df.loc[df.Match_ID == matchDay]

  df = df.loc[df['endX'] >= 70]

  player = df[df['name'] == player_name]

  keyPass = player[(player['qualifiers'].str.contains('KeyPass') == True) & (player['typedisplayName'] == 'Pass')]

  Pass = player[(player['typedisplayName'] == 'Pass')]

  sucess = player[(player['typedisplayName'] == 'Pass') & (player['outcomeTypedisplayName'] == 'Successful')]

  unsucess = player[(player['typedisplayName'] == 'Pass') & (player['outcomeTypedisplayName'] == 'Unsuccessful')]

  Progressive = Pass[Pass['progressive']==True]

  #Progressive = Progressive.loc[(Progressive.x > 99) | (Progressive.x > 1) & (Progressive.y > 55) & (Progressive.y < 99)]

  Pass_percentage = round((len(sucess) / len(Pass)) * 100, 2)

  #--------------------------------------------------------------------------------------------------------------------------------------------------------------

  fig, ax = plt.subplots(figsize=(18,14))

  pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                  pitch_color='#181818', line_color='white', half=True,
                  line_zorder=1, linewidth=5, spot_scale=0.00)

  pitch.draw(ax=ax)

  fig.set_facecolor('#181818')

  #Criação das setas que simbolizam os passes realizados bem sucedidos
  pitch.arrows(sucess.x, sucess.y, sucess.endX, sucess.endY, color='white', ax=ax,
              width=2, headwidth=5, headlength=5, label='Passes' + ':' + ' ' + f'{len(Pass)}' + ' ' + '(' + f'{Pass_percentage}' + '%' + ' ' + 'Completion rate' + ')' )
  
  #Criação das setas que simbolizam os passes realizados bem sucedidos
  pitch.arrows(unsucess.x, unsucess.y, unsucess.endX, unsucess.endY, color='#5d5e60', ax=ax,
              width=2, headwidth=5, headlength=5, label='Passes unsuccessful')

  #Criação das setas que simbolizam os passes realizados falhados
  pitch.arrows(Progressive.x, Progressive.y, Progressive.endX, Progressive.endY, color='#00bbf9', ax=ax,
              width=2, headwidth=5, headlength=5, label='Progressive passes' + ':' + ' ' + f'{len(Progressive)}')
 
  #Criação das setas que simbolizam os passes realizados falhados
  pitch.arrows(keyPass.x, keyPass.y, keyPass.endX, keyPass.endY, color='#ffba08', ax=ax,
              width=2, headwidth=0.1, headlength=0.1, label='Key passes' + ':' + ' ' + f'{len(keyPass)}')
  
  pitch.scatter(keyPass.endX, keyPass.endY, s = 150, marker='*', color='#ffba08', ax=ax)

  #--------------------------------------------------------------------------------------------------------------------------------------------------------------

  #Criação da legenda
  l = ax.legend(bbox_to_anchor=(0.02, 0), loc='upper left', facecolor='white', framealpha=0, labelspacing=.7)
  #Ciclo FOR para atribuir a white color na legend
  for text in l.get_texts():
      text.set_color("white")

  #Params for the text inside the <> this is a function to highlight text
  highlight_textprops =\
      [{"color": color[0],"fontweight": 'bold'}
        ]  

  fig_text(s =f'<{player_name}>' + ' ' + 'Pass Map',
            x = 0.5, y = 0.95, highlight_textprops = highlight_textprops,
            color='white', fontweight='bold', ha='center', va='center', fontsize=35);

  fig_text(s = 'MatchDay:' + ' ' +  str(matchDay) + ' ' + '| Opponent Half | Season 21-22 | @menesesp20',
            x = 0.5, y = 0.918,
            color='white', fontweight='bold', ha='center', va='center', fontsize=16, alpha=0.7);

  # Club Logo
  fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.15, bottom=0.88, width=0.2, height=0.09)


def intoBox(df, player_name, league, club, matchDay):

  color = ['#FF0000', '#181818']

  df['beginning'] = np.sqrt(np.square(100 - df['x']) + np.square(100 - df['y']))
  df['end'] = np.sqrt(np.square(100 - df['endX']) + np.square(100 - df['endY']))

  df['progressive'] = [(df['end'][x]) / (df['beginning'][x]) < .75 for x in range(len(df.beginning))]

  df = df.loc[df.Match_ID == matchDay]

  df = df.loc[(df['endX'] >= 83) & (df['endY'] >= 21.1) & (df['endY'] <= 78.9)]

  player = df[df['name'] == player_name]

  keyPass = player[(player['qualifiers'].str.contains('KeyPass') == True) & (player['typedisplayName'] == 'Pass')]

  Pass = player[(player['typedisplayName'] == 'Pass')]

  sucess = player[(player['typedisplayName'] == 'Pass') & (player['outcomeTypedisplayName'] == 'Successful')]

  unsucess = player[(player['typedisplayName'] == 'Pass') & (player['outcomeTypedisplayName'] == 'Unsuccessful')]

  Progressive = Pass[Pass['progressive']==True]

  Pass_percentage = round((len(sucess) / len(Pass)) * 100, 2)

  #--------------------------------------------------------------------------------------------------------------------------------------------------------------

  fig, ax = plt.subplots(figsize=(18,14))

  pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                  pitch_color='#181818', line_color='white', half=True,
                  line_zorder=1, linewidth=5, spot_scale=0.00)

  pitch.draw(ax=ax)

  fig.set_facecolor('#181818')

  #Criação das setas que simbolizam os passes realizados bem sucedidos
  pitch.arrows(sucess.x, sucess.y, sucess.endX, sucess.endY, color='white', ax=ax,
              width=2, headwidth=5, headlength=5, label='Passes' + ':' + ' ' + f'{len(Pass)}' + ' ' + '(' + f'{Pass_percentage}' + '%' + ' ' + 'Completion rate' + ')' )
  
  #Criação das setas que simbolizam os passes realizados bem sucedidos
  pitch.arrows(unsucess.x, unsucess.y, unsucess.endX, unsucess.endY, color='#cad2c5', ax=ax,
              width=2, headwidth=5, headlength=5, label='Passes unsuccessful')

  #Criação das setas que simbolizam os passes realizados falhados
  pitch.arrows(Progressive.x, Progressive.y, Progressive.endX, Progressive.endY, color='#00bbf9', ax=ax,
              width=2, headwidth=5, headlength=5, label='Progressive passes' + ':' + ' ' + f'{len(Progressive)}')

  #Criação das setas que simbolizam os passes realizados falhados
  pitch.arrows(keyPass.x, keyPass.y, keyPass.endX, keyPass.endY, color='#ffba08', ax=ax,
              width=2, headwidth=0.1, headlength=0.1, label='Key passes' + ':' + ' ' + f'{len(keyPass)}')
  
  pitch.scatter(keyPass.endX, keyPass.endY, s = 150, marker='*', color='#ffba08', ax=ax)

  #--------------------------------------------------------------------------------------------------------------------------------------------------------------  

  #Criação da legenda
  l = ax.legend(bbox_to_anchor=(0.02, 0), loc='upper left', facecolor='white', framealpha=0, labelspacing=.7)
  #Ciclo FOR para atribuir a white color na legend
  for text in l.get_texts():
      text.set_color("white")

  #Params for the text inside the <> this is a function to highlight text
  highlight_textprops =\
      [{"color": color[0],"fontweight": 'bold'}
        ]

  fig_text(s =f'<{player_name}>' + ' ' + 'Pass Map',
            x = 0.5, y = 0.95, highlight_textprops = highlight_textprops,
            color='white', fontweight='bold', ha='center', va='center', fontsize=35);

  fig_text(s = 'MatchDay:' + ' ' +  str(matchDay) + ' ' + '| Box Passes | Season 21-22 | @menesesp20',
            x = 0.5, y = 0.918,
            color='white', fontweight='bold', ha='center', va='center', fontsize=16, alpha=0.7);

  # Club Logo
  fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.15, bottom=0.88, width=0.2, height=0.09)


def draw_keyPasses_Dashboard(df, player_name, league, club, matchDay):

  color = ['#FF0000', '#181818']

  df['beginning'] = np.sqrt(np.square(100 - df['x']) + np.square(100 - df['y']))
  df['end'] = np.sqrt(np.square(100 - df['endX']) + np.square(100 - df['endY']))

  df['progressive'] = [(df['end'][x]) / (df['beginning'][x]) < .75 for x in range(len(df.beginning))]

  df = df.loc[df.Match_ID == matchDay]

  player = df[(df['name'] == player_name)]

  keyPass = player[(player['qualifiers'].str.contains('KeyPass') == True) & (player['typedisplayName'] == 'Pass')]

  Pass = player[(player['typedisplayName'] == 'Pass')]

  sucess = player[(player['typedisplayName'] == 'Pass') & (player['outcomeTypedisplayName'] == 'Successful')]

  unsucess = player[(player['typedisplayName'] == 'Pass') & (player['outcomeTypedisplayName'] == 'Unsuccessful')]

  Progressive = Pass[(Pass['progressive']==True)]

  #Progressive = Progressive.loc[(Progressive.x > 99) | (Progressive.x > 1) & (Progressive.y > 55) & (Progressive.y < 99)]

  Pass_percentage = round((len(sucess) / len(Pass)) * 100, 2)

  #--------------------------------------------------------------------------------------------------------------------------------------------------------------

  fig, ax = plt.subplots(figsize=(18,14))

  pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                  pitch_color='#181818', line_color='white',
                  line_zorder=1, linewidth=5, spot_scale=0.00)

  pitch.draw(ax=ax)

  fig.set_facecolor('#181818')

  #Criação das setas que simbolizam os passes realizados bem sucedidos
  pitch.arrows(sucess.x, sucess.y, sucess.endX, sucess.endY, color='white', ax=ax,
              width=2, headwidth=5, headlength=5, label='Passes' + ':' + ' ' + f'{len(Pass)}' + ' ' + '(' + f'{Pass_percentage}' + '%' + ' ' + 'Completion rate' + ')' )
  
  #Criação das setas que simbolizam os passes realizados bem sucedidos
  pitch.arrows(unsucess.x, unsucess.y, unsucess.endX, unsucess.endY, color='#cad2c5', ax=ax,
              width=2, headwidth=5, headlength=5, label='Passes unsuccessful' + ':' + ' ' + f'{len(unsucess)}')
  #Criação das setas que simbolizam os passes realizados falhados
  pitch.arrows(Progressive.x, Progressive.y, Progressive.endX, Progressive.endY, color='#00bbf9', ax=ax,
              width=2, headwidth=5, headlength=5, label='Progressive passes' + ':' + ' ' + f'{len(Progressive)}')

  #Criação das setas que simbolizam os passes realizados falhados
  pitch.arrows(keyPass.x, keyPass.y, keyPass.endX, keyPass.endY, color='#ffba08', ax=ax,
              width=2, headwidth=0.1, headlength=0.1, label='Key passes' + ':' + ' ' + f'{len(keyPass)}')
  
  pitch.scatter(keyPass.endX, keyPass.endY, s = 150, marker='*', color='#ffba08', ax=ax)
  
  #--------------------------------------------------------------------------------------------------------------------------------------------------------------
  
  #Criação da legenda
  l = ax.legend(bbox_to_anchor=(0.02, 0), loc='upper left', facecolor='white', framealpha=0, labelspacing=.7)
  #Ciclo FOR para atribuir a white color na legend
  for text in l.get_texts():
      text.set_color("white")

  #Params for the text inside the <> this is a function to highlight text
  highlight_textprops =\
      [{"color": color[0],"fontweight": 'bold'}
        ]

  fig_text(s =f'<{player_name}>' + ' ' + 'Pass Map',
            x = 0.5, y = 0.95, highlight_textprops = highlight_textprops, color='white', fontweight='bold', ha='center', va='center', fontsize=28);

  fig_text(s = 'MatchDay:' + ' ' +  str(matchDay) + ' ' + '| Season 21-22 | @menesesp20',
            x = 0.5, y = 0.918,
            color='white', fontweight='bold', ha='center', va='center', fontsize=12, alpha=0.7);

  # Club Logo
  fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.21, bottom=0.894, width=0.2, height=0.07)


def dashboardOffensive(events, league, club, playerName, matchDay):

        color = ['#ea04dc', '#181818']

        fig  = plt.figure(figsize=(15,8), dpi = 80)
        grid = plt.GridSpec(6, 6)

        a1 = fig.add_subplot(grid[0:5, 0:2])
        a2 = fig.add_subplot(grid[0:5, 2:4])
        a3 = fig.add_subplot(grid[0:5, 4:9])

        #################################################################################################################################################

        #Params for the text inside the <> this is a function to highlight text
        highlight_textprops =\
        [{"color": color[0],"fontweight": 'bold'},
        {"color": color[0],"fontweight": 'bold'}]

        # Club Logo
        add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.08, bottom=0.943, width=0.2, height=0.12)

        fig.set_facecolor('#181818')

        fig_text(s =f'<{playerName}>' + "<'s>" + ' ' + 'performance',
                 x = 0.48, y = 1.03, color='white', highlight_textprops = highlight_textprops, fontweight='bold', ha='center' ,fontsize=35);
        
        if matchDay != 'All Season':
                fig_text(s = 'MatchDay' + ' ' + str(matchDay) + '| Season 2022 | @menesesp20',
                        x = 0.365, y = 0.968,
                        color='white', fontweight='bold', ha='center' ,fontsize=12, alpha=0.5);

        elif matchDay == 'All Season':
                fig_text(s ='Season 2022 | @menesesp20',
                        x = 0.365, y = 0.968,
                        color='white', fontweight='bold', ha='center' ,fontsize=12, alpha=0.5);

        fig_text(s = 'Territory Plot',
                 x = 0.25, y = 0.91, color='white', fontweight='bold', ha='center' ,fontsize=14);

        fig_text(s = 'Pass Plot',
                 x = 0.513, y = 0.91, color='white', fontweight='bold', ha='center' ,fontsize=14);

        fig_text(s = 'xT Plot',
                 x = 0.78, y = 0.91, color='white', fontweight='bold', ha='center' ,fontsize=14);

        #################################################################################################################################################
        # 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE

        if matchDay != 'All Season':
                df = events.loc[(events['name'] == playerName) & (events['isTouch'] == True) & (events.Match_ID == matchDay)]

        elif matchDay == 'All Season':
                df = events.loc[(events['name'] == playerName) & (events['isTouch'] == True)]

        #shirt = df['shirtNo'].unique()
        #shirt = shirt[0]

        pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                        pitch_color='#181818', line_color='white',
                        line_zorder=2, linewidth=3, spot_scale=0.00)

        pitch.draw(ax=a1)

        #################################################################################################################################################

        pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                        ['#181818', color[0]], N=10)
        bs = pitch.bin_statistic(df.x, df.y, bins=(12, 8))

        pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                        ['#181818', color[0]], N=10)
        bs = pitch.bin_statistic(df.x, df.y, bins=(12, 8))

        convex = df[(np.abs(stats.zscore(df[['x','y']])) < .8).all(axis=1)]

        pitch.heatmap(bs, edgecolors='#181818', ax=a1, cmap=pearl_earring_cmap)

        pitch.scatter(df['x'], df['y'], ax=a1, edgecolor='white', facecolor='black', alpha=0.3)

        hull = pitch.convexhull(convex['x'], convex['y'])

        pitch.polygon(hull, ax=a1, edgecolor='white', facecolor='white', alpha=0.4, linestyle='--', linewidth=2.5)

        pitch.scatter(x=convex['x'].mean(), y=convex['y'].mean(), ax=a1, c='white', edgecolor=color[0], s=500, zorder=2)
        
        #fig_text(s = str(shirt),
        #         x = 0.328, y = 0.673, color=color[0], fontfamily = 'Courier New', fontweight='bold', ha='center', fontsize=14, zorder=2);

        #################################################################################################################################################
        # 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE

        events['beginning'] = np.sqrt(np.square(100 - events['x']) + np.square(100 - events['y']))
        events['end'] = np.sqrt(np.square(100 - events['endX']) + np.square(100 - events['endY']))

        events['progressive'] = [(events['end'][x]) / (events['beginning'][x]) < .75 for x in range(len(events.beginning))]

        if matchDay != 'All Season':
                df2 = events.loc[events['Match_ID'] == matchDay]

        if matchDay == 'All Season':
                df2 = events

        player = df2[df2['name'] == playerName]

        keyPass = player[(player['qualifiers'].str.contains('KeyPass') == True) & (player['typedisplayName'] == 'Pass')]

        Pass = player[(player['typedisplayName'] == 'Pass')]

        sucess = player[(player['typedisplayName'] == 'Pass') & (player['outcomeTypedisplayName'] == 'Successful')]

        unsucess = player[(player['typedisplayName'] == 'Pass') & (player['outcomeTypedisplayName'] == 'Unsuccessful')]

        Progressive = Pass[Pass['progressive']==True]

        #Progressive = Progressive.loc[(Progressive.x > 99) | (Progressive.x > 1) & (Progressive.y > 55) & (Progressive.y < 99)]

        Pass_percentage = round((len(sucess) / len(Pass)) * 100, 2)

        #################################################################################################################################################
        pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                pitch_color='#181818', line_color='white',
                line_zorder=2, linewidth=3, spot_scale=0.00)

        pitch.draw(ax=a2)

        fig.set_facecolor('#181818')

        #Criação das setas que simbolizam os passes realizados bem sucedidos
        pitch.arrows(sucess.x, sucess.y, sucess.endX, sucess.endY, color='white', ax=a2,
                width=2, headwidth=5, headlength=5, label='Passes' + ':' + ' ' + f'{len(Pass)}' + ' ' + '(' + f'{Pass_percentage}' + '%' + ' ' + 'Completion rate' + ')' )
        
        #Criação das setas que simbolizam os passes realizados bem sucedidos
        pitch.arrows(unsucess.x, unsucess.y, unsucess.endX, unsucess.endY, color='#cad2c5', ax=a2,
                width=2, headwidth=5, headlength=5, label='Passes unsuccessful' + ':' + ' ' + f'{len(unsucess)}')

        #Criação das setas que simbolizam os passes realizados falhados
        pitch.arrows(Progressive.x, Progressive.y, Progressive.endX, Progressive.endY, color='#00bbf9', ax=a2,
                width=2, headwidth=5, headlength=5, label='Progressive passes' + ':' + ' ' + f'{len(Progressive)}')

        #Criação das setas que simbolizam os passes realizados falhados
        pitch.arrows(keyPass.x, keyPass.y, keyPass.endX, keyPass.endY, color='#ffba08', ax=a2,
                width=2, headwidth=0.1, headlength=0.1, label='Key passes' + ':' + ' ' + f'{len(keyPass)}')
        
        pitch.scatter(keyPass.endX, keyPass.endY, s = 150, marker='*', color='#ffba08', ax=a2)
        #################################################################################################################################################

        matchDay = df.Match_ID.unique()
        matchDay = str(matchDay)
        matchDay = matchDay[1]
        #Criação da legenda
        l = a2.legend(bbox_to_anchor=(0.02, 0), loc='upper left', facecolor='white', framealpha=0, labelspacing=.7)
        #Ciclo FOR para atribuir a white color na legend
        for text in l.get_texts():
                text.set_color("white")

        #################################################################################################################################################
        # 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE

        if matchDay != 'All Season':
                df = events.loc[events['Match_ID'] == matchDay]

        if matchDay == 'All Season':
                df = events

        xTDF = ds.xT(eventsPlayers)

        xTheatMap = xTDF.loc[(xTDF.xT > 0) & (xTDF.name == playerName)]

        # setup pitch
        pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                pitch_color='#181818', line_color='white',
                line_zorder=2, linewidth=3, spot_scale=0.00)

        pitch.draw(ax=a3)

        fig.set_facecolor('#181818')

        pitch.draw(ax=a3)

        pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                                ['#181818', color[0]], N=10)

        bs = pitch.bin_statistic(xTheatMap.x, xTheatMap.y, bins=(12, 8))

        heatmap = pitch.heatmap(bs, edgecolors='#181818', ax=a3, cmap=pearl_earring_cmap)


def dashboardDeffensive(df, league, club, matchDay, playerName):

        color = ['#ea04dc', '#181818']

        fig = plt.figure(figsize=(15,8), dpi = 80)
        grid = plt.GridSpec(6, 6)

        a1 = fig.add_subplot(grid[0:5, 0:2])
        a2 = fig.add_subplot(grid[0:5, 2:4])
        a3 = fig.add_subplot(grid[0:5, 4:9])

        #################################################################################################################################################

        #Params for the text inside the <> this is a function to highlight text
        highlight_textprops =\
        [{"color": color[0],"fontweight": 'bold'},
        {"color": color[0],"fontweight": 'bold'}]

        # Club Logo
        fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.08, bottom=0.95, width=0.2, height=0.1)

        fig.set_facecolor('#181818')

        fig_text(s =f'<{playerName}>' + "<'s>" + ' ' + 'performance',
                 x = 0.465, y = 1.07, highlight_textprops = highlight_textprops,
                 color='white', fontweight='bold', ha='center' ,fontsize=35);
        
        if matchDay != 'All Season':
                fig_text(s = 'MatchDay:' + ' ' + str(matchDay) + ' ' + '| Season 2022 | @menesesp20',
                        x = 0.338, y = 0.98 , color='white', fontweight='bold', ha='center' ,fontsize=11);

        if matchDay == 'All Season':
                fig_text(s = 'Season 2022 | @menesesp20',
                        x = 0.40, y = 0.98 , color='white', fontweight='bold', ha='center' ,fontsize=11);

        fig_text(s = 'Territory Plot',
                 x = 0.25, y = 0.91 , color='white', fontweight='bold', ha='center' ,fontsize=14);

        fig_text(s = 'Pass Plot',
                 x = 0.513, y = 0.91, color='white', fontweight='bold', ha='center' ,fontsize=14);

        fig_text(s = 'Defensive Actions Plot',
                 x = 0.78, y = 0.91, color='white', fontweight='bold', ha='center' ,fontsize=14);

        #################################################################################################################################################
        # 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE

        if matchDay == 'All Season':
                df1 = df[(df['name'] == playerName) & (df['isTouch'] == True)]

        elif matchDay != 'All Season':
                df1 = df[(df['name'] == playerName) & (df['isTouch'] == True) & (df['Match_ID'] == matchDay)]

        pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                        pitch_color='#181818', line_color='white',
                        line_zorder=2, linewidth=3, spot_scale=0.00)

        pitch.draw(ax=a1)

        #################################################################################################################################################

        pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                        ['#181818', color[0]], N=10)
        bs = pitch.bin_statistic(df1.x, df1.y, bins=(12, 8))

        pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                        ['#181818', color[0]], N=10)
        bs = pitch.bin_statistic(df1.x, df1.y, bins=(12, 8))

        convex = df1[(np.abs(stats.zscore(df1[['x','y']])) < 1).all(axis=1)]

        pitch.heatmap(bs, edgecolors='#181818', ax=a1, cmap=pearl_earring_cmap)

        pitch.scatter(df1['x'], df1['y'], ax=a1, edgecolor='white', facecolor='black', alpha=0.3)

        hull = pitch.convexhull(convex['x'], convex['y'])

        pitch.polygon(hull, ax=a1, edgecolor='white', facecolor='white', alpha=0.4, linestyle='--', linewidth=2.5)

        pitch.scatter(x=convex['x'].mean(), y=convex['y'].mean(), ax=a1, c='white', edgecolor=color[0], s=700, zorder=2)


        #################################################################################################################################################
        # 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE


        df['beginning'] = np.sqrt(np.square(100 - df['x']) + np.square(100 - df['y']))
        df['end'] = np.sqrt(np.square(100 - df['endX']) + np.square(100 - df['endY']))

        df['progressive'] = [(df['end'][x]) / (df['beginning'][x]) < .75 for x in range(len(df.beginning))]

        if matchDay == 'All Season':
                player = df.loc[df['name'] == playerName]

        elif matchDay != 'All Season':
                player = df.loc[(df['name'] == playerName) & (df['Match_ID'] == matchDay)]

        keyPass = player[(player['qualifiers'].str.contains('KeyPass') == True) & (player['typedisplayName'] == 'Pass')]

        Pass = player[(player['typedisplayName'] == 'Pass')]

        sucess = player[(player['typedisplayName'] == 'Pass') & (player['outcomeTypedisplayName'] == 'Successful')]

        unsucess = player[(player['typedisplayName'] == 'Pass') & (player['outcomeTypedisplayName'] == 'Unsuccessful')]

        Progressive = Pass[Pass['progressive']==True]

        Pass_percentage = round((len(sucess) / len(Pass)) * 100, 2)

        #################################################################################################################################################
        pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                pitch_color='#181818', line_color='white',
                line_zorder=1, linewidth=3, spot_scale=0.00)

        pitch.draw(ax=a2)

        fig.set_facecolor('#181818')

        #Criação das setas que simbolizam os passes realizados bem sucedidos
        pitch.arrows(sucess.x, sucess.y, sucess.endX, sucess.endY, color='white', ax=a2,
                width=2, headwidth=5, headlength=5, label='Passes' + ':' + ' ' + f'{len(Pass)}' + ' ' + '(' + f'{Pass_percentage}' + '%' + ' ' + 'Completion rate' + ')' )
        
        #Criação das setas que simbolizam os passes realizados bem sucedidos
        pitch.arrows(unsucess.x, unsucess.y, unsucess.endX, unsucess.endY, color='#cad2c5', ax=a2,
                width=2, headwidth=5, headlength=5, label='Passes unsuccessful' + ':' + ' '  + f'{len(unsucess)}')

        #Criação das setas que simbolizam os passes realizados falhados
        pitch.arrows(Progressive.x, Progressive.y, Progressive.endX, Progressive.endY, color='#00bbf9', ax=a2,
                width=2, headwidth=5, headlength=5, label='Progressive passes' + ':' + ' ' + f'{len(Progressive)}')

        #Criação das setas que simbolizam os passes realizados falhados
        pitch.arrows(keyPass.x, keyPass.y, keyPass.endX, keyPass.endY, color='#ffba08', ax=a2,
                width=2, headwidth=0.1, headlength=0.1, label='Key passes' + ':' + ' ' + f'{len(keyPass)}')
        
        pitch.scatter(keyPass.endX, keyPass.endY, s = 150, marker='*', color='#ffba08', ax=a2)

        #################################################################################################################################################

        #Criação da legenda
        l = a2.legend(bbox_to_anchor=(0, 0), loc='upper left', facecolor='white', framealpha=0, labelspacing=.7)
        #Ciclo FOR para atribuir a white color na legend
        for text in l.get_texts():
                text.set_color("white")

        #################################################################################################################################################
        # 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE

        if matchDay == 'All Season':
                df3 = df.loc[(df.x <= 55) & (df.name == playerName)]

        elif matchDay != 'All Season':
                df3 = df.loc[(df.x <= 55) & (df.name == playerName) & (df['Match_ID'] == matchDay)]
        
        # Tackle
        tackle = df3.loc[(df3['typedisplayName'] == 'Tackle') & (df3['outcomeTypedisplayName'] == 'Successful')]

        tackleUn = df3.loc[(df3['typedisplayName'] == 'Tackle') & (df3['outcomeTypedisplayName'] == 'Unsuccessful')]

        # Interception
        interception = df3.loc[df3['typedisplayName'] == 'Interception']

        # Aerial
        aerial = df3.loc[(df3['typedisplayName'] == 'Aerial') & (df3['outcomeTypedisplayName'] == 'Successful')]

        aerialUn = df3.loc[(df3['typedisplayName'] == 'Aerial') & (df3['outcomeTypedisplayName'] == 'Unsuccessful')]

        # Clearance
        clearance = df3.loc[(df3['typedisplayName'] == 'Clearance') & (df3['outcomeTypedisplayName'] == 'Successful')]

        # Ball Recovery
        ballRecovery = df3.loc[(df3['typedisplayName'] == 'BallRecovery')]
        # Plotting the pitch

        pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                                pitch_color='#181818', line_color='white',
                                line_zorder=1, linewidth=5, spot_scale=0.005)

        pitch.draw(ax=a3)

        fig.set_facecolor('#181818')

        convex = df3.loc[(np.abs(stats.zscore(df3[['x','y']])) < 1).all(axis=1)]

        hull = pitch.convexhull(convex['x'], convex['y'])

        pitch.polygon(hull, ax=a3, edgecolor='white', facecolor='white', alpha=0.3, linestyle='--', linewidth=2.5)

        pitch.scatter(tackle['x'], tackle['y'], ax=a3, marker='s', color='#fac404', edgecolor='#fac404', linestyle='--', s=150, label='Tackle')

        pitch.scatter(ballRecovery['x'], ballRecovery['y'], ax=a3, marker='8', edgecolor='#fac404', facecolor='none', hatch='//////', linestyle='--', s=150, label='Ball Recovery')

        pitch.scatter(tackleUn['x'], tackleUn['y'], ax=a3, marker='s', color='#ff0000', edgecolor='#ff0000', linestyle='--', s=150)

        pitch.scatter(aerial['x'], aerial['y'], ax=a3, marker='^', color='#fac404', edgecolor='#fac404', linestyle='--', s=150, label='Aerial')

        pitch.scatter(aerialUn['x'], aerialUn['y'], ax=a3, marker='^', color='#ff0000', edgecolor='#ff0000', linestyle='--', s=150)
        
        pitch.scatter(interception['x'], interception['y'], ax=a3, marker='P', color='#fac404', edgecolor='#fac404',  linestyle='--', s=150, label='Interception')

        pitch.scatter(clearance['x'], clearance['y'], ax=a3, marker='*', color='#fac404', edgecolor='#fac404', linestyle='--', s=200, label='Clearance')


        #Criação da legenda
        l = a3.legend(bbox_to_anchor=(0, 0), loc='upper left', facecolor='white', framealpha=0, labelspacing=.7)
        #Ciclo FOR para atribuir a white color na legend
        for text in l.get_texts():
                text.set_color("white")


def dashboardTerritory(df, league, club, matchDay, playerName, playerName2, playerName3, playerName4=None):

        color = ['#ea04dc', '#181818']

        homeTeam = df['away_Team'].unique()

        homeTeam = homeTeam.tolist()

        homeTeam = homeTeam[0]

        opponent = df['home_Team'].unique()

        opponent = opponent.tolist()

        opponent = opponent[0]

        if playerName4 == None:
                fig = plt.figure(figsize=(15,8), dpi = 80)
                grid = plt.GridSpec(6, 6)

                a1 = fig.add_subplot(grid[0:5, 0:2])
                a2 = fig.add_subplot(grid[0:5, 2:4])
                a3 = fig.add_subplot(grid[0:5, 4:9])

                #Params for the text inside the <> this is a function to highlight text
                highlight_textprops =\
                [{"color": color[0],"fontweight": 'bold'}]

                # Club Logo
                fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.08, bottom=0.95, width=0.2, height=0.1)

                fig.set_facecolor('#181818')

                fig_text(s =f'<{homeTeam}>' + ' ' +  'front attack against' + ' ' + f'<{opponent}>',
                        x = 0.53, y = 1.03, highlight_textprops = highlight_textprops, color='white', fontweight='bold', ha='center' ,fontsize=28);
                            
                if matchDay != 'All Season':
                        fig_text(s = 'MatchDay:' + ' ' + str(matchDay) + ' ' + '| Season 21-22 | @menesesp20',
                                x = 0.45, y = 0.98,
                                color='white', fontweight='bold', ha='center' ,fontsize=11, alpha=0.5);
                elif matchDay == 'All Season':
                        fig_text(s = 'Season 21-22 | @menesesp20',
                                x = 0.38, y = 0.98,
                                color='white', fontweight='bold', ha='center' ,fontsize=11, alpha=0.5);

                fig_text(s = playerName,
                        x = 0.25, y = 0.91, color='white', fontweight='bold', ha='center' ,fontsize=14);

                fig_text(s = playerName2,
                        x = 0.513, y = 0.91, color='white', fontweight='bold', ha='center' ,fontsize=14);

                fig_text(s = playerName3,
                        x = 0.78, y = 0.91, color='white', fontweight='bold', ha='center' ,fontsize=14);

        elif playerName4 != None:
                fig = plt.figure(figsize=(18,12), dpi = 80)
                grid = plt.GridSpec(8, 8)

                a1 = fig.add_subplot(grid[0:5, 0:2])
                a2 = fig.add_subplot(grid[0:5, 2:4])
                a3 = fig.add_subplot(grid[0:5, 4:6])
                a4 = fig.add_subplot(grid[0:5, 6:8])

                #Params for the text inside the <> this is a function to highlight text
                highlight_textprops =\
                [{"color": color[0],"fontweight": 'bold'}]

                # Club Logo
                fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.08, bottom=0.90, width=0.2, height=0.1)

                fig.set_facecolor('#181818')

                fig_text(s =f'<{homeTeam}>' + ' ' +  'front attack against' + ' ' + opponent,
                        x = 0.53, y = 1.03, highlight_textprops = highlight_textprops, color='white', fontweight='bold', ha='center' ,fontsize=28);
                
                if matchDay != 'All Season':
                        fig_text(s = 'MatchDay:' + ' ' + str(matchDay) + ' ' + '| Season 21-22 | @menesesp20',
                                x = 0.45, y = 0.98,
                                color='white', fontweight='bold', ha='center' ,fontsize=11, alpha=0.5);
                elif matchDay == 'All Season':
                        fig_text(s = 'Season 21-22 | @menesesp20',
                                x = 0.38, y = 0.98,
                                color='white', fontweight='bold', ha='center' ,fontsize=11, alpha=0.5);

                fig_text(s = playerName,
                        x = 0.217, y = 0.86, color='white', fontweight='bold', ha='center' ,fontsize=14);

                fig_text(s = playerName2,
                        x = 0.415, y = 0.86, color='white', fontweight='bold', ha='center' ,fontsize=14);

                fig_text(s = playerName3,
                        x = 0.617, y = 0.86, color='white', fontweight='bold', ha='center' ,fontsize=14);

                fig_text(s = playerName4,
                        x = 0.808, y = 0.86, color='white', fontweight='bold', ha='center' ,fontsize=14);

        #################################################################################################################################################
        # 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE 1 FIGURE

        if matchDay == 'All Season':
                df1 = df.loc[(df['name'] == playerName) & (df['isTouch'] == True)]

        if matchDay != 'All Season':
                df1 = df.loc[(df['name'] == playerName) & (df['isTouch'] == True) & (df['Match_ID'] == matchDay)]

        pitch = VerticalPitch(pitch_type='opta',pad_top=0.1, pad_bottom=0.5,
                        pitch_color='#181818', line_color='white', line_zorder=3, linewidth=3, spot_scale=0.00)

        pitch.draw(ax=a1)

        #################################################################################################################################################

        pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                        ['#181818', color[0]], N=10)
        bs = pitch.bin_statistic(df1.x, df1.y, bins=(12, 8))

        convex = df1.loc[(np.abs(stats.zscore(df1[['x','y']])) < 1).all(axis=1)]

        pitch.heatmap(bs, edgecolors='#181818', ax=a1, cmap=pearl_earring_cmap)

        pitch.scatter(df1['x'], df1['y'], ax=a1, edgecolor='white', facecolor='black', alpha=0.3)

        hull = pitch.convexhull(convex['x'], convex['y'])

        pitch.polygon(hull, ax=a1, edgecolor='white', facecolor='white', alpha=0.4, linestyle='--', linewidth=2.5)

        pitch.scatter(x=convex['x'].mean(), y=convex['y'].mean(), ax=a1, c='white', edgecolor=color[0], s=700, zorder=2)


        #################################################################################################################################################
        # 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE 2 FIGURE


        if matchDay == 'All Season':
                df2 = df.loc[(df['name'] == playerName2) & (df['isTouch'] == True)]

        if matchDay != 'All Season':
                df2 = df.loc[(df['name'] == playerName2) & (df['isTouch'] == True) & (df['Match_ID'] == matchDay)]

        pitch = VerticalPitch(pitch_type='opta',pad_top=0.1, pad_bottom=0.5,
                        pitch_color='#181818', line_color='white', line_zorder=3, linewidth=3, spot_scale=0.00)

        pitch.draw(ax=a2)

        #################################################################################################################################################

        pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                        ['#181818', color[0]], N=10)
        bs = pitch.bin_statistic(df2.x, df2.y, bins=(12, 8))

        convex = df2[(np.abs(stats.zscore(df2[['x','y']])) < 1).all(axis=1)]

        pitch.heatmap(bs, edgecolors='#181818', ax=a2, cmap=pearl_earring_cmap)

        pitch.scatter(df2['x'], df2['y'], ax=a2, edgecolor='white', facecolor='black', alpha=0.3)

        hull = pitch.convexhull(convex['x'], convex['y'])

        pitch.polygon(hull, ax=a2, edgecolor='white', facecolor='white', alpha=0.4, linestyle='--', linewidth=2.5)

        pitch.scatter(x=convex['x'].mean(), y=convex['y'].mean(), ax=a2, c='white', edgecolor=color[0], s=700, zorder=2)

        #################################################################################################################################################
        # 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE

        if matchDay == 'All Season':
                df3 = df.loc[(df['name'] == playerName3) & (df['isTouch'] == True)]

        if matchDay != 'All Season':
                df3 = df.loc[(eventsPlayers['name'] == playerName3) & (df['isTouch'] == True) & ((df['Match_ID'] == matchDay))]

        pitch = VerticalPitch(pitch_type='opta',pad_top=0.1, pad_bottom=0.5,
                        pitch_color='#181818', line_color='white', line_zorder=3, linewidth=3, spot_scale=0.00)

        pitch.draw(ax=a3)

        #################################################################################################################################################

        pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                        ['#181818', color[0]], N=10)
        bs = pitch.bin_statistic(df3.x, df3.y, bins=(12, 8))

        convex = df3[(np.abs(stats.zscore(df3[['x','y']])) < 1).all(axis=1)]

        pitch.heatmap(bs, edgecolors='#181818', ax=a3, cmap=pearl_earring_cmap)

        pitch.scatter(df3['x'], df3['y'], ax=a3, edgecolor='white', facecolor='black', alpha=0.3)

        hull = pitch.convexhull(convex['x'], convex['y'])

        pitch.polygon(hull, ax=a3, edgecolor='white', facecolor='white', alpha=0.4, linestyle='--', linewidth=2.5)

        pitch.scatter(x=convex['x'].mean(), y=convex['y'].mean(), ax=a3, c='white', edgecolor=color[0], s=700, zorder=2)

        if playerName4 == None:
                pass
        elif playerName4 != None:

                #################################################################################################################################################
                # 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE 3 FIGURE

                if matchDay == 'All Season':
                        df4 = df.loc[(df['name'] == playerName4) & (df['isTouch'] == True)]

                if matchDay != 'All Season':
                        df4 = df.loc[(eventsPlayers['name'] == playerName4) & (df['isTouch'] == True) & ((df['Match_ID'] == matchDay))]

                pitch = VerticalPitch(pitch_type='opta',pad_top=0.1, pad_bottom=0.5,
                                pitch_color='#181818', line_color='white', line_zorder=3, linewidth=3, spot_scale=0.00)

                pitch.draw(ax=a4)

                #################################################################################################################################################

                pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                                ['#181818', color[0]], N=10)
                bs = pitch.bin_statistic(df4.x, df4.y, bins=(12, 8))

                convex = df4[(np.abs(stats.zscore(df4[['x','y']])) < 1).all(axis=1)]

                pitch.heatmap(bs, edgecolors='#181818', ax=a4, cmap=pearl_earring_cmap)

                pitch.scatter(df4['x'], df4['y'], ax=a4, edgecolor='white', facecolor='black', alpha=0.3)

                hull = pitch.convexhull(convex['x'], convex['y'])

                pitch.polygon(hull, ax=a4, edgecolor='white', facecolor='white', alpha=0.4, linestyle='--', linewidth=2.5)

                pitch.scatter(x=convex['x'].mean(), y=convex['y'].mean(), ax=a4, c='white', edgecolor=color[0], s=700, zorder=2)

def halfspaces_Zone14Player(Game, league, club, matchDay, player=None):

    color = ['#ea04dc', '#181818']
    
    if player != None:
        Game = Game.loc[Game['name'] == player]
    elif player == None:
        Game = Game.loc[Game.team == club]

    halfspaceleft = Game[(Game.endY <= 83) & (Game.endY >= 65) &
                                  (Game.endX >= 78) &
                                  (Game.typedisplayName == 'Pass') &
                                  (Game.Match_ID == matchDay)][['name', 'teamId', 'typedisplayName', 'qualifiers', 'x', 'y', 'endX', 'endY']]

    zone14 = Game[(Game.endX <= 83) & (Game.endX >= 75) &
                          (Game.endY <= 66) & (Game.endY >= 35) &
                          (Game.typedisplayName == 'Pass') &
                          (Game.Match_ID == matchDay)][['name', 'teamId', 'typedisplayName', 'qualifiers', 'x', 'y', 'endX', 'endY']]

    halfspaceright = Game[(Game.endY >= 17) & (Game.endY <= 33) &
                          (Game.endX >= 78) &
                          (Game.typedisplayName == 'Pass') &
                          (Game.Match_ID == matchDay)][['name', 'teamId', 'typedisplayName', 'qualifiers', 'x', 'y', 'endX', 'endY']]

    fig, ax = plt.subplots(figsize=(22,18))

    pitch = VerticalPitch(pitch_type='opta', figsize = (18,16),pad_top=0.1, pad_bottom=0.5,
                    pitch_color='#181818', line_color='white', half=True,
                    constrained_layout=True, tight_layout=True,
                    line_zorder=1, linewidth=5, spot_scale=0.00)

    pitch.draw(ax=ax)

    fig.set_facecolor('#181818')

    ###################################################################################################################################

    fig.suptitle(player, fontsize=50, color='white', fontweight = "bold", y=0.928)

    Title = fig_text(s = 'Half Spaces Zone 14 passes |' + ' ' + str(matchDay) + ' ' + '| @menesesp20',
            x = 0.5, y = 0.87,
            color='white', ha='center', va='center', fontweight = "bold", fontsize=18);

    ###################################################################################################################################

    ZONE14 = patches.Rectangle([20.8, 68], width=58, height=15, linewidth = 2, linestyle='-',
                            edgecolor='white', facecolor='#ff0000', alpha=0.5)

    HalfSpaceLeft = patches.Rectangle([67, 68.05], width=20, height=78, linewidth = 2, linestyle='-',
                            edgecolor='white', facecolor='#2894e5', alpha=0.5)

    HalfSpaceRight = patches.Rectangle([13, 68.05], width=20, height=78, linewidth = 2, linestyle='-',
                            edgecolor='white', facecolor='#2894e5', alpha=0.5,)

    ###################################################################################################################################

    # HALF SPACE LEFT

    pitch.arrows(xstart=halfspaceleft['x'], ystart=halfspaceleft['y'],
                                        xend=halfspaceleft['endX'], yend=halfspaceleft['endY'],
                                        color='#2894e5',
                                        lw=3, zorder=2,
                                        ax=ax)

    ###################################################################################################################################

    # ZONE14

    pitch.arrows(xstart=zone14['x'], ystart=zone14['y'],
                                        xend=zone14['endX'], yend=zone14['endY'],
                                        color='#ff0000',
                                        lw=3, zorder=2,
                                        ax=ax)

    ###################################################################################################################################

    # HALF SPACE RIGHT

    pitch.arrows(xstart=halfspaceright['x'], ystart=halfspaceright['y'],
                                        xend=halfspaceright['endX'], yend=halfspaceright['endY'],
                                        color='#2894e5',
                                        lw=3, zorder=2,
                                        ax=ax)

    ###################################################################################################################################

    ax.add_patch(ZONE14)
    ax.add_patch(HalfSpaceLeft)
    ax.add_patch(HalfSpaceRight)

    ###################################################################################################################################

    # Club Logo
    fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.22, bottom=0.86, width=0.2, height=0.08)


def deep_Progression(df, player, radiusN, club, matchDay):

  color = ['#ea04dc', '#181818']

  df = df.loc[df.Match_ID == matchDay]

  sucess = df[(df['typedisplayName'] == 'Pass') & (df['outcomeTypedisplayName'] == 'Successful') & (df['x'] != 99.5)]

  insucess = df[(df['typedisplayName'] == 'Pass') & (df['outcomeTypedisplayName'] == 'Unsuccessful') & (df['x'] != 99.5)]

  Passes = pd.concat([sucess, insucess], axis=0, ignore_index=True)[['name', 'team', 'x', 'y', 'endX', 'endY', 'outcomeTypedisplayName', 'Match_ID']]

  radius = radiusN

  Passes['initialDistancefromgoal'] = np.sqrt(((100 - Passes['x'])**2) + ((50 - Passes['y'])**2))

  Passes['finalDistancefromgoal'] = np.sqrt(((100 - Passes['endX'])**2) + ((50 - Passes['endY'])**2))

  Passes['deepCompletion'] = np.where(((Passes['finalDistancefromgoal'] <= radius) & (Passes['initialDistancefromgoal'] >= radius)), 'True', 'False')

  deepcompletion =  Passes.loc[(((Passes['deepCompletion']=='True') & (Passes['outcomeTypedisplayName']!='Unsuccessful')))]

  pitchColor = "#1e1e1e"
  lineColor = "white"
  passColor = color[0]
  
  #Plotting the pitch

  pitch = VerticalPitch(pitch_type='opta', pad_top=0.1, pad_bottom=0.5,
                    pitch_color=pitchColor, line_color=lineColor,half = True,
                    line_zorder=1, linewidth=5, spot_scale=0.00)

  fig, ax = pitch.grid(nrows=1, ncols=1, figheight=55,
                        endnote_height=0.0, endnote_space=0, axis=False,
                        title_height=0.13, grid_height=0.86, space=0.11)

  fig.set_facecolor(pitchColor)

  #Title of our plot

  fig.suptitle("Deep Progression", fontweight='bold', fontsize=150, color='white', y=0.98)

  highlight_textprops =\
      [{"color": color[0],"fontweight": 'bold'}
      ]


  Title = fig_text(s = 'A <Completed pass> ends in the highlighted zone' + ' ' + '|' + 'MatchDay' + ' ' + str(matchDay) + ' ' + '| Season 21-22 | @Menesesp20',
          x = 0.5, y = 0.935, highlight_textprops = highlight_textprops,
          fontweight='bold', ha='center', va='center', fontsize=70, color='white');

  #The plotting of the area of focus for our plot. This is one of the aesthetic element that if you don't like you can ignore.
  #We will be drawing a semicircle centered at the mid-point of the goal with a diameter equal to the width of the penalty box.
  #The important stylistic arguments here are linestyle, I have gone with a dashed line instead of a solid one, more on this
  #can be found out in Matplotlib docs which I highly recommend you check out.

  #Zorder is basically layering different elements of our viz on top of one another, so we want our semi-circle to be plotted
  #as the third layer from the bottom. 

  circle = patches.Circle([50,100],radius = radius , linewidth = 7, linestyle='--',
                    edgecolor='white', facecolor='none', alpha=0.9, zorder=3 )

  ax['pitch'].add_patch(circle)


  #Defining out plotting function
  df = deepcompletion[(deepcompletion['name'] == player)]

  ax['pitch'].set_title(player , fontsize=75, color=lineColor, fontweight = 'bold', va="center", ha="center", pad=60)
      
  #Plotting the passes. The scatter point at the end of the the lines is a stylistic choice and you can do it without it.
  #The syntax is very intuitive and you can control various parameters of the lines by controlling different arguments.
      
  pitch.lines(df['x'], df['y'], df['endX'], df['endY'],
              ax=ax['pitch'], comet = True, color= passColor, lw=10, alpha = 0.7)

  pitch.scatter(df['endX'], df['endY'], edgecolors= passColor, c=pitchColor,
                s = 500, zorder=4, ax=ax['pitch'], marker = 'o', alpha = 0.9,linewidths=5)