import pandas as pd
import numpy as np

import sys

import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

import mplsoccer

import seaborn as sns
import matplotlib as mpl

from highlight_text import ax_text,fig_text

from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

from soccerplots.radar_chart import Radar
from soccerplots.utils import add_image

from matplotlib import font_manager

font_path = 'Fonts/Gagalin-Regular.otf'
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

#Courier New

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()

#############################################################################################################################################################

sys.path.append('Functions')
sys.path.append('Data/Teams')


#############################################################################################################################################################

import matplotlib.pyplot as plt


#############################################################################################################################################################

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
              'Liverpool' : ['#d40424', '#e2e1ab'],
              'PSG' : ['#043c70', '#c63230'],
              'RB Leipzig' : ['#ff0000', 'white'],
              'River Plate' : ['#ff0000', 'black'],
              'Boca Juniores' : ['yellow', 'blue']}
              
def radar_chart_compare(df, player, player2, cols):

  #Obtenção dos dois jogadores que pretendemos
  pl1 = df[(df['Player'] == player)]

  position = pl1['Position'].unique()
  position = position.tolist()
  position = position[0]

  val1 = pl1[cols].values[0]

  club = pl1['Team'].values[0]
  league = pl1['Comp'].values[0]

  #Obtenção dos dois jogadores que pretendemos
  pl2 = df[(df['Player'] == player2)]
  val2 = pl2[cols].values[0]

  position2 = pl2['Position'].unique()
  position2 = position2.tolist()
  position2 = position2[0]

  club2 = pl2['Team'].values[0]
  league2 = pl2['Comp'].values[0]


  df = df.loc[(df.Position == position)| (df.Position == position2)]

  #Obtenção dos valores das colunas que pretendemos colocar no radar chart, não precisamos aceder ao index porque só iriamos aceder aos valores de um dos jogadores
  values = [val1, val2]

  #Obtençaõ dos valores min e max das colunas selecionadas
  ranges = [(df[col].min(), df[col].max()) for col in cols] 

  #Atribuição dos valores aos titulos e respetivos tamanhos e cores
  title = dict(
      #Jogador 1
      title_name = player,
      title_color = '#ea04dc',
      
      #Jogador 2
      title_name_2 = player2,
      title_color_2 = '#2d92df',

      #Tamnhos gerais do radar chart
      title_fontsize = 20,
      subtitle_fontsize = 15
  )

  #team_player = df[col_name_team].to_list()

  #dict_team ={'Dortmund':['#ffe011', '#000000'],
              #'Nice':['#cc0000', '#000000'],
              #'Nice':['#cc0000', '#000000']}

  #color = dict_team.get(team_player[0])

  ## endnote 
  endnote = "Visualization made by: Pedro Meneses(@menesesp20)"

  #Criação do radar chart
  fig, ax = plt.subplots(figsize=(18,15), dpi=200)
  radar = Radar(background_color="#E8E8E8", patch_color="#181818", range_color="#181818", label_color="#181818", label_fontsize=10, range_fontsize=11)
  fig, ax = radar.plot_radar(ranges=ranges, 
                             params=cols, 
                             values=values, 
                             radar_color=['#ea04dc','#2d92df'], 
                             figax=(fig, ax), 
                             image='Images/Clubs/' + league + '/' + club + '.png', 
                             image_coord=[0.40, 0.81, 0.1, 0.075],
                             title=title,
                             endnote=endnote, end_size=0, end_color="#1b1b1b",
                             compare=True)
  
  fig.set_facecolor('#E8E8E8')

  fig = add_image(image='Images/Clubs/' + league2 + '/' + club2 + '.png', fig=fig, left=0.53, bottom=0.81, width=0.1, height=0.075)
  fig = add_image(image='Images/Players/' + league + '/' + club + '/' + player + '.png', fig=fig, left=0.20, bottom=0.75, width=0.2, height=0.1)
  fig = add_image(image='Images/Players/' + league2 + '/' + club2 + '/' + player2 + '.png', fig=fig, left=0.68, bottom=0.75, width=0.2, height=0.1)



#Automatização da criação do gráfico radar chart de 1 ou vários jogadores, parametros pre estabelecidos tem de vir no fim dos parametros
def radar_chart(df, player, cols, league, club, player2=None):

  from soccerplots.radar_chart import Radar

  if player2 == None:
    #Atribuição do jogador a colocar no gráfico
    players = df[df['Player'] == player]
    #Valores que pretendemos visualizar no radar chart, acedemos ao index 0 para obtermos os valores dentro da lista correta
    values = players[cols].values[0]
    #Obtenção do alcance minimo e máximo dos valores
    ranges = [(df[col].min(), df[col].max()) for col in cols]

    color = ['#ea04dc','#2d92df']
    #Atribuição dos valores aos titulos e respetivos tamanhos e cores
    title = dict(
      title_name = player,
      title_color = color[0],
      title_fontsize = 25,
    )

    #team_player = df[col_name_team].to_list()

    #dict_team ={'Dortmund':['#ffe011', '#000000'],
              #'Nice':['#cc0000', '#000000'],}

    #color = dict_team.get(team_player[0])

    ## endnote 
    endnote = "Visualization made by: Pedro Meneses(@menesesp20)"

    #Criação do radar chart
    fig, ax = plt.subplots(figsize=(18,15))
    radar = Radar(background_color="#E8E8E8", patch_color="#181818", range_color="#181818", label_color="#181818", label_fontsize=10, range_fontsize=11)
    fig, ax = radar.plot_radar(ranges=ranges, 
                               params=cols, 
                               values=values, 
                               radar_color=color,
                               figax=(fig, ax), 
                               image='Images/Clubs/' + league + '/' + club + '.png', 
                               image_coord=[0.464, 0.81, 0.1, 0.075],
                               title=title,
                               endnote=endnote)

    fig.set_facecolor('#E8E8E8')

    fig = add_image(image='Images/Players/' + league + '/' + club + '/' + player + '.png', fig=fig, left=0.20, bottom=0.75, width=0.2, height=0.1)

  else:
    radar_chart_compare(df, player, player2, 'Player', 'Team', cols, league)


#Radar Clubs

def radar_chart_compare_clubs(df, club, club2, col_name_club, cols, league):

  color = clubColors.get(club)

  #Obtenção dos dois jogadores que pretendemos
  pl1 = df[(df[col_name_club] == club)]
  val1 = pl1[cols].values[0]

  #Obtenção dos dois jogadores que pretendemos
  pl2 = df[(df[col_name_club] == club2)]
  val2 = pl2[cols].values[0]


  #Obtenção dos valores das colunas que pretendemos colocar no radar chart, não precisamos aceder ao index porque só iriamos aceder aos valores de um dos jogadores
  values = [val1, val2]

  #Obtençaõ dos valores min e max das colunas selecionadas
  ranges = [(df[col].min(), df[col].max()) for col in cols] 

  #Atribuição dos valores aos titulos e respetivos tamanhos e cores
  title = dict(
      #Jogador 1
      title_name = club,
      title_color = color[0],
      
      #Jogador 2
      title_name_2 = club2,
      title_color_2 = color[0],

      #Tamnhos gerais do radar chart
      title_fontsize = 20,
      subtitle_fontsize = 15
  )

  #team_club = df[col_name_club].to_list()

  #dict_team ={'Dortmund':['#ffe011', '#000000'],
              #'Nice':['#cc0000', '#000000'],
              #'Nice':['#cc0000', '#000000']}

  #color = dict_team.get(team_club[0])

  ## endnote 
  endnote = "Visualization made by: Pedro Meneses(@menesesp20)"

  #Criação do radar chart
  fig, ax = plt.subplots(figsize=(18,15))

  fig.set_facecolor('#181818')

  radar = Radar(background_color="#181818", patch_color="#eb00e5", range_color="white", label_color="white", label_fontsize=20, range_fontsize=12)
  fig, ax = radar.plot_radar(ranges=ranges, 
                             params=cols, 
                             values=values, 
                             radar_color=color, 
                             figax=(fig, ax),
                             title=title,
                             endnote=endnote, 
                             compare=True)
  
  fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.20, bottom=0.75, width=0.2, height=0.1)
  fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.68, bottom=0.75, width=0.2, height=0.1)

#Automatização da criação do gráfico radar chart de 1 ou vários jogadores, parametros pre estabelecidos tem de vir no fim dos parametros
def radar_chart_clubs(df, club, col_name_club, cols, league, game_phase, club2=None):

  color = clubColors.get(club)

  if club2 == None:
    #Atribuição do jogador a colocar no gráfico
    clubs = df[df[col_name_club] == club]
    #Valores que pretendemos visualizar no radar chart, acedemos ao index 0 para obtermos os valores dentro da lista correta
    values = clubs[cols].values[0]
    #Obtenção do alcance minimo e máximo dos valores
    ranges = [(df[col].min(), df[col].max()) for col in cols]

    #Atribuição dos valores aos titulos e respetivos tamanhos e cores
    title = dict(
      title_name = club + ' ' + game_phase,
      title_color = color[0],
      title_fontsize = 25,
    )

    #team_player = df[col_name_team].to_list()

    #dict_team ={'Dortmund':['#ffe011', '#000000'],
              #'Nice':['#cc0000', '#000000'],}

    #color = dict_team.get(team_player[0])

    ## endnote 
    endnote = "Visualization made by: Pedro Meneses(@menesesp20)"

    #Criação do radar chart
    fig, ax = plt.subplots(figsize=(18,15))

    fig.set_facecolor('#181818')

    radar = Radar(background_color="#181818", patch_color="#eb00e5", range_color="white", label_color="white", label_fontsize=20, range_fontsize=12)
    fig, ax = radar.plot_radar(ranges=ranges, 
                               params=cols, 
                               values=values, 
                               radar_color=color,
                               figax=(fig, ax),
                               title=title,
                               endnote=endnote)
    
    fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.20, bottom=0.75, width=0.2, height=0.1)

  else:
    radar_chart_compare_clubs(df, club, club2, col_name_club, cols)