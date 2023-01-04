import pandas as pd
import numpy as np
import sys

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import matplotlib as mpl

import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

from mplsoccer import Pitch, PyPizza, add_image

from highlight_text import  ax_text, fig_text

from soccerplots.utils import add_image
from soccerplots.radar_chart import Radar

from scipy import stats

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import math

from pandas.core.common import SettingWithCopyWarning

import warnings
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

from matplotlib import font_manager

font_path = 'Fonts/Gagalin-Regular.otf'
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

#Courier New

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()

plt.rcParams["figure.dpi"] = 300

sys.path.append('Functions')

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

offensive_Midfield_BS = ['Successful dribbles %', 'xA/90', 'Deep completions/90', 'Passes to penalty area/90',
                      'Key passes/90', 'Passes final 1/3 %']

Winger = ['Successful dribbles %', 'Goals', 'xG/90',
          'xA/90', 'Touches in box/90', 'Dribbles/90', 'Passes to penalty area/90', 'Key passes/90',
          'Progressive runs/90', 'Crosses/90', 'Deep completed crosses/90',
          'Offensive duels/90', 'PAdj Interceptions']

Forward = ['Goals', 'xG/90', 'Shots on target, %', 'Goal conversion, %',
           'Successful dribbles %', 'xA/90', 'Touches in box/90', 'Dribbles/90',
           'Offensive duels/90', 'PAdj Interceptions', 'Aerial duels/90', 'Aerial duels %']


clubs = ['Goals/90', 'xG/90', 'Dribbles', 'Touches in box',  'Deep completions', 'Deep completed crosses', 'Clean sheets']

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
              'Athletic Bilbao' : ['#ff0000', '#e8e8e8'],
              'Real Madrid' : ['#1a346e', '#e8e8e8'],
              'FC Barcelona' : ['#c2043a', '#06274c'],
              'Deportivo Alavés' : ['#062494', '#e8e8e8'],
              'Elche' : ['#076235', '#e8e8e8'],
              'Mallorca' : ['#ff0000', '#f9e006'],
              'Valladolid' : ['#5b2482', '#e8e8e8'],
              'Almeria' : ['#ff0000', '#e8e8e8'],
              'Cadiz' : ['#f9e310', '#0045a8'],
              'Manchester City' : ['#7bb1d8', '#062e63'],
              'Manchester United' : ['#ff0000', '#e8e8e8'],
              'Liverpool' : ['#d40424', '#e2e1ab'],
              'Norwich City' : ['#00a650', '#fff200'],
              ###################################
              'Corinthians' : ['#ff0000', '#e8e8e8'],
              'Avai' : ['#00679a', '#e8e8e8'],
              'Flamengo' : ['#ff0000', '#1b1b1b'],
              'Palmeiras' : ['#046434', '#e8e8e8'],
              ###################################
              'PSG' : ['#043c70', '#c63230'],
              ###################################
              'River Plate' : ['#ff0000', '#1b1b1b'],
              'Racing Club' : ['#ff0000', '#1b1b1b'],
              'Stuttgard' : ['#ff0000', '#1b1b1b'],
              'Benfica' : ['#ff0000', '#e8e8e8'],
              'Porto' : ['#356ea1', '#e8e8e8']}


def rank(df):
    for col in df.columns:
      df['rank_' + col] = df[col].rank(pct=True)


def rating(df):
    df.rename({'Defensive duels won, %': 'Defensive duels %',
                    'Aerial duels won, %': 'Aerial duels %', 'Accurate passes to penalty area, %' : 'Passes penalty area %',
                    'Accurate passes to final third, %' : 'Passes final 1/3 %', 'Successful dribbles, %' : 'Successful dribbles %',
                    'Successful defensive actions/90' : 'Succ defensive actions/90',
                    'Accurate forward passes, %': 'Forward passes %', 'Accurate passes, %' : 'Passes %', 'Offensive duels won, %' : 'Offensive duels %'}, axis=1, inplace=True)

    center_Back = ['Non-penalty goals/90', 'Offensive duels %', 'Progressive runs/90',
                'PAdj Interceptions', 'PAdj Sliding tackles', 'Defensive duels/90', 'Defensive duels %',
                'Aerial duels/90', 'Aerial duels %', 'Shots blocked/90',
                'Passes %', 'Forward passes %', 'Forward passes/90', 'Progressive passes/90']

    full_Back = ['Successful dribbles %', 'Offensive duels %', 'Touches in box/90', 'Progressive runs/90', 'Crosses/90', 'Deep completed crosses/90',
                'PAdj Sliding tackles', 'PAdj Interceptions', 'Defensive duels %', 'Aerial duels/90', 'Aerial duels %',
                'Passes %', 'Deep completions/90', 'Progressive passes/90', 'Key passes/90', 'Third assists/90']

    Midfield  = ['xG/90', 'Shots', 'Progressive runs/90', 'Successful dribbles %', 'PAdj Interceptions', 'Aerial duels %', 'Defensive duels %', 
                'Passes %', 'Forward passes %', 'Forward passes/90', 'Progressive passes/90',
                'Key passes/90', 'Second assists/90', 'Assists', 'xA']

    offensive_Midfield = ['xG/90', 'Goals/90', 'Progressive runs/90', 'Successful dribbles %',
                        'Succ defensive actions/90', 'PAdj Interceptions', 'Aerial duels %', 'Defensive duels %',
                        'xA/90', 'Deep completions/90', 'Passes to penalty area/90',
                        'Touches in box/90', 'Key passes/90', 'Passes final 1/3 %',
                        'Passes penalty area %', 'Progressive passes/90']

    Forward = ['Goals', 'xG/90', 'Shots on target, %', 'Goal conversion, %',
            'Offensive duels/90', 'PAdj Interceptions', 'Aerial duels/90', 'Aerial duels %',
            'Successful dribbles %', 'xA/90', 'Touches in box/90', 'Dribbles/90']





    df['offensive_CB'] = df[['rank_Non-penalty goals/90', 'rank_Offensive duels %', 'rank_Progressive runs/90']].mean(axis=1)

    df['tecnica_CB'] = df[['rank_Passes %', 'rank_Forward passes %', 'rank_Forward passes/90', 'rank_Progressive passes/90']].mean(axis=1)

    df['defense_CB'] = df[['rank_PAdj Interceptions', 'rank_PAdj Sliding tackles', 'rank_Defensive duels/90', 'rank_Defensive duels %',
                                    'rank_Aerial duels/90', 'rank_Aerial duels %', 'rank_Shots blocked/90']].mean(axis=1)           

    df['rating_CB'] = ((df['offensive_CB'] * 20) + (df['defense_CB'] * 60) + (df['tecnica_CB'] * 20)) / 10





    df['offensive_FB'] = df[['rank_Successful dribbles %', 'rank_Offensive duels %', 'rank_Touches in box/90',
                                    'rank_Progressive runs/90', 'rank_Crosses/90', 'rank_Deep completed crosses/90']].mean(axis=1)

    df['tecnica_FB'] = df[['rank_Passes %', 'rank_Deep completions/90', 'rank_Progressive passes/90', 'rank_Key passes/90', 'rank_Third assists/90']].mean(axis=1)

    df['defense_FB'] = df[['rank_PAdj Sliding tackles', 'rank_PAdj Interceptions', 'rank_Defensive duels %',
                                    'rank_Aerial duels/90', 'rank_Aerial duels %']].mean(axis=1)           

    df['rating_FB'] = ((df['offensive_FB'] * 25) + (df['defense_FB'] * 50) + (df['tecnica_FB'] * 25)) / 10






    df['offensive_MF'] = df[['rank_xG/90', 'rank_Assists', 'rank_xA']].mean(axis=1)

    df['tecnica_MF'] = df[['rank_Passes %', 'rank_Forward passes %', 'rank_Forward passes/90', 'rank_Progressive runs/90',
                'rank_Progressive passes/90', 'rank_Key passes/90', 'rank_Second assists/90', 'rank_Successful dribbles %']].mean(axis=1)

    df['defense_MF'] = df[['rank_PAdj Interceptions', 'rank_Aerial duels %', 'rank_Defensive duels %']].mean(axis=1)           

    df['rating_MF'] = ((df['offensive_MF'] * 20) + (df['defense_MF'] * 20) + (df['tecnica_MF'] * 60)) / 10




    df['offensive_OMF'] = df[['rank_xG/90', 'rank_Goals/90', 'rank_Progressive runs/90', 'rank_Successful dribbles %']].mean(axis=1)

    df['tecnica_OMF'] = df[['rank_Passes %', 'rank_xA/90', 'rank_Deep completions/90', 'rank_Passes to penalty area/90',
                'rank_Progressive passes/90', 'rank_Key passes/90', 'rank_Touches in box/90', 'rank_Passes final 1/3 %', 'rank_Passes penalty area %']].mean(axis=1)

    df['defense_OMF'] = df[['rank_PAdj Interceptions', 'rank_Aerial duels %', 'rank_Defensive duels %', 'rank_Succ defensive actions/90']].mean(axis=1)           

    df['rating_OMF'] = ((df['offensive_OMF'] * 30) + (df['defense_OMF'] * 10) + (df['tecnica_OMF'] * 60)) / 10





    df['offensive_FW'] = df[['rank_Goals', 'rank_xG/90', 'rank_Shots on target, %', 'rank_Goal conversion, %']].mean(axis=1)

    df['tecnica_FW'] = df[['rank_Successful dribbles %', 'rank_xA/90', 'rank_Touches in box/90', 'rank_Dribbles/90']].mean(axis=1)

    df['defense_FW'] = df[['rank_Offensive duels/90', 'rank_PAdj Interceptions', 'rank_Aerial duels/90', 'rank_Aerial duels %']].mean(axis=1)           

    df['rating_FW'] = ((df['offensive_FW'] * 40) + (df['defense_FW'] * 20) + (df['tecnica_FW'] * 40)) / 10


def playerRole(df):

    defensive = ['Defensive duels/90', 'Defensive duels %']

    Aerial = ['Aerial duels/90', 'Aerial duels %']

    positioning = ['Shots blocked/90', 'PAdj Interceptions']

    progressiveRuns = ['Progressive runs/90', 'Accelerations/90']

    ballPlaying = ['Passes %', 'Forward passes %', 'Forward passes/90', 'Progressive passes/90', 'Accurate progressive passes, %']

    attackingThreat = ['xG/90', 'Goals/90', 'Head goals/90', 'Shots/90']


    df['Defensive Ability'] = ((df['rank_Defensive duels/90'] * 35) + (df[ 'rank_Defensive duels %'] * 65)) / 10

    ##########################################################################################################################################################################

    df['Aerial'] = ((df['rank_Aerial duels/90'] * 35) + (df[ 'rank_Aerial duels %'] * 65)) / 10

    ##########################################################################################################################################################################

    df['positioning'] = ((df['rank_Shots blocked/90'] * 50) + (df[ 'rank_PAdj Interceptions'] * 50)) / 10

    ##########################################################################################################################################################################

    df['progressiveRuns'] = ((df['rank_Progressive runs/90'] * 70) + (df[ 'rank_Accelerations/90'] * 30)) / 10

    ##########################################################################################################################################################################

    df['ballPlaying'] = ((df['rank_Passes %'] * 20) + (df[ 'rank_Forward passes %'] * 15) +
                            (df[ 'rank_Forward passes/90'] * 25) + (df[ 'rank_Progressive passes/90'] * 25) +
                            (df[ 'rank_Accurate progressive passes, %'] * 15)) / 10

    ##########################################################################################################################################################################

    df['attackingThreat'] = ((df['rank_xG/90'] * 40) + (df[ 'rank_Goals/90'] * 15) +
                                (df[ 'rank_Head goals/90'] * 30) + (df[ 'rank_Shots/90'] * 15)) / 10

    ##########################################################################################################################################################################

    df['Stopper'] = round(((df['Defensive Ability'] * 27.5) + (df[ 'positioning'] * 37.5) + (df[ 'Aerial'] * 20) +
                            (df[ 'ballPlaying'] * 5) + (df[ 'progressiveRuns'] * 5) + (df[ 'attackingThreat'] * 5)) / 10, )

    ##########################################################################################################################################################################

    df['Aerial CB'] =  round(((df['Defensive Ability'] * 20) + (df[ 'positioning'] * 20) + (df[ 'Aerial'] * 35) +
                            (df[ 'ballPlaying'] * 10) + (df[ 'progressiveRuns'] * 10) + (df[ 'attackingThreat'] * 5)) / 10, 2)

    ##########################################################################################################################################################################

    df['Ball Playing CB'] =  round(((df['Defensive Ability'] * 20) + (df[ 'positioning'] * 15) + (df[ 'Aerial'] * 10) +
                            (df[ 'ballPlaying'] * 30) + (df[ 'progressiveRuns'] * 15) + (df[ 'attackingThreat'] * 10)) / 10, 2)

    ##########################################################################################################################################################################

    df['Ball Carrying CB'] =  round(((df['Defensive Ability'] * 20) + (df[ 'positioning'] * 15) + (df[ 'Aerial'] * 10) +
                            (df[ 'ballPlaying'] * 15) + (df[ 'progressiveRuns'] * 30) + (df[ 'attackingThreat'] * 10)) / 10, 2)


    ##########################################################################################################################################################################

    crossing = ['Crosses/90', 'Accurate crosses, %']

    ##########################################################################################################################################################################

    dribbles = ['Dribbles/90', 'Successful dribbles %']

    ##########################################################################################################################################################################

    defending1v1 = ['Defensive duels/90', 'Defensive duels %']

    ##########################################################################################################################################################################

    positioning = ['Shots blocked/90', 'PAdj Interceptions']

    ##########################################################################################################################################################################

    progressiveRuns = ['Progressive runs/90', 'Accelerations/90', 'Dribbles/90']

    ##########################################################################################################################################################################

    decisionMake = ['Shot assists/90', 'Passes penalty area %', 'Shots/90',
                    'Passes to penalty area/90', 'xA/90', 'Shots on target, %', 'Assists/90']

    ##########################################################################################################################################################################

    touchQuality = ['Key passes/90', 'Accurate smart passes, %', 'Smart passes/90', 'Fouls suffered/90']

    ##########################################################################################################################################################################

    df['crossing'] = ((df['rank_Crosses/90'] * 65) + (df[ 'rank_Accurate crosses, %'] * 35)) / 10

    ##########################################################################################################################################################################

    df['dribbles'] = ((df['rank_Dribbles/90'] * 65) + (df[ 'rank_Successful dribbles %'] * 35)) / 10

    ##########################################################################################################################################################################

    df['defending1v1'] = ((df['rank_Defensive duels/90'] * 35) + (df[ 'rank_PAdj Interceptions'] * 65)) / 10

    ##########################################################################################################################################################################

    df['positioning'] = ((df['rank_Shots blocked/90'] * 50) + (df[ 'rank_PAdj Interceptions'] * 50)) / 10

    ##########################################################################################################################################################################

    df['progressiveRuns'] = ((df['rank_Progressive runs/90'] * 50) + (df[ 'rank_Accelerations/90'] * 20) +
                                (df[ 'rank_Dribbles/90'] * 30)) / 10

    ##########################################################################################################################################################################

    df['decisionMake'] = ((df['rank_Shot assists/90'] * 20) + (df[ 'rank_Passes penalty area %'] * 20) +
                                (df[ 'rank_Assists/90'] * 15) + (df[ 'rank_Shots on target, %'] * 15) + (df[ 'rank_Assists/90'] * 15) +
                                (df[ 'rank_xA/90'] * 10) + (df[ 'rank_Passes to penalty area/90'] * 10) + (df[ 'rank_Shots/90'] * 10)) / 10

    ##########################################################################################################################################################################

    df['touchQuality'] = ((df['rank_Key passes/90'] * 30) + (df[ 'rank_Accurate smart passes, %'] * 25) +
                                (df[ 'rank_Smart passes/90'] * 25) + (df[ 'rank_Fouls suffered/90'] * 20)) / 10

    ##########################################################################################################################################################################

    df['Attacking FB'] =  round(((df['crossing'] * 10) + (df[ 'dribbles'] * 20) + (df[ 'defending1v1'] * 5) +
                            (df[ 'positioning'] * 10) + (df[ 'progressiveRuns'] * 25) + (df[ 'decisionMake'] * 15) + (df[ 'touchQuality'] * 15)) / 10, 2)

    ##########################################################################################################################################################################

    df['Wing Back'] =  round(((df['crossing'] * 20) + (df[ 'dribbles'] * 10) + (df[ 'defending1v1'] * 10) +
                            (df[ 'positioning'] * 15) + (df[ 'progressiveRuns'] * 20) + (df[ 'decisionMake'] * 15) + (df[ 'touchQuality'] * 10)) / 10, 2)

    ##########################################################################################################################################################################

    df['Inverted Wing Back'] =  round(((df['crossing'] * 10) + (df[ 'dribbles'] * 15) + (df[ 'defending1v1'] * 10) +
                            (df[ 'positioning'] * 10) + (df[ 'progressiveRuns'] * 15) + (df[ 'decisionMake'] * 20) + (df[ 'touchQuality'] * 20)) / 10, 2)

    ##########################################################################################################################################################################

    df['Defensive FB'] =  round(((df['crossing'] * 15) + (df[ 'dribbles'] * 10) + (df[ 'defending1v1'] * 25) +
                            (df[ 'positioning'] * 15) + (df[ 'progressiveRuns'] * 10) + (df[ 'decisionMake'] * 10) + (df[ 'touchQuality'] * 15)) / 10, 2)

    ##########################################################################################################################################################################
    ##########################################################################################################################################################################

    df['Aerial'] = ((df['rank_Aerial duels/90'] * 35) + (df[ 'rank_Aerial duels %'] * 65)) / 10

    ##########################################################################################################################################################################

    df['ballPlaying'] = ((df['rank_Passes %'] * 20) + (df[ 'rank_Forward passes %'] * 15) +
                            (df[ 'rank_Forward passes/90'] * 25) + (df[ 'rank_Progressive passes/90'] * 25) +
                            (df[ 'rank_Accurate progressive passes, %'] * 15)) / 10

    ##########################################################################################################################################################################

    df['dribbles'] = ((df['rank_Dribbles/90'] * 65) + (df[ 'rank_Successful dribbles %'] * 35)) / 10

    ##########################################################################################################################################################################

    df['defending1v1'] = ((df['rank_Defensive duels/90'] * 35) + (df[ 'rank_PAdj Interceptions'] * 65)) / 10

    ##########################################################################################################################################################################

    df['positioning'] = ((df['rank_Shots blocked/90'] * 50) + (df[ 'rank_PAdj Interceptions'] * 50)) / 10

    ##########################################################################################################################################################################

    df['progressiveRuns'] = ((df['rank_Progressive runs/90'] * 50) + (df[ 'rank_Accelerations/90'] * 20) +
                                (df[ 'rank_Dribbles/90'] * 30)) / 10

    ##########################################################################################################################################################################

    df['decisionMake'] = ((df['rank_Shot assists/90'] * 20) + (df[ 'rank_Passes penalty area %'] * 20) +
                            (df[ 'rank_Assists/90'] * 15) + (df[ 'rank_Shots on target, %'] * 15) + (df[ 'rank_Assists/90'] * 15) +
                            (df[ 'rank_xA/90'] * 10) + (df[ 'rank_Passes to penalty area/90'] * 10) + (df[ 'rank_Shots/90'] * 10)) / 10

    ##########################################################################################################################################################################

    df['touchQuality'] = ((df['rank_Key passes/90'] * 30) + (df[ 'rank_Accurate smart passes, %'] * 25) +
                            (df[ 'rank_Smart passes/90'] * 25) + (df[ 'rank_Fouls suffered/90'] * 20)) / 10


    ##########################################################################################################################################################################
    ##########################################################################################################################################################################

    df['Ball Winner'] =  round(((df['positioning'] * 25) + (df[ 'defending1v1'] * 30) +
                                (df[ 'touchQuality'] * 12) + (df[ 'dribbles'] * 10) + (df[ 'ballPlaying'] * 11) +
                                (df[ 'Aerial'] * 12)) / 10, 2)

    ##########################################################################################################################################################################

    df['Deep Lying Playmaker'] =  round(((df['positioning'] * 15) + (df[ 'progressiveRuns'] * 16) +
                                    (df[ 'decisionMake'] * 17) + (df[ 'touchQuality'] * 14) + (df[ 'dribbles'] * 10) + (df[ 'ballPlaying'] * 28)) / 10, 2)

    ##########################################################################################################################################################################

    df['Attacking Playmaker'] =  round(((df['positioning'] * 10) + (df[ 'progressiveRuns'] * 14) +
                                    (df[ 'decisionMake'] * 25.5) + (df[ 'touchQuality'] * 14) + (df[ 'dribbles'] * 22.5) + (df[ 'ballPlaying'] * 14)) / 10, 2)

    ##########################################################################################################################################################################

    df['Box-to-box'] =  round(((df[ 'defending1v1'] * 15) + (df[ 'progressiveRuns'] * 28) +
                                    (df[ 'decisionMake'] * 10) + (df[ 'touchQuality'] * 10) + (df[ 'dribbles'] * 15) + (df[ 'ballPlaying'] * 11) +
                                    (df[ 'Aerial'] * 11)) / 10, 2)

    ##########################################################################################################################################################################

    goal = ['Goal conversion, %']

    df['Aerial'] = ((df['rank_Aerial duels/90'] * 35) + (df[ 'rank_Aerial duels %'] * 65)) / 10

    ##########################################################################################################################################################################

    df['ballPlaying'] = ((df['rank_Passes %'] * 20) + (df[ 'rank_Forward passes %'] * 15) +
                            (df[ 'rank_Forward passes/90'] * 25) + (df[ 'rank_Progressive passes/90'] * 25) +
                            (df[ 'rank_Accurate progressive passes, %'] * 15)) / 10

    ##########################################################################################################################################################################

    df['dribbles'] = ((df['rank_Dribbles/90'] * 65) + (df[ 'rank_Successful dribbles %'] * 35)) / 10

    ##########################################################################################################################################################################

    df['progressiveRuns'] = ((df['rank_Progressive runs/90'] * 50) + (df[ 'rank_Accelerations/90'] * 20) +
                                (df[ 'rank_Dribbles/90'] * 30)) / 10

    ##########################################################################################################################################################################

    df['decisionMake'] = ((df['rank_Shot assists/90'] * 20) + (df[ 'rank_Passes penalty area %'] * 20) +
                            (df[ 'rank_Assists/90'] * 15) + (df[ 'rank_Shots on target, %'] * 15) + (df[ 'rank_Assists/90'] * 15) +
                            (df[ 'rank_xA/90'] * 10) + (df[ 'rank_Passes to penalty area/90'] * 10) + (df[ 'rank_Shots/90'] * 10)) / 10

    ##########################################################################################################################################################################

    df['touchQuality'] = ((df['rank_Key passes/90'] * 30) + (df[ 'rank_Accurate smart passes, %'] * 25) +
                            (df[ 'rank_Smart passes/90'] * 25) + (df[ 'rank_Fouls suffered/90'] * 20)) / 10

    ##########################################################################################################################################################################

    df['attackingThreat'] = ((df['rank_xG/90'] * 25) + (df[ 'rank_Goals/90'] * 25) +
                                (df[ 'rank_Head goals/90'] * 12) + (df[ 'rank_Shots/90'] * 12) + (df[ 'rank_Shots on target, %'] * 14) +
                                (df[ 'rank_Goal conversion, %'] * 12)) / 10

    ##########################################################################################################################################################################
    ##########################################################################################################################################################################

    df['False 9'] =  round(((df[ 'progressiveRuns'] * 15) + (df[ 'decisionMake'] * 20) +
                        (df[ 'touchQuality'] * 20) + (df[ 'dribbles'] * 15) + (df[ 'ballPlaying'] * 15) +
                        (df[ 'attackingThreat'] * 15)) / 10, 2)

    ##########################################################################################################################################################################

    df['Target Man'] =  round(((df[ 'decisionMake'] * 15) + (df[ 'touchQuality'] * 15) +
                            (df[ 'Aerial'] * 40) + (df[ 'attackingThreat'] * 30)) / 10, 2)

    ##########################################################################################################################################################################

    df['Advanced Forward'] =  round(((df['progressiveRuns'] * 10) + (df[ 'decisionMake'] * 20) +
                            (df['touchQuality'] * 15) + (df[ 'dribbles'] * 10) +
                            (df['Aerial'] * 15) + (df[ 'attackingThreat'] * 30)) / 10, 2)


def playerAbility(df):

  def rank(df):
    for col in df.columns:
      df['rank_' + col] = df[col].rank(pct=True)

  rank(df)

  df['Pass Ability'] = ((df['rank_Passes to penalty area/90'] * 15) + (df['rank_Key passes/90'] * 15) +
                            (df['rank_Passes final 1/3 %'] * 15) + (df['rank_Smart passes/90'] * 15) + (df['rank_Passes %'] * 40))
                          
  ##########################################################################################################################################################################

  df['SetPieces Ability'] = ((df['rank_Corners/90']  * 60) + (df['rank_Direct free kicks on target, %'] * 40))

  ##########################################################################################################################################################################

  df['Dribbling Ability'] = ((df['rank_Dribbles/90']* 50) + (df['rank_Successful dribbles %'] * 50))

  ##########################################################################################################################################################################

  df['Create Chances Ability'] = ((df['rank_Shot assists/90'] * 5) + (df['rank_Second assists/90'] * 30) + (df['rank_Third assists/90'] * 15) +
                                      (df['rank_xA'] * 25) + (df['rank_Assists'] * 25))

  ##########################################################################################################################################################################

  df['Concentration Ability'] = ((df['rank_PAdj Sliding tackles'] * 50) + (df['rank_PAdj Interceptions'] * 50))

  ##########################################################################################################################################################################

  df['Finishing Ability'] = ((df['rank_Shots on target, %'] * 15) + (df['rank_Goals'] * 60) + (df['rank_xG'] * 25))


def szcore_df(df):

    cols_cat = []
    for col in df.columns:
        if col not in df.select_dtypes([np.number]).columns:
            cols_cat.append(col)

    for i in ['Age', 'Market value', 'Matches played', 'Minutes played', 'Height', 'Weight']:
        cols_cat.append(i)

    cols_num = [] 
    for col in df.select_dtypes([np.number]).columns:
            cols_num.append(col)
    
    for i in ['Age', 'Market value', 'Matches played', 'Minutes played', 'Height', 'Weight']:
        cols_num.remove(i)
        
    data = df[cols_cat]

    test = stats.zscore(df[cols_num])

    data = pd.concat([data, test], axis=1)

    return data


def PizzaChart(df, cols, playerName, league):
    # parameter list
    params = cols

    playerDF = df.loc[(df.Player == playerName) & (df.Comp == league)]

    league = playerDF.Comp.unique()

    league = league.tolist()

    league = league[0]

    position = playerDF['Position'].unique()

    position = position.tolist()

    position = position[0]
    if ', ' in position:
        position = position.split(', ')[0]

    marketValue = playerDF['Market value'].unique()

    marketValue = marketValue.tolist()
    
    marketValue = marketValue[0]

    df = df.loc[(df['Comp'] == league) & (df['Position'].str.contains(position))].reset_index(drop=True)

    player = df.loc[(df['Player'] == playerName) & (df['Comp'] == league)][cols].reset_index()
    player = list(player.loc[0])
    player = player[1:]

    values = []
    for x in range(len(params)):   
        values.append(math.floor(stats.percentileofscore(df[params[x]], player[x])))

    for n,i in enumerate(values):
        if i == 100:
            values[n] = 99

    if cols == Forward:
        # color for the slices and text
        slice_colors = ["#2d92df"] * 4 + ["#fb8c04"] * 4 + ["#eb04e3"] * 4
        text_colors = ["#F2F2F2"] * 12

    elif cols == Winger:
        # color for the slices and text
        slice_colors = ["#2d92df"] * 3 + ["#fb8c04"] * 8 + ["#eb04e3"] * 2
        text_colors = ["#F2F2F2"] * 13

    elif cols == defensive_Midfield:
        # color for the slices and text
        slice_colors = ["#2d92df"] * 4 + ["#fb8c04"] * 4 + ["#eb04e3"] * 5
        text_colors = ["#F2F2F2"] * 13
        
    elif cols == Midfield:
        # color for the slices and text
        slice_colors = ["#2d92df"] * 4 + ["#fb8c04"] * 8 + ["#eb04e3"] * 3
        text_colors = ["#F2F2F2"] * 15

    elif cols == full_Back:
        # color for the slices and text
        slice_colors = ["#2d92df"] * 6 + ["#fb8c04"] * 5 + ["#eb04e3"] * 4
        text_colors = ["#F2F2F2"] * 15

    elif cols == center_Back:
        # color for the slices and text
        slice_colors = ["#2d92df"] * 3 + ["#fb8c04"] * 4 + ["#eb04e3"] * 7
        text_colors = ["#F2F2F2"] * 14

    elif cols == offensive_Midfield:
        # color for the slices and text
        slice_colors = ["#2d92df"] * 4 + ["#fb8c04"] * 8 + ["#eb04e3"] * 4
        text_colors = ["#F2F2F2"] * 16

    # instantiate PyPizza class
    baker = PyPizza(
        params=params,                  # list of parameters
        background_color="#1b1b1b",     # background color
        straight_line_color="#000000",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_color="#000000",    # color for last line
        last_circle_lw=1,               # linewidth of last circle
        other_circle_lw=0,              # linewidth for other circles
        inner_circle_size=20            # size of inner circle
    )

    # plot pizza
    fig, ax = baker.make_pizza(
        values,                          # list of values
        figsize=(15, 10),                # adjust the figsize according to your need
        color_blank_space="same",        # use the same color to fill blank space
        slice_colors=slice_colors,       # color for individual slices
        value_colors=text_colors,        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        blank_alpha=0.4,                 # alpha for blank-space colors
        kwargs_slices=dict(
            edgecolor="#000000", zorder=2, linewidth=1
        ),                               # values to be used when plotting slices
        kwargs_params=dict(
            color="#F2F2F2", fontsize=10,
            va="center"
        ),                               # values to be used when adding parameter labels
        kwargs_values=dict(
            color="#F2F2F2", fontsize=11,
            zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        )                                # values to be used when adding parameter-values labels
    )

    if cols == Forward:

        fig_text(s =  'Forward Template',
             x = 0.253, y = 0.035,
             color='#F2F2F2',
             fontweight='bold', ha='center',
             fontsize=8)

    elif cols == Winger:

        fig_text(s =  'Winger Template',
             x = 0.253, y = 0.035,
             color='#F2F2F2',
             fontweight='bold', ha='center',
             fontsize=8)

    elif cols == defensive_Midfield:

        fig_text(s =  'Defensive Midfield Template',
             x = 0.253, y = 0.035,
             color='#F2F2F2',
             fontweight='bold', ha='center',
             fontsize=8)

    elif cols == Midfield:

        fig_text(s =  'Midfield Template',
             x = 0.253, y = 0.035,
             color='#F2F2F2',
             fontweight='bold', ha='center',
             fontsize=8)

    elif cols == full_Back:

        fig_text(s =  'Full Back Template',
             x = 0.253, y = 0.035,
             color='#F2F2F2',
             fontweight='bold', ha='center',
             fontsize=8)
    elif cols == center_Back:

        fig_text(s =  'Center Back Template',
             x = 0.253, y = 0.035,
             color='#F2F2F2',
             fontweight='bold', ha='center',
             fontsize=8)

    elif cols == offensive_Midfield:

        fig_text(s =  'Offensive Midfield Template',
             x = 0.253, y = 0.035,
             color='#F2F2F2',
             fontweight='bold', ha='center',
             fontsize=8)

    ###########################################################################################################

    fig_text(s =  playerName,
             x = 0.5, y = 1.12,
             color='#F2F2F2',
             fontweight='bold', ha='center',
             fontsize=50);

    if playerName != 'David Neres':

        fig_text(s =  'Percentile Rank | ' + league + ' | Pizza Chart | Season 2021-22',
                x = 0.5, y = 1.03,
                color='#F2F2F2',
                fontweight='bold', ha='center',
                fontsize=14);

    elif playerName == 'David Neres':

        fig_text(s =  'Percentile Rank | ' + league + ' | Pizza Chart | Calendar Year 2021',
                x = 0.5, y = 1.03,
                color='#F2F2F2',
                fontweight='bold', ha='center',
                fontsize=14);

    #fig_text(s =  str(marketValue),
    #         x = 0.5, y = 1.02,
    #         color='#F2F2F2',
    #         fontweight='bold', ha='center',
    #         fontsize=18);

    # add credits
    CREDIT_1 = "data: WyScout"
    CREDIT_2 = "made by: @menesesp20"
    CREDIT_3 = "inspired by: @Worville, @FootballSlices, @somazerofc & @Soumyaj15209314"


    # CREDITS
    fig_text(s =  f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}",
             x = 0.35, y = 0.02,
             color='#F2F2F2',
             fontweight='bold', ha='center',
             fontsize=8);

    # Attacking
    fig_text(s =  'Attacking',
             x = 0.41, y = 0.988,
             color='#F2F2F2',
             fontweight='bold', ha='center',
             fontsize=16);

    # Possession
    fig_text(s =  'Possession',
             x = 0.535, y = 0.988,
             color='#F2F2F2',
             fontweight='bold', ha='center',
             fontsize=16);

    # Defending
    fig_text(s =  'Defending',
             x = 0.665, y = 0.988,
             color='#F2F2F2',
             fontweight='bold', ha='center',
             fontsize=16);

    # add rectangles
    fig.patches.extend([
        plt.Rectangle(
            (0.34, 0.97), 0.025, 0.021, fill=True, color="#2d92df",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.47, 0.97), 0.025, 0.021, fill=True, color="#fb8c04",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.60, 0.97), 0.025, 0.021, fill=True, color="#eb04e3",
            transform=fig.transFigure, figure=fig
        ),
    ])

    # add image
    add_image('Images/SWL LOGO.png', fig, left=0.462, bottom=0.436, width=0.10, height=0.132)


def PizzaChartCompare(df, cols, playerName, playerName2):

    params = cols

###########################################################################################

    player = df.loc[df['Player'] == playerName][cols].reset_index()
    player = list(player.loc[0])
    player = player[1:]

    values = []
    for x in range(len(params)):   
        values.append(math.floor(stats.percentileofscore(df[params[x]], player[x])))

    for n,i in enumerate(values):
        if i == 100:
            values[n] = 99

###########################################################################################

    player2 = df.loc[df['Player'] == playerName2][cols].reset_index()
    player2 = list(player2.loc[0])
    player2 = player2[1:]

    values_2 = []
    for x in range(len(params)):   
        values_2.append(math.floor(stats.percentileofscore(df[params[x]], player2[x])))

    for n,i in enumerate(values_2):
        if i == 100:
            values_2[n] = 99

    # instantiate PyPizza class
    baker = PyPizza(
        params=params,                  # list of parameters
        background_color="#1b1b1b",     # background color
        straight_line_color="#000000",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_lw=1,               # linewidth of last circle
        last_circle_color="#000000",    # color of last circle
        other_circle_ls="-.",           # linestyle for other circles
        other_circle_lw=1,              # linewidth for other circles
        inner_circle_size=20            
    )

    # plot pizza
    fig, ax = baker.make_pizza(
        values,                     # list of values
        compare_values=values_2,    # comparison values
        figsize=(15, 10),             # adjust figsize according to your need
        kwargs_slices=dict(
            facecolor="#1A78CF", edgecolor="#000000",
            zorder=2, linewidth=1
        ),                          # values to be used when plotting slices
        kwargs_compare=dict(
            facecolor="#FF9300", edgecolor="#000000",
            zorder=2, linewidth=1,
        ),
        kwargs_params=dict(
            color="#F2F2F2",
            fontsize=12,
            va="center"
        ),                          # values to be used when adding parameter
        kwargs_values=dict(
            color="#F2F2F2",
            fontsize=12,
            zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        ),                          # values to be used when adding parameter-values labels
        kwargs_compare_values=dict(
            color="#F2F2F2",
            fontsize=12,
            zorder=3,
            bbox=dict(edgecolor="#000000", facecolor="#FF9300", boxstyle="round,pad=0.2", lw=1)
        ),                          # values to be used when adding parameter-values labels
    )

    fig_text(s =  playerName + ' ' + 'vs' + ' ' + playerName2,
             x = 0.52, y = 1.12,
             color='#F2F2F2',
             fontweight='bold', ha='center',
             fontsize=40);

    fig_text(s =  'Percentile Rank | Pizza Chart | Season 2021-22',
             x = 0.5, y = 1.05,
             color='#F2F2F2',
             fontweight='bold', ha='center',
             fontsize=14);

    # add credits
    CREDIT_1 = "data: WyScout"
    CREDIT_2 = "made by: @menesesp20"
    CREDIT_3 = "inspired by: @Worville, @FootballSlices, @somazerofc & @Soumyaj15209314"


    # CREDITS
    fig_text(s =  f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}",
             x = 0.35, y = 0.02,
             color='#F2F2F2',
             fontweight='bold', ha='center',
             fontsize=8);

    # Attacking
    fig_text(s =  playerName,
             x = 0.47, y = 0.988,
             color='#F2F2F2',
             fontweight='bold', ha='center',
             fontsize=16);

    # Possession
    fig_text(s =  playerName2,
             x = 0.605, y = 0.988,
             color='#F2F2F2',
             fontweight='bold', ha='center',
             fontsize=16);

    # add rectangles
    fig.patches.extend([
        plt.Rectangle(
            (0.40, 0.97), 0.025, 0.021, fill=True, color="#2d92df",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.52, 0.97), 0.025, 0.021, fill=True, color="#fb8c04",
            transform=fig.transFigure, figure=fig
        )
        ])

    # add image
    add_image('Images/SWL LOGO.png', fig, left=0.462, bottom=0.436, width=0.10, height=0.132) 


def barChart(df, playerName, league, club):

  color = clubColors.get(club)

  fig, ax = plt.subplots(figsize=(18,14))

  #Set color background outside the graph
  fig.set_facecolor('#e8e8e8')

  #Set color background inside the graph
  ax.set_facecolor('#e8e8e8')

  for i in range(len(df)):
    ax.barh(df['Similar Player'], df['Correlation Factor'], fill=False, hatch='///', height=0.5, color=color[0], edgecolor=color[0], linewidth=2)

  ax.bar_label(ax.containers[0], color='#1b1b1b', fontweight = "bold", size=15, padding=5)
  #--------------------------------------------------------------------------------------------------------------------------------------------------------------
  #Title
  Title = fig.suptitle(playerName, fontsize=35, color='#1b1b1b', fontweight = "bold", y=0.97)

  #Params for the text inside the <> this is a function to highlight text
  highlight_textprops =\
      [{"color": color[0],"fontweight": 'bold'}
      ]

  #SubTitle
  SubTitle = fig_text(s = 'Top 10 most identical <PCA players>',
                      x = 0.5, y = 0.92, highlight_textprops = highlight_textprops,
                      fontweight='bold', va='center', ha='center',fontsize=20, color='#1b1b1b');
  #--------------------------------------------------------------------------------------------------------------------------------------------------------------

  fig = add_image(image='Images/Clubs/' + league + '/' + club + '.png', fig=fig, left=0.12, bottom=0.89, width=0.2, height=0.1)

  #Atribuição da cor e tamanho das tick labels, the left=False retires the ticks
  ax.tick_params(axis='x', colors='#1b1b1b', labelsize=14)
  ax.tick_params(axis='y', colors='#1b1b1b', labelsize=14, left = False)
      
  #Setg the color of the line in the spines and retire the spines from the top and right sides
  ax.spines['bottom'].set_color('#1b1b1b')
  ax.spines['top'].set_visible(False)
  ax.spines['left'].set_color('#1b1b1b')
  ax.spines['right'].set_visible(False)

  fig.text(0.01,0.08,'Made by Pedro Meneses/@menesesp20.', color='#181818', size=12, weight='bold')


def PCA10(df, playerName, role):

    df_player = df.loc[df.Player == playerName]

    pos = df_player.iloc[0]['Position']

    pos.split(',')[0]

    df = df.loc[(df.Age <= 25) & (df['Minutes played'] >= 1500) | (df.Player == playerName)]

############################################################################## ########################################################################################################

    if role == 'Center Back':
        df = df[['Player', 'Successful dribbles %', 'Touches in box/90', 'Offensive duels %', 'Progressive runs/90', 'Crosses/90', 'Deep completed crosses/90',
            'Passes %', 'Deep completions/90', 'Progressive passes/90', 'Key passes/90', 'Third assists/90',
             'PAdj Interceptions', 'Defensive duels %', 'Aerial duels/90', 'Aerial duels %']]
             
    elif role == 'Full Back':
        df = df[['Player', 'Accurate passes, %', 'Crosses/90', 'Deep completed crosses/90', 'Deep completions/90', 'Progressive passes/90',
             'Sliding tackles/90', 'Interceptions/90', 'Successful dribbles, %', 'Defensive duels won, %',
             'Aerial duels won, %', 'Received passes/90', 'xA', 'Key passes/90', 'Second assists/90', 'Third assists/90']]

    elif role == 'Midfield':

        df = df[['Player', 'xG/90', 'Shots', 'Progressive runs/90', 'Successful dribbles %',
                       'Passes %', 'Forward passes %', 'Forward passes/90', 'Progressive passes/90','PAdj Sliding tackles',
                       'PAdj Interceptions', 'Aerial duels %', 'Defensive duels %', 'Offensive duels %']]
 
    elif role == 'Offensive Midfield':

        df = df[['Player', 'xG/90', 'Goals/90', 'Progressive runs/90', 'Successful dribbles %',
                      'xA/90', 'Deep completions/90', 'Passes to penalty area/90',
                      'Touches in box/90', 'Key passes/90', 'Passes final 1/3 %',
                      'Passes penalty area %', 'Progressive passes/90',
                      'Succ defensive actions/90', 'PAdj Interceptions', 'Aerial duels %', 'Defensive duels %']]
                      
    elif role == 'Winger':

        df = df[['Player', 'Successful dribbles %', 'Goals', 'xG/90',
          'xA/90', 'Touches in box/90', 'Dribbles/90', 'Passes to penalty area/90', 'Key passes/90',
          'Progressive runs/90', 'Crosses/90', 'Deep completed crosses/90',
          'Offensive duels/90', 'PAdj Interceptions']]

    elif role == 'Forward':

        df = df[['Player', 'Goals', 'xG/90', 'Shots on target, %', 'Goal conversion, %',
           'Successful dribbles %', 'xA/90', 'Touches in box/90', 'Dribbles/90',
           'Offensive duels/90', 'PAdj Interceptions', 'Aerial duels/90', 'Aerial duels %']]

    else:
        df = df

    #Guardar como matriz na variavél X todas as métricas e na variavél y todos os nomes dos jogadores
    X, y = df.iloc[:, 1:len(df.columns)].values, df.iloc[:, 0].values

    #Escalar os dados, passo muito importante em Machine Learning
    X_std = StandardScaler().fit_transform(X)

    #Aplicar o método PCA, ou seja reduzir o dataframe até à quantidade necessária de dados, sem perdermos informação essencial
    
    pca = PCA(n_components = len(df.columns)-1)
    pca.fit(X_std)
    X_pca = pca.transform(X_std)
    #Visualização de quantas dimensões nos interessam
    #print("Shape x_PCA: ", X_pca.shape)
    #expl = pca.explained_variance_ratio_

    #for x in range(0, len(df.columns), 2):
    #    print("Explained Variance: " + str(x) + " components:", sum(expl[0:x]))

    #plt.plot(np.cumsum(pca.explained_variance_ratio_))
    #plt.xlabel('Dimensions')
    #plt.ylabel('Explained Variance')

    #Utilizar n dimensões que nos indicar o Elbow
    N_COMP = 8
    
    columns = []

    for col in range(1, N_COMP+1):
        columns.append("PCA" + str(col))

    df_pca_resultado = pd.DataFrame(data=X_pca[:,:N_COMP], columns=columns, index = y)

    #Mostrar a correlação numa matriz
    corr_matrix = df_pca_resultado.T.corr(method='pearson')

    #Função automatizada para encontrarmos o jogador que pretendemos e o jogadores mais similar a ele
    def GetSimilarPlayers(playerName, numPlayers, corr_matrix):
        
        SimPlayers = pd.DataFrame(columns = ['PlayerName', 'Similar Player', 'Correlation Factor'])

        i = 0
        for i in range(0, numPlayers):
            row = corr_matrix.loc[corr_matrix.index == playerName].squeeze()

            SimPlayers.at[i, 'PlayerName'] = playerName
            SimPlayers.at[i, 'Similar Player'] = row.nlargest(i+2).sort_values(ascending=True).index[0]
            SimPlayers.at[i, 'Correlation Factor'] = row.nlargest(i+2).round(2).sort_values(ascending=True)[0]

            i = i+1
        
        return SimPlayers
    
    PlayerName = playerName
    NumPlayers = 5

    df_correlatedPlayers = GetSimilarPlayers(playerName, 5, corr_matrix)

    df_correlatedPlayers.drop_duplicates(inplace=True)

    return df_correlatedPlayers


def beeswarm(df, playerName, cols, playerName2=None):
    
    if playerName2 != None:
        player = df.loc[(df['Player'] == playerName)]

        league = player.Comp.unique()

        league = league[0]

        position = player.Position.unique()

        position = position.tolist()

        position = position[0]

        player2 = df.loc[(df['Player'] == playerName2)]

        league2 = player2.Comp.unique()

        league2 = league2[0]

        position2 = player.Position.unique()

        position2 = position2.tolist()

        position2 = position2[0]

        minute = player['Minutes played'].max()

        minute2 = player2['Minutes played'].max()

        if minute > minute2:
            minute = minute
        elif minute2 > minute2:
            minute = minute2
        else:
            minute = minute

        df = df.loc[(df['Minutes played'] >= minute)].reset_index()

    elif playerName2 == None:
        player = df.loc[(df['Player'] == playerName)].reset_index()

        position = player.Position.unique()

        position = position.tolist()

        position = position[0]

        minute = player['Minutes played'].max()

        league = player.Comp.unique()

        league = league[0]

        df = df.loc[(df['Minutes played'] >= minute)].reset_index()

    fig,axes = plt.subplots(3,2,figsize=(14,10))
    fig.set_facecolor('#E8E8E8')

    metrics = cols

    #set default colors
    text_color = '#181818'
    background = '#E8E8E8'

    #set up our base layer
    mpl.rcParams['xtick.color'] = text_color
    mpl.rcParams['ytick.color'] = text_color

    #create a list of comparisons
    counter=0
    counter2=0
    met_counter = 0

    for i,ax in zip(df['Player'],axes.flatten()):
        ax.set_facecolor(background)
        ax.grid(ls='dotted',lw=.5,color='#181818',axis='y',zorder=1)
        
        spines = ['top','bottom','left','right']
        for x in spines:
            if x in spines:
                ax.spines[x].set_visible(False)
                
        sns.swarmplot(x=metrics[met_counter],data=df,ax=axes[counter,counter2], zorder=1,color='#181818')
        ax.set_xlabel(f'{metrics[met_counter]}',c='#181818')
        
        if playerName2 != None:
            for x in range(len(df['Player'])):
                if playerName in df['Player'][x]:
                    ax.scatter(x=df[metrics[met_counter]][x], y=0, s=200, c='#ea04dc', zorder=2)

                if playerName2 in df['Player'][x]:
                    ax.scatter(x=df[metrics[met_counter]][x], y=0, s=200, c='#2d92df', zorder=2)

        if playerName2 == None:
            for x in range(len(df['Player'])):
                if playerName in df['Player'][x]:
                    ax.scatter(x=df[metrics[met_counter]][x], y=0, s=200, c='#ea04dc', zorder=2)            

        met_counter+=1
        if counter2 == 0:
            counter2 = 1
            continue
        if counter2 == 1:
            counter2 = 0
            counter+=1

            
    if playerName2 == None:
        highlight_textprops =\
        [{"color": '#ea04dc',"fontweight": 'bold'}]

        fig_text(s=f'<{playerName}>' + ' ' + 'Stats',
                x=0.4, y=.93,
                #highlight_weights = ['bold'],
                fontsize=30,
                highlight_textprops = highlight_textprops,
                color = text_color,
                va='center'
                    )
    elif playerName2 != None:
        highlight_textprops =\
            [{"color": '#ea04dc',"fontweight": 'bold'},
            {"color": '#2d92df',"fontweight": 'bold'}]

        fig_text(s=f'<{playerName}>' + ' ' +  'and' + ' ' + f'<{playerName2}>' + ' ' + 'Stats',
                x=0.3, y=.90,
                #highlight_weights = ['bold'],
                fontsize=30,
                highlight_textprops = highlight_textprops,
                color = text_color,
                va='center'
                    )

    fig.text(.12,.05,"all stats/90", fontsize=11, color=text_color)
    fig.text(.12,.03,"@menesesp20 / data via wyscout", fontstyle='italic', fontsize=11,color=text_color)


def beeswarmPlot(df, continent_choice, player, cols, player2=None):
    if continent_choice == 'Europe 1st tier':
        df = df.loc[(df['Minutes played'] >= 500) & (df['Comp'] == 'La Liga') | (df['Comp'] == 'Ligue 1') | (df['Comp'] == 'Bundesliga') |
                    (df['Comp'] == 'Premier League') | (df['Comp'] == 'Serie A') | (df['Comp'] == 'Liga Bwin')]

    elif continent_choice == 'Europe 2nd Tier':
        df = df.loc[(df['Minutes played'] >= 500) & (df['Comp'] == 'Liga Bwin') | (df['Comp'] == 'Super Liga Denamark') | (df['Comp'] == 'Super Liga Serbia') |
                    (df['Comp'] == 'Super Liga Turkey') | (df['Comp'] == 'First Divison Belgium') | (df['Comp'] == 'Fortuna Liga')]

    elif continent_choice == 'South America':
        df = df.loc[(df['Minutes played'] >= 50) & (df['Comp'] == 'Liga BetPlay Colombia') | (df['Comp'] == 'Liga Profesional Argentina') |
                    (df['Comp'] == 'Brasileirao')]

    elif continent_choice == 'North America':
        df = df.loc[(df['Minutes played'] >= 500) & (df['Comp'] == 'MLS') | (df['Comp'] == 'Liga Mexico')]

    elif continent_choice == 'Asia':
        df = df.loc[(df['Minutes played'] >= 500) & (df['Comp'] == 'J1 League') | (df['Comp'] == 'K League 1')]

    if player2 == None:
        return beeswarm(df, player, cols)
    else:
        return beeswarm(df, player, cols, player2)


def PCA10(df, age, comp, startValue, endValue, playerName, role):

    if (comp != 'All leagues') & (age != 'All'):
        df = df.loc[(df.Age <= age) & (df.Comp == comp) & (df['Minutes played'] >= 1500) & (df['Market value'] >= startValue) & (df['Market value'] <= endValue) | (df.Player == playerName)].reset_index(drop=True)
    elif (comp == 'All leagues') & (age != 'All'):
        df = df.loc[(df.Age <= age) & (df['Minutes played'] >= 1500) & (df['Market value'] >= startValue) & (df['Market value'] <= endValue) | (df.Player == playerName)].reset_index(drop=True)
    elif (comp != 'All leagues') & (age == 'All'):
        df = df.loc[(df.Comp == comp) & (df['Minutes played'] >= 1500) & (df['Market value'] >= startValue) & (df['Market value'] <= endValue) | (df.Player == playerName)].reset_index(drop=True)
    elif (comp == 'All leagues') & (age == 'All'):
        df = df.loc[(df['Minutes played'] >= 1500) & (df['Market value'] >= startValue) & (df['Market value'] <= endValue) | (df.Player == playerName)].reset_index(drop=True)

############################################################################## ########################################################################################################

    if role == 'Center Back':
        df = df[['Player', 'Successful dribbles %', 'Touches in box/90', 'Offensive duels %', 'Progressive runs/90', 'Crosses/90', 'Deep completed crosses/90',
            'Passes %', 'Deep completions/90', 'Progressive passes/90', 'Key passes/90', 'Third assists/90',
             'PAdj Interceptions', 'Defensive duels %', 'Aerial duels/90', 'Aerial duels %']]

    elif role == 'Full Back':
        df = df[['Player', 'Accurate passes, %', 'Crosses/90', 'Deep completed crosses/90', 'Deep completions/90', 'Progressive passes/90',
             'Sliding tackles/90', 'Interceptions/90', 'Successful dribbles, %', 'Defensive duels won, %',
             'Aerial duels won, %', 'Received passes/90', 'xA', 'Key passes/90', 'Second assists/90', 'Third assists/90']]

    elif role == 'Defensive Midfield':
        df = df[['Player', 'xG/90', 'Shots', 'Progressive runs/90', 'Successful dribbles %',
                       'Passes %', 'Forward passes %', 'Forward passes/90', 'Progressive passes/90','PAdj Sliding tackles',
                       'PAdj Interceptions', 'Aerial duels %', 'Defensive duels %', 'Offensive duels %']]

    elif role == 'Midfield':
        df = df[['Player', 'xG/90', 'Shots', 'Progressive runs/90', 'Successful dribbles %',
                       'Passes %', 'Forward passes %', 'Forward passes/90', 'Progressive passes/90','PAdj Sliding tackles',
                       'PAdj Interceptions', 'Aerial duels %', 'Defensive duels %', 'Offensive duels %']]
 
    elif role == 'Offensive Midfield':
        df = df[['Player', 'xG/90', 'Goals/90', 'Progressive runs/90', 'Successful dribbles %',
                      'xA/90', 'Deep completions/90', 'Passes to penalty area/90',
                      'Touches in box/90', 'Key passes/90', 'Passes final 1/3 %',
                      'Passes penalty area %', 'Progressive passes/90',
                      'Succ defensive actions/90', 'PAdj Interceptions', 'Aerial duels %', 'Defensive duels %']]

    elif role == 'Winger':
        df = df[['Player', 'Successful dribbles %', 'Goals', 'xG/90',
          'xA/90', 'Touches in box/90', 'Dribbles/90', 'Passes to penalty area/90', 'Key passes/90',
          'Progressive runs/90', 'Crosses/90', 'Deep completed crosses/90',
          'Offensive duels/90', 'PAdj Interceptions']]

    elif role == 'Forward':
        df = df[['Player', 'Goals', 'xG/90', 'Shots on target, %', 'Goal conversion, %',
           'Successful dribbles %', 'xA/90', 'Touches in box/90', 'Dribbles/90',
           'Offensive duels/90', 'PAdj Interceptions', 'Aerial duels/90', 'Aerial duels %']]

    else:

        df = df
    #Guardar como matriz na variavél X todas as métricas e na variavél y todos os nomes dos jogadores
    X, y = df.iloc[:, 1:len(df.columns)].values, df.iloc[:, 0].values

    #Escalar os dados, passo muito importante em Machine Learning
    X_std = StandardScaler().fit_transform(X)

    #Aplicar o método PCA, ou seja reduzir o dataframe até à quantidade necessária de dados, sem perdermos informação essencial
    
    pca = PCA(n_components = len(df.columns)-1)
    pca.fit(X_std)
    X_pca = pca.transform(X_std)
    #Visualização de quantas dimensões nos interessam
    #print("Shape x_PCA: ", X_pca.shape)
    #expl = pca.explained_variance_ratio_

    #for x in range(0, len(df.columns), 2):
    #    print("Explained Variance: " + str(x) + " components:", sum(expl[0:x]))

    #plt.plot(np.cumsum(pca.explained_variance_ratio_))
    #plt.xlabel('Dimensions')
    #plt.ylabel('Explained Variance')

    #Utilizar n dimensões que nos indicar o Elbow
    N_COMP = 8
    
    columns = []

    for col in range(1, N_COMP+1):
        columns.append("PCA" + str(col))

    df_pca_resultado = pd.DataFrame(data=X_pca[:,:N_COMP], columns=columns, index = y)

    #Mostrar a correlação numa matriz
    corr_matrix = df_pca_resultado.T.corr(method='pearson')

    #Função automatizada para encontrarmos o jogador que pretendemos e o jogadores mais similar a ele
    def GetSimilarPlayers(playerName, numPlayers, corr_matrix):
        
        SimPlayers = pd.DataFrame(columns = ['PlayerName', 'Similar Player', 'Correlation Factor'])

        i = 0
        for i in range(0, numPlayers):
            row = corr_matrix.loc[corr_matrix.index == playerName].squeeze()

            SimPlayers.at[i, 'PlayerName'] = playerName
            SimPlayers.at[i, 'Similar Player'] = row.nlargest(i+2).sort_values(ascending=True).index[0]
            SimPlayers.at[i, 'Correlation Factor'] = row.nlargest(i+2).round(2).sort_values(ascending=True)[0]

            i = i+1
        
        return SimPlayers
    
    PlayerName = playerName
    NumPlayers = 5

    df_correlatedPlayers = GetSimilarPlayers(playerName, 5, corr_matrix)

    df_correlatedPlayers.drop_duplicates(inplace=True)

    return df_correlatedPlayers


def similarityDashboard(df, age, comp, startValue, endValue, playerName, role):

        fig = plt.figure(figsize=(50, 45), dpi = 100, facecolor = '#f2f2f2')
        gspec = gridspec.GridSpec(
        ncols=7, nrows=2, wspace = 0.5
        )

        ########################################################################################################################################################

        ax6 = plt.subplot(
                        gspec[1, 0],
                )

        df1 = PCA10(df, age, comp, startValue, endValue, playerName, role).sort_values('Correlation Factor', ascending=False).reset_index(drop=True)

        if role == 'Center Back':
            role = center_Back
                
        elif role == 'Full Back':
            role = full_Back

        elif role == 'Defensive Midfield':
            role = defensive_Midfield

        elif role == 'Midfield':
            role = Midfield
    
        elif role == 'Offensive Midfield':
            role = offensive_Midfield
                        
        elif role == 'Winger':
            role = Winger

        elif role == 'Forward':
            role = Forward

        rows = 9
        cols = 0

        #Criação da lista de jogadores
        Players = df1['PlayerName'].unique()

        Players = Players.tolist()

        #Criação da lista de jogadores similares
        similarPlayers = df1['Similar Player'].unique()

        similarPlayers = similarPlayers.tolist()
        
        df2 = df.loc[(df['Player'] == df1['Similar Player'].iloc[0]) | (df['Player'] == df1['Similar Player'].iloc[1]) | (df['Player'] == df1['Similar Player'].iloc[2]) |
                     (df['Player'] == df1['Similar Player'].iloc[3]) | (df['Player'] == df1['Similar Player'].iloc[4])]

        xG90 = df2['xG/90']

        Goals90 = df2['Goals/90']

        Progressiveruns = df2['Progressive runs/90']

        Dribles = df2['Successful dribbles %']

        xA90 = df2['xA/90']

        Deepcompletions90 = df2['Deep completions/90']

        Penaltyarea90 = df2['Passes to penalty area/90']

        Touches = df2['Touches in box/90']

        Keypasses90 = df2['Key passes/90']

        PassesFinalThird = df2['Passes final 1/3 %']

        Passespenaltyarea = df2['Passes penalty area %']

        Progressivepasses90 = df2['Progressive passes/90']

        Succdefensiveactions90 = df2['Succ defensive actions/90']

        PAdjInterceptions = df2['PAdj Interceptions']

        Aerialduels = df2['Aerial duels %']

        Defensiveduels = df2['Defensive duels %']

        #Valores de similariedade
        valuePlayers = df1['Correlation Factor']
        valuePlayers = valuePlayers.tolist()

        data = {
                'Players' : similarPlayers,
                'Similarity' : valuePlayers,
                'xG/90' : xG90,
                'Goals/90' : Goals90,
                'Progressive runs/90' : Progressiveruns,
                'Succ dribbles %' : Dribles,
                'xA/90' : xA90,
                'Deep completions/90' : Deepcompletions90,
                'Passes to penalty area/90' : Penaltyarea90,
                'Touches in box/90' : Touches,
                'Key passes/90' : Keypasses90,
                'Passes final 1/3 %' : PassesFinalThird,
                'Passes penalty area %' : Passespenaltyarea,
                'Progressive passes/90' : Progressivepasses90,
                'Succ defensive actions/90' : Succdefensiveactions90,
                'PAdj Interceptions' : PAdjInterceptions,
                'Aerial duels %' : Aerialduels,
                'Defensive duels %' : Defensiveduels

        }

        data = pd.DataFrame(data)

        data.reset_index(drop=True, inplace=True)

        data = data.T

        data = data.to_dict('index')

        for i in range(1):
                for k, v in data.items():
                        if k == 'Players':
                                ax6.text(x=8, y=11, s=v[0], va='center', ha='center', weight='bold', size=48, color='#ea04dc')
                                ax6.text(x=11.5, y=11, s=v[1], va='center', ha='center', weight='bold', size=48, color='#ea04dc')
                                ax6.text(x=14.3, y=11, s=v[2], va='center', ha='center', weight='bold', size=48, color='#ea04dc')
                                ax6.text(x=17.5, y=11, s=v[3], va='center', ha='center', weight='bold', size=48, color='#ea04dc')
                                ax6.text(x=20.8, y=11, s=v[4], va='center', ha='center', weight='bold', size=48, color='#ea04dc')
                                # shots column - this is my "main" column, hence bold text

                        if k == 'Similarity':
                                ax6.text(x=8, y=10.3, s=v[0], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=11.5, y=10.3, s=v[1], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=14.3, y=10.3, s=v[2], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=17.5, y=10.3, s=v[3], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=20.8, y=10.3, s=v[4], va='center', ha='right', size=48, color='#181818')

                        if k == 'xG/90':
                                ax6.text(x=8, y=9.6, s=v[0], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=11.5, y=9.6, s=v[1], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=14.3, y=9.6, s=v[2], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=17.5, y=9.6, s=v[3], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=20.8, y=9.6, s=v[4], va='center', ha='right', size=48, color='#181818')

                        if k == 'Progressive runs/90':
                                ax6.text(x=8, y=8.9, s=v[0], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=11.5, y=8.9, s=v[1], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=14.3, y=8.9, s=v[2], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=17.5, y=8.9, s=v[3], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=20.8, y=8.9, s=v[4], va='center', ha='right', size=48, color='#181818')

                        if k == 'Succ dribbles %':
                                ax6.text(x=8, y=8.2, s=v[0], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=11.5, y=8.2, s=v[1], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=14.3, y=8.2, s=v[2], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=17.5, y=8.2, s=v[3], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=20.8, y=8.2, s=v[4], va='center', ha='right', size=48, color='#181818')

                        if k == 'xA/90':
                                ax6.text(x=8, y=7.5, s=v[0], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=11.5, y=7.5, s=v[1], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=14.3, y=7.5, s=v[2], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=17.5, y=7.5, s=v[3], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=20.8, y=7.5, s=v[4], va='center', ha='right', size=48, color='#181818')

                        if k == 'Deep completions/90':
                                ax6.text(x=8, y=6.8, s=v[0], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=11.5, y=6.8, s=v[1], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=14.3, y=6.8, s=v[2], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=17.5, y=6.8, s=v[3], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=20.8, y=6.8, s=v[4], va='center', ha='right', size=48, color='#181818')

                        if k == 'Passes to penalty area/90':
                                ax6.text(x=8, y=6.1, s=v[0], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=11.5, y=6.1, s=v[1], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=14.3, y=6.1, s=v[2], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=17.5, y=6.1, s=v[3], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=20.8, y=6.1, s=v[4], va='center', ha='right', size=48, color='#181818')

                        if k == 'Touches in box/90':
                                ax6.text(x=8, y=5.4, s=v[0], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=11.5, y=5.4, s=v[1], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=14.3, y=5.4, s=v[2], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=17.5, y=5.4, s=v[3], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=20.8, y=5.4, s=v[4], va='center', ha='right', size=48, color='#181818')

                        if k == 'Key passes/90':
                                ax6.text(x=8, y=4.7, s=v[0], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=11.5, y=4.7, s=v[1], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=14.3, y=4.7, s=v[2], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=17.5, y=4.7, s=v[3], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=20.8, y=4.7, s=v[4], va='center', ha='right', size=48, color='#181818')

                        if k == 'Passes final 1/3 %':
                                ax6.text(x=8, y=4, s=v[0], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=11.5, y=4, s=v[1], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=14.3, y=4, s=v[2], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=17.5, y=4, s=v[3], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=20.8, y=4, s=v[4], va='center', ha='right', size=48, color='#181818')

                        if k == 'Passes penalty area %':
                                ax6.text(x=8, y=3.3, s=v[0], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=11.5, y=3.3, s=v[1], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=14.3, y=3.3, s=v[2], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=17.5, y=3.3, s=v[3], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=20.8, y=3.3, s=v[4], va='center', ha='right', size=48, color='#181818')

                        if k == 'Progressive passes/90':
                                ax6.text(x=8, y=2.6, s=v[0], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=11.5, y=2.6, s=v[1], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=14.3, y=2.6, s=v[2], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=17.5, y=2.6, s=v[3], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=20.8, y=2.6, s=v[4], va='center', ha='right', size=48, color='#181818')

                        if k == 'Succ defensive actions/90':
                                ax6.text(x=8, y=1.9, s=v[0], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=11.5, y=1.9, s=v[1], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=14.3, y=1.9, s=v[2], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=17.5, y=1.9, s=v[3], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=20.8, y=1.9, s=v[4], va='center', ha='right', size=48, color='#181818')

                        if k == 'PAdj Interceptions':
                                ax6.text(x=8, y=1.2, s=v[0], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=11.5, y=1.2, s=v[1], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=14.3, y=1.2, s=v[2], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=17.5, y=1.2, s=v[3], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=20.8, y=1.2, s=v[4], va='center', ha='right', size=48, color='#181818')

                        if k == 'Aerial duels %':
                                ax6.text(x=8, y=0.5, s=v[0], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=11.5, y=0.5, s=v[1], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=14.3, y=0.5, s=v[2], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=17.5, y=0.5, s=v[3], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=20.8, y=0.5, s=v[4], va='center', ha='right', size=48, color='#181818')

                        if k == 'Defensive duels %':
                                ax6.text(x=8, y=-0.2, s=v[0], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=11.5, y=-0.2, s=v[1], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=14.3, y=-0.2, s=v[2], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=17.5, y=-0.2, s=v[3], va='center', ha='right', size=48, color='#181818')
                                ax6.text(x=20.8, y=-0.2, s=v[4], va='center', ha='right', size=48, color='#181818')


        ax6.text(1, 11, 'Players', weight='bold', ha='left', size=50, color='#ea04dc')

        ax6.text(1, 10.3, 'Similarity', weight='bold', ha='left', size=50, color='#ea04dc')

        ax6.text(1, 9.6, 'xG/90', weight='bold', ha='left', size=50, color='#ea04dc')

        ax6.text(1, 8.9, 'Progressive runs/90', weight='bold', ha='left', size=50, color='#ea04dc')

        ax6.text(1, 8.2, 'Succ Dribbles %', weight='bold', ha='left', size=50, color='#ea04dc')

        ax6.text(1, 7.5, 'xA/90', weight='bold', ha='left', size=50, color='#ea04dc')

        ax6.text(1, 6.8, 'Deep Completions/90', weight='bold', ha='left', size=50, color='#ea04dc')

        ax6.text(1, 6.1, 'Passes penalty area/90', weight='bold', ha='left', size=50, color='#ea04dc')

        ax6.text(1, 5.4, 'Touches box/90', weight='bold', ha='left', size=50, color='#ea04dc')

        ax6.text(1, 4.7, 'Key passes/90', weight='bold', ha='left', size=50, color='#ea04dc')

        ax6.text(1, 4, 'Passes final 1/3 %', weight='bold', ha='left', size=50, color='#ea04dc')

        ax6.text(1, 3.3, 'Passes penalty area %', weight='bold', ha='left', size=50, color='#ea04dc')

        ax6.text(1, 2.6, 'Progressive passes/90', weight='bold', ha='left', size=50, color='#ea04dc')

        ax6.text(1, 1.9, 'Succ defensive actions/90', weight='bold', ha='left', size=50, color='#ea04dc')

        ax6.text(1, 1.2, 'PAdj Interceptions', weight='bold', ha='left', size=50, color='#ea04dc')

        ax6.text(1, 0.5, 'Aerial duels %', weight='bold', ha='left', size=50, color='#ea04dc')

        ax6.text(1, -0.2, 'Defensive duels %', weight='bold', ha='left', size=50, color='#ea04dc')

        for row in range(rows):
                ax6.plot(
                [0, cols + 2],
                [row -.5, row - .5],
                ls=':',
                lw='.5',
                c='#e8e8e8'
                )

        ax6.axis('off')

        """
        for i in range(len(data)):

                ax6_image = add_image(image='Images/Players/' + 'Premier League' + '/' + data[0].get('Players') + '.png', fig=fig, left=0.09, bottom=0.16, width=0.1, height=0.058)

                ax6_image = add_image(image='Images/Players/' + 'Premier League' + '/' + data[1].get('Players') + '.png', fig=fig, left=0.09, bottom=0.242, width=0.1, height=0.058)

                ax6_image = add_image(image='Images/Players/' + 'Premier League' + '/' + data[2].get('Players') + '.png', fig=fig, left=0.09, bottom=0.322, width=0.1, height=0.058)

                ax6_image = add_image(image='Images/Players/' + 'Premier League' + '/' + data[3].get('Players')+ '.png', fig=fig, left=0.09, bottom=0.398, width=0.1, height=0.058)

                ax6_image = add_image(image='Images/Players/' + 'Premier League' + '/' + data[4].get('Players') + '.png', fig=fig, left=0.09, bottom=0.47, width=0.1, height=0.058)

                ax6_image = add_image(image='Images/Players/' + 'Premier League' + '/' + data[5].get('Players') + '.png', fig=fig, left=0.09, bottom=0.55, width=0.1, height=0.058)

                ax6_image = add_image(image='Images/Players/' + 'Premier League' + '/' + data[6].get('Players') + '.png', fig=fig, left=0.09, bottom=0.624, width=0.1, height=0.058)

                ax6_image = add_image(image='Images/Players/' + 'Premier League' + '/' + data[7].get('Players') + '.png', fig=fig, left=0.09, bottom=0.70, width=0.1, height=0.058)

                ax6_image = add_image(image='Images/Players/' + 'Premier League' + '/' + data[8].get('Players') + '.png', fig=fig, left=0.09, bottom=0.773, width=0.1, height=0.058)

                ax6_image = add_image(image='Images/Players/' + 'Premier League' + '/' + data[9].get('Players') + '.png', fig=fig, left=0.09, bottom=0.85, width=0.1, height=0.058)
        """

        ax1 = plt.subplot(
                        gspec[0, 1],
                )

        cols = role

        #PLAYER 1
        pl1 = df.loc[df['Player'] == playerName]
        values = pl1[cols].values[0]

        #Obtenção do alcance minimo e máximo dos valores
        ranges = [(df[col].min(), df[col].max()) for col in cols]

        #Criação do radar chart
        radar = Radar(background_color="#181818", patch_color='#181818', range_color="#181818", label_color="#181818", label_fontsize=0, range_fontsize=0)
        fig, ax1 = radar.plot_radar(ranges=ranges, 
                                params=cols, 
                                values=values, 
                                radar_color=['#ea04dc', '#ea04dc'],
                                figax=(fig, ax1),
                                end_size=0, end_color="#1b1b1b")

        ax_text(x = -20, y = -25,
                s=playerName,
                size=48,
                color='#181818',
                ax=ax1)

        team = pl1['Team'].unique()
        team = team.tolist()
        team = team[0]

        ax_text(x = -5, y = -19,
                s=team,
                size=35,
                color='#181818',
                ax=ax1)

        ########################################################################################################################################################

        ax2 = plt.subplot(
                        gspec[0, 2],
                )

        cols = role

        #PLAYER 1
        pl1 = df.loc[df['Player'] == data.get('Players')[0]]
        val1 = pl1[cols].values[0]

        # PLAYER 2
        pl2 = df.loc[df['Player'] == playerName]
        val2 = pl2[cols].values[0]

        values = [val1, val2]

        #Obtenção do alcance minimo e máximo dos valores
        ranges = [(df[col].min(), df[col].max()) for col in cols]

        #Criação do radar chart
        radar = Radar(background_color="#181818", patch_color='#181818', range_color="#181818", label_color="#181818", label_fontsize=0, range_fontsize=0)
        fig, ax2 = radar.plot_radar(ranges=ranges, 
                                params=cols, 
                                values=values, 
                                radar_color=['#2d92df', '#ea04dc'],
                                figax=(fig, ax2),
                                end_size=0, end_color="#1b1b1b",
                                compare=True)

        ax_text(x = -8, y = -27,
                s=data.get('Players')[0],
                size=48,
                color='#181818',
                ax=ax2)

        team = pl1['Team'].unique()
        team = team.tolist()
        team = team[0]

        ax_text(x = -5, y = -19,
                s=team,
                size=35,
                color='#181818',
                ax=ax2)

        ########################################################################################################################################################    

        ax3 = plt.subplot(
                        gspec[0, 3],
                )

        cols = role

        #PLAYER 1
        pl1 = df.loc[df['Player'] == data.get('Players')[1]]
        val1 = pl1[cols].values[0]

        # PLAYER 2
        pl2 = df.loc[df['Player'] == playerName]
        val2 = pl2[cols].values[0]

        values = [val1, val2]
        #Obtenção do alcance minimo e máximo dos valores
        ranges = [(df[col].min(), df[col].max()) for col in cols]

        #Criação do radar chart
        radar = Radar(background_color="#181818", patch_color='#181818', range_color="#181818", label_color="#181818", label_fontsize=0, range_fontsize=0)
        fig, ax3 = radar.plot_radar(ranges=ranges, 
                                params=cols, 
                                values=values, 
                                radar_color=['#2d92df', '#ea04dc'],
                                figax=(fig, ax3),
                                end_size=0, end_color="#1b1b1b",
                                compare=True)

        ax_text(x = -8, y = -27,
                s=data.get('Players')[1],
                size=48,
                color='#181818',
                ax=ax3)

        team = pl1['Team'].unique()
        team = team.tolist()
        team = team[0]

        ax_text(x = -5, y = -19,
                s=team,
                size=35,
                color='#181818',
                ax=ax3)

        ########################################################################################################################################################

        ax4 = plt.subplot(
                        gspec[0, 4],
                )

        cols = role

        #PLAYER 1
        pl1 = df.loc[df['Player'] == data.get('Players')[2]]
        val1 = pl1[cols].values[0]

        # PLAYER 2
        pl2 = df.loc[df['Player'] == playerName]
        val2 = pl2[cols].values[0]

        values = [val1, val2]
        #Obtenção do alcance minimo e máximo dos valores
        ranges = [(df[col].min(), df[col].max()) for col in cols]

        #Criação do radar chart
        radar = Radar(background_color="#181818", patch_color='#181818', range_color="#181818", label_color="#181818", label_fontsize=0, range_fontsize=0)
        fig, ax4 = radar.plot_radar(ranges=ranges, 
                                params=cols, 
                                values=values, 
                                radar_color=['#2d92df', '#ea04dc'],
                                figax=(fig, ax4),
                                end_size=0, end_color="#181818",
                                compare=True)

        ax_text(x = -8, y = -27,
                s=data.get('Players')[2],
                size=48,
                color='#181818',
                ax=ax4)

        team = pl1['Team'].unique()
        team = team.tolist()
        team = team[0]

        ax_text(x = -5, y = -19,
                s=team,
                size=35,
                color='#181818',
                ax=ax4)

        ########################################################################################################################################################

        ax5 = plt.subplot(
                        gspec[0, 5],
                )

        cols = role

        #PLAYER 1
        pl1 = df.loc[df['Player'] == data.get('Players')[3]]
        val1 = pl1[cols].values[0]

        # PLAYER 2
        pl2 = df.loc[df['Player'] == playerName]
        val2 = pl2[cols].values[0]

        values = [val1, val2]
        #Obtenção do alcance minimo e máximo dos valores
        ranges = [(df[col].min(), df[col].max()) for col in cols]

        #Criação do radar #181818
        radar = Radar(background_color="#181818", patch_color='#181818', range_color="#181818", label_color="#181818", label_fontsize=0, range_fontsize=0)
        fig, ax5 = radar.plot_radar(ranges=ranges, 
                                params=cols, 
                                values=values, 
                                radar_color=['#2d92df', '#ea04dc'],
                                figax=(fig, ax5),
                                end_size=0, end_color="#181818",
                                compare=True)

        ax_text(x = -8, y = -27,
                s= data.get('Players')[3],
                size=48,
                color='#181818',
                ax=ax5)

        team = pl1['Team'].unique()
        team = team.tolist()
        team = team[0]

        ax_text(x = -5, y = -19,
                s=team,
                size=35,
                color='#181818',
                ax=ax5)

        ########################################################################################################################################################

        ax7 = plt.subplot(
                        gspec[0, 6],
                )

        cols = role

        #PLAYER 1
        pl1 = df.loc[df['Player'] == data.get('Players')[4]]
        val1 = pl1[cols].values[0]

        # PLAYER 2
        pl2 = df.loc[df['Player'] == playerName]
        val2 = pl2[cols].values[0]

        values = [val1, val2]
        #Obtenção do alcance minimo e máximo dos valores
        ranges = [(df[col].min(), df[col].max()) for col in cols]

        #Criação do radar chart
        radar = Radar(background_color="#181818", patch_color='#181818', range_color="#181818", label_color="#181818", label_fontsize=0, range_fontsize=0)
        fig, ax7 = radar.plot_radar(ranges=ranges, 
                                params=cols, 
                                values=values, 
                                radar_color=['#2d92df', '#ea04dc'],
                                figax=(fig, ax7),
                                end_size=0, end_color="#181818",
                                compare=True)

        ax_text(x = -8, y = -27,
                s= data.get('Players')[4],
                size=48,
                color='#181818',
                ax=ax7)

        team = pl1['Team'].unique()
        team = team.tolist()
        team = team[0]

        ax_text(x = -5, y = -19,
                s=team,
                size=35,
                color='#181818',
                ax=ax7)

########################################################################################################################################################

        #Params for the text inside the <> this is a function to highlight text
        highlight_textprops =\
        [{"color": "#ea04dc","fontweight": 'bold'}]

        fig_text(x = 0.15, y = 0.8,
                s= 'Similar to:' + ' ' + f'<{playerName}>',
                size=100,
                highlight_textprops = highlight_textprops,
                color='#181818')

########################################################################################################################################################

        subtitle = df.loc[df['Player'] == playerName]

        team = subtitle.Team.unique()

        team = team.tolist()

        team = team[0]

########################################################################################################################################################

        league = subtitle.Comp.unique()

        league = league.tolist()

        league = league[0]

########################################################################################################################################################

        season = subtitle.Season.unique()

        season = season.tolist()

        season = season[0]

########################################################################################################################################################

        fig_text(x = 0.15, y = 0.768,
                s= team + ' |' + league + ' |' + season,
                size=35,
                color='#181818',
                ax=ax6)

        ax_text(x = 0.15, y = -0.70,
                s= 'Visualization made by: Pedro Menees | @menesesp20',
                size=30,
                color='#181818',
                ax=ax6)

        ax_text(x = 0.15, y = -1,
                s= 'Data from WyScout',
                size=25,
                color='#181818',
                ax=ax6)


def scoutReport(df, playerName, league, setPieces, isDefensive):

    playerClub = df.loc[df['Player'] == playerName]

    playerClub['Market value'] = playerClub['Market value'].astype(str)

    country = playerClub['Birth country'].unique()
    country = country.tolist()
    country = country[0]
    if country == '0':
        country = playerClub['Passport country'].unique()
        country = country.tolist()
        country = country[0]
    if ',' in country:
        country = country.split(', ')[0]

    Market = playerClub['Market value'].unique()
    Market = Market.tolist()
    Market = Market[0]

    if len(str(Market)) == 6:
        Market = str(Market)[:3]
                
    elif len(str(Market)) == 7:
        if str(Market)[:2][1] != 0:
            Market = str(Market)[:2][0] + '.' + str(Market)[:2][1] + 'M'
            
    elif len(str(Market)) == 8:
        Market = str(Market)[:2] + 'M'

    elif len(str(Market)) == 9:
        Market = str(Market)[:3] + 'M'

    position = playerClub['Position'].unique()
    position = position.tolist()
    position = position[0]
    if ', ' in position:
        position = position.split(', ')[0]

    Contract = playerClub['Contract expires'].unique()
    Contract = Contract.tolist()
    Contract = Contract[0]

    Height = playerClub['Height'].unique()
    Height = Height.tolist()
    Height = str(Height[0])

    Foot = playerClub['Foot'].unique()
    Foot = Foot.tolist()
    Foot = Foot[0]

    Minutes = playerClub['Minutes played'].unique()
    Minutes = Minutes.tolist()
    Minutes = str(Minutes[0])
    Minutes = int(Minutes)

    club = playerClub['Team'].unique()
    club = club.tolist()
    club = club[0]

    color = ['#FF0000', '#181818']

    #######################################################################################################################################

    fig = plt.figure(figsize=(15, 10), dpi=1000, facecolor = '#F2F2F2')
    gspec = gridspec.GridSpec(
    ncols=2, nrows=2, wspace = 0.5
    )

    ########################################################################################################################################################

    ax1 = plt.subplot(
                    gspec[0, 0],
            )


    ax1.axis('off')

    ax2 = plt.subplot(
                    gspec[1, 1],
            )

    pitch = Pitch(pitch_type='opta',pad_top=-0.5, pad_bottom=0.5, pad_right=-0.5,
                                pitch_color='#F2F2F2', line_color='#1b1b1b',line_zorder=1, linewidth=5, spot_scale=0.002)

    pitch.draw(ax=ax2)

    if 'GK' in position:
        # GK
        pitch.scatter(x=5.8, y=50, ax=ax2, c=color[0], edgecolor='#1b1b1b', s=500, zorder=3)

#######################################################################################################################################

    elif 'RB' in position:
        # RIGHT FULLBACK
        pitch.scatter(x=17, y=15, ax=ax2, c=color[0], edgecolor='#1b1b1b', s=500, zorder=3)

    elif 'RCB' in position:
        # RIGHT CENTER BACK
        pitch.scatter(x=17, y=36.8, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

    elif 'LCB' in position:
        # LEFT CENTER BACK
        pitch.scatter(x=17, y=63.2, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

    elif 'LB' in position:
        # LEFT FULLBACK
        pitch.scatter(x=17, y=85, ax=ax2, c=color[0], edgecolor='#1b1b1b', s=500, zorder=3)

#######################################################################################################################################

    elif 'DM' in position:
        # DEFENSIVE MIDFIELDER
        pitch.scatter(x=40, y=50, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

    elif 'RCMF' in position:
        # CENTER MIDFIELDER RIGHT
        pitch.scatter(x=55, y=36.8, ax=ax2, c=color[0], edgecolor='#1b1b1b', s=500, zorder=3)

    elif 'LCMF' in position:
        # CENTER MIDFIELDER LEFT
        pitch.scatter(x=55, y=63.2, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

#######################################################################################################################################
    elif 'RAMF' in position:
        # RIGHT MIDFIELDER
        pitch.scatter(x=70, y=15, ax=ax2, c=color[0], edgecolor='#1b1b1b', s=500, zorder=3)

    elif 'AMF' in position:
        # OFFENSIVE MIDFIELDER
        pitch.scatter(x=70, y=50, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

    elif 'LAMF' in position:
        # LEFT MIDFIELDER
        pitch.scatter(x=70, y=85, ax=ax2, c=color[0], edgecolor='#1b1b1b', s=500, zorder=3)

#######################################################################################################################################

    elif 'LW' in position:
        # WINGER LEFT
        pitch.scatter(x=85, y=88, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

    elif 'RW' in position:
        # WINGER RIGHT
        pitch.scatter(x=85, y=12, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

#######################################################################################################################################

    elif 'CF' in position:
        # FORWARD
        pitch.scatter(x=88.5, y=50, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

######################################################## MUTIPLE POSITIONS - LW / RW AND OM ###############################################################################

    elif (position == 'LCB & RCB') | (position == 'RCB & LCB'):
        # LEFT CENTER BACK
        pitch.scatter(x=17, y=63.2, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)
        
        # RIGHT CENTER BACK
        pitch.scatter(x=17, y=36.8, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

    elif (position == 'LW & AMF') | (position == 'OM & LW'):
        # WINGER LEFT
        pitch.scatter(x=85, y=88, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

        # OFFENSIVE MIDFIELDER
        pitch.scatter(x=70, y=50, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

    elif (position == 'RW & AMF') | (position == 'AMF & RW'):
        # WINGER RIGHT
        pitch.scatter(x=85, y=12, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

        # OFFENSIVE MIDFIELDER
        pitch.scatter(x=70, y=50, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

######################################################## MUTIPLE POSITIONS - LM / RM AND OM ###############################################################################

    elif (position == 'LAMF & AMF') | (position == 'AMF & LAMF'):
        # LEFT MIDFIELDER
        pitch.scatter(x=70, y=85, ax=ax2, c=color[0], edgecolor='#1b1b1b', s=500, zorder=3)

        # OFFENSIVE MIDFIELDER
        pitch.scatter(x=70, y=50, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

    elif (position == 'RAMF & AMF') | (position == 'AMF & RAMF'):
        # RIGHT MIDFIELDER
        pitch.scatter(x=70, y=15, ax=ax2, c=color[0], edgecolor='#1b1b1b', s=500, zorder=3)

        # OFFENSIVE MIDFIELDER
        pitch.scatter(x=70, y=50, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

######################################################## MUTIPLE POSITIONS - AMF, CF, RCMF ###############################################################################

    elif (position == 'AMF, CF, RCMF'):
        # FORWARD
        pitch.scatter(x=88.5, y=50, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

        # OFFENSIVE MIDFIELDER
        pitch.scatter(x=70, y=50, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

        # RIGHT MIDFIELDER
        pitch.scatter(x=70, y=15, ax=ax2, c=color[0], edgecolor='#1b1b1b', s=500, zorder=3)
######################################################## MUTIPLE POSITIONS - FW AND OM ###############################################################################

    elif (position == 'FW & AMF') | (position == 'AMF & FW'):
        # FORWARD
        pitch.scatter(x=88.5, y=50, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

        # OFFENSIVE MIDFIELDER
        pitch.scatter(x=70, y=50, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

######################################################## MUTIPLE POSITIONS - RB AND LB ###############################################################################

    elif (position == 'LB & RB') | (position == 'RB & LB'):
        # RIGHT FULLBACK
        pitch.scatter(x=17, y=15, ax=ax2, c=color[0], edgecolor='#1b1b1b', s=500, zorder=3)

        # LEFT FULLBACK
        pitch.scatter(x=17, y=85, ax=ax2, c=color[0], edgecolor='#1b1b1b', s=500, zorder=3)

######################################################## MUTIPLE POSITIONS - LCB AND LB ###############################################################################

    elif (position == 'LB & LCB') | (position == 'LCB & LB'):
        # LEFT CENTER BACK
        pitch.scatter(x=17, y=36.8, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)
        
        # LEFT FULLBACK
        pitch.scatter(x=17, y=15, ax=ax2, c=color[0], edgecolor='#1b1b1b', s=500, zorder=3)

######################################################## MUTIPLE POSITIONS - RCB AND RB ###############################################################################

    elif (position == 'RB & RCB') | (position == 'RCB & RB'):
        # RIGHT CENTER BACK
        pitch.scatter(x=17, y=63.2, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)
        
        # RIGHT FULLBACK
        pitch.scatter(x=17, y=15, ax=ax2, c=color[0], edgecolor='#1b1b1b', s=500, zorder=3)

######################################################## MUTIPLE POSITIONS - DM AND CML ###############################################################################

    elif (position == 'DMF & LDMF') | (position == 'LDMF & DMF'):
        # DEFENSIVE MIDFIELDER
        pitch.scatter(x=40, y=50, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)
        
        # CENTER MIDFIELDER LEFT
        pitch.scatter(x=55, y=36.8, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

######################################################## MUTIPLE POSITIONS - DM AND CMR ###############################################################################

    elif (position == 'RDMF & DMF') | (position == 'DMF, RDMF'):
        # DEFENSIVE MIDFIELDER
        pitch.scatter(x=40, y=50, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)
        
        # CENTER MIDFIELDER RIGHT
        pitch.scatter(x=55, y=36.8, ax=ax2, c=color[0], edgecolor='#1b1b1b', s=500, zorder=3)

######################################################## MUTIPLE POSITIONS - CML AND CMR ###############################################################################

    elif (position == 'LCMF, RCMF') | (position == 'RCMF, LCMF'):
        # CENTER MIDFIELDER RIGHT
        pitch.scatter(x=55, y=36.8, ax=ax2, c=color[0], edgecolor='#1b1b1b', s=500, zorder=3)
        
        # CENTER MIDFIELDER LEFT
        pitch.scatter(x=55, y=63.2, ax=ax2, c=color[0], edgecolor="#1b1b1b", s=500, zorder=3)

#######################################################################################################################################

    cols_Offensive = ['Finishing Ability', 'Concentration Ability', 'Create Chances Ability', 'Dribbling Ability', 'SetPieces Ability', 'Pass Ability', 'Aerial duels %', 'Key passes/90']
    cols_Defensive = ['Concentration Ability', 'Pass Ability', 'Aerial duels %', 'PAdj Interceptions', 'PAdj Sliding tackles', 'SetPieces Ability']


    if (isDefensive == True) & (setPieces == False):
        params = cols_Defensive

        cols_Defensive.remove('SetPieces Ability')
    
        player = df.loc[(df['Player'] == playerName) & (df['Comp'] == league)][cols_Defensive].reset_index()
        player = list(player.loc[0])
        player = player[1:]

    elif (isDefensive == True) & (setPieces == True):

        params = cols_Defensive

        player = df.loc[(df['Player'] == playerName) & (df['Comp'] == league)][cols_Defensive].reset_index()
        player = list(player.loc[0])
        player = player[1:]

    elif (isDefensive == False) & (setPieces == True):

        params = cols_Offensive

        player = df.loc[(df['Player'] == playerName) & (df['Comp'] == league)][cols_Offensive].reset_index()
        player = list(player.loc[0])
        player = player[1:]

    elif (isDefensive == False) & (setPieces == False):

        params = cols_Offensive

        cols_Offensive.remove('SetPieces Ability')
    
        player = df.loc[(df['Player'] == playerName) & (df['Comp'] == league)][cols_Offensive].reset_index()
        player = list(player.loc[0])
        player = player[1:]

    #######################################################################################################################################

    df2 = df.loc[(df['Comp'] == league) & (df['Position'] == position) & (df['Minutes played'] >= 500)].reset_index(drop=True)

    values = []
    for x in range(len(params)):   
        values.append(math.floor(stats.percentileofscore(df2[params[x]], player[x])))

    for n,i in enumerate(values):
        if i == 100:
            values[n] = 99
    
    elite = []
    veryStrong = []
    strong = []
    improve = []
    weak = []
    veryWeak = []
    for i in range(len(values)):
        if values[i] >= 90:
            elite.append(params[i])

        elif values[i] >= 80 | values[i] < 90:
            veryStrong.append(params[i])

        elif values[i] >= 70 | values[i] < 80:
            strong.append(params[i])

        elif values[i] >= 50 | values[i] < 70:
            improve.append(params[i])

        elif values[i] < 50:
            weak.append(params[i])

        elif values[i] <= 30:
            veryWeak.append(params[i])
        

    #######################################################################################################################################
    highlight_textpropsStrong =\
    [{"color": '#2ae102', "fontweight": 'bold'}]

    fig_text(x = 0.53, y = 0.9,
            s='Strengths',
            size=28,
            color='#2ae102')

    h=0.94
    for i in elite:
        ax_text(x=1.5, y=h - 0.1, s='<Elite:>' + ' ' + i, va='center', ha='center',
                highlight_textprops = highlight_textpropsStrong, size=18, color='#1b1b1b', ax=ax1)
        h=h-0.1

    h=h
    for i in veryStrong:
        ax_text(x=1.5, y=h - 0.1, s='<Very Strong:>' + ' ' + i, va='center', ha='center',
                highlight_textprops = highlight_textpropsStrong, size=18, color='#1b1b1b', ax=ax1)
        h=h-0.1

    h=h
    for i in strong:
        ax_text(x=1.5, y=h - 0.1, s='<Strong:>' + ' ' + i, va='center', ha='center',
                highlight_textprops = highlight_textpropsStrong, size=18, color='#1b1b1b', ax=ax1)
        h=h-0.1

    highlight_textprops =\
    [{"color": '#ff0000', "fontweight": 'bold'},
     {"color": '#f48515', "fontweight": 'bold'}]

    fig_text(x = 0.75, y = 0.9,
             s='<Weaknesses>/<To improve>',
             highlight_textprops = highlight_textprops,
             size=28)

    highlight_textpropsImprove =\
    [{"color": '#f48515', "fontweight": 'bold'}]

    highlight_textpropsWeak =\
    [{"color": '#ff0000', "fontweight": 'bold'}]

    h=0.94
    for i in improve:
        ax_text(x=2.5, y=h - 0.1, s='<Improve:>' + ' ' + i, va='center', ha='center',
                highlight_textprops = highlight_textpropsImprove, size=18, color='#1b1b1b', ax=ax1)
        h=h-0.1

    h=h
    for i in weak:
        ax_text(x=2.5, y=h - 0.1, s='<Weak:>' + ' ' + i, va='center', ha='center',
                highlight_textprops = highlight_textpropsWeak, size=18, color='#1b1b1b', ax=ax1)
        h=h-0.1

    h=h
    for i in veryWeak:
        ax_text(x=2.5, y=h - 0.1, s='<Very Weak:>' + ' ' + i, va='center', ha='center',
                highlight_textprops = highlight_textpropsWeak, size=18, color='#1b1b1b', ax=ax1)
        h=h-0.1
        
    #######################################################################################################################################

    fig_text(x = 0.23, y = 0.91,
            s=playerName,
            size=30,
            color='#1b1b1b')

    fig_text(x = 0.23, y = 0.75,
            s='Club: ',
            size=20,
            color='#1b1b1b')

    fig_text(x = 0.21, y = 0.71,
            s='League: ',
            size=20,
            color='#1b1b1b')

    fig_text(x = 0.16, y = 0.67,
            s='Market Value: ',
            size=20,
            color='#1b1b1b')

    fig_text(x = 0.15, y = 0.63,
            s='Contract until: ',
            size=20,
            color='#1b1b1b')

    fig_text(x = 0.15, y = 0.59,
            s='Minutes played: ',
            size=20,
            color='#1b1b1b')

    fig_text(x = 0.223, y = 0.55,
            s='Height: ',
            size=20,
            color='#1b1b1b')

    fig_text(x = 0.233, y = 0.51,
            s='Foot: ',
            size=20,
            color='#1b1b1b')

#######################################################################################################################################

    highlight_textprops =\
    [{"color": color[0], "fontweight": 'bold'}]

    fig_text(x = 0.3, y = 0.75,
            s=f'<{club}>',
            highlight_textprops = highlight_textprops,
            size=18,
            color='#1b1b1b')

    fig_text(x = 0.301, y = 0.71,
            s=league,
            size=18,
            color='#1b1b1b')

    fig_text(x = 0.301, y = 0.67,
            s=Market,
            size=18,
            color='#1b1b1b')

    if 'M' not in Market:
        fig_text(x = 0.33, y = 0.667,
                s='Thousand',
                size=11,
                color='#1b1b1b')

    fig_text(x = 0.301, y = 0.63,
            s=Contract,
            size=18,
            color='#1b1b1b')

    fig_text(x = 0.301, y = 0.59,
            s=str(Minutes),
            size=18,
            color='#1b1b1b')

    fig_text(x = 0.301, y = 0.55,
            s=Height,
            size=18,
            color='#1b1b1b')

    fig_text(x = 0.301, y = 0.51,
            s=Foot,
            size=18,
            color='#1b1b1b')

#######################################################################################################################################

    fig_text(x = 0.47, y = 0.41,
            s='<Main Position>',
            highlight_textprops = highlight_textprops,
            size=18,
            color='#1b1b1b')

    if (position.split(', ')[0] == 'RAMF') | (position == 'RAMF'):
        fig_text(x = 0.423, y = 0.38,
                s='RIGHT MIDFIELDER',
                size=18,
                color='#1b1b1b')

    elif (position.split(', ')[0] == 'LAMF') | (position == 'LAMF'):
        fig_text(x = 0.423, y = 0.38,
                s='LEFT MIDFIELDER',
                size=18,
                color='#1b1b1b')
    
    elif (position.split(', ')[0] == 'CF') | (position == 'CF'):
        fig_text(x = 0.423, y = 0.38,
                s='FORWARD',
                size=18,
                color='#1b1b1b')
    
    elif (position.split(', ')[0] == 'RW') | (position == 'RW'):
        fig_text(x = 0.423, y = 0.38,
                s='RIGHT WINGER',
                size=18,
                color='#1b1b1b')

    elif (position.split(', ')[0] == 'LW') | (position == 'LW'):
        fig_text(x = 0.423, y = 0.38,
                s='LEFT WINGER',
                size=18,
                color='#1b1b1b')

    elif (position.split(', ')[0] == 'LB') | (position == 'LB'):
        fig_text(x = 0.423, y = 0.38,
                s='LEFT BACK',
                size=18,
                color='#1b1b1b')
    
    elif (position.split(', ')[0] == 'RB') | (position == 'RB'):
        fig_text(x = 0.423, y = 0.38,
                s='RIGHT BACK',
                size=18,
                color='#1b1b1b')
    
    elif (position.split(', ')[0] == 'LCB') | (position == 'LCB'):
        fig_text(x = 0.423, y = 0.38,
                s='LEFT CENTER BACK',
                size=18,
                color='#1b1b1b')
    
    elif (position.split(', ')[0] == 'RCB') | (position == 'RCB'):
        fig_text(x = 0.423, y = 0.38,
                s='RIGHT CENTER BACK',
                size=18,
                color='#1b1b1b')

    elif (position.split(', ')[0] == 'DMF') | (position == 'DMF'):
        fig_text(x = 0.423, y = 0.38,
                s='DEFENSIVE MIDFIELDER',
                size=18,
                color='#1b1b1b')

    elif (position.split(', ')[0] == 'RCMF') | (position == 'RCMF'):
        fig_text(x = 0.423, y = 0.38,
                s='CENTER MIDFIELDER RIGHT',
                size=18,
                color='#1b1b1b')


    elif (position.split(', ')[0] == 'LCMF') | (position == 'LCMF'):
        fig_text(x = 0.423, y = 0.38,
                s='CENTER MIDFIELDER LEFT',
                size=18,
                color='#1b1b1b')

    elif (position.split(', ')[0] == 'AMF') | (position == 'AMF'):
        fig_text(x = 0.423, y = 0.38,
                s='OFFENSIVE MIDFIELDER',
                size=18,
                color='#1b1b1b')

    elif (position.split(' &')[0] == 'GK') | (position == 'GK'):
        fig_text(x = 0.423, y = 0.38,
                s='GOALKEEPER',
                size=18,
                color='#1b1b1b')
                
    #######################################################################################################################################
    dfPlayer = df.loc[df['Player'] == playerName].reset_index(drop=True)

    playerRole = dfPlayer[['False 9', 'Target Man', 'Advanced Forward', 'Ball Winner', 'Deep Lying Playmaker',
                                                        'Attacking Playmaker', 'Box-to-box','Attacking FB', 'Defensive FB',
                                                        'Wing Back', 'Inverted Wing Back', 'Stopper', 'Aerial CB', 'Ball Playing CB',
                                                        'Ball Carrying CB']].max(axis=0).sort_values(ascending=False)


    # PLAYER ROLE   
    #playerRole.index[0]

    fig_text(x = 0.17, y = 0.4,
            s='Final Rating',
            size=16,
            color='#1b1b1b')

    if playerRole[0] >= 75:
        fig_text(x = 0.25, y = 0.38,
                s='A',
                size=100,
                color='#2ae102')

    elif (playerRole[0] >= 65) & (playerRole[0] < 75):
        fig_text(x = 0.25, y = 0.38,
                s='B',
                size=100,
                color='#d7ee1a')

    elif (playerRole[0] >= 50) & (playerRole[0] < 65):
        fig_text(x = 0.25, y = 0.38,
                s='C',
                size=100,
                color='#fdab16')

    elif playerRole[0] < 50:
        fig_text(x = 0.25, y = 0.38,
                s='D',
                size=100,
                color='#ff0000')

    fig = add_image(image='Images/Players/' + league + '/' + club + '/' + playerName + '.png', fig=fig, left=0.12, bottom=0.78, width=0.1, height=0.23)

    fig = add_image(image='Images/Country/' + country + '.png', fig=fig, left=0.23, bottom=0.775, width=0.1, height=0.07)


def role_Chart(df, playerName, pos):
    # parameter and value list
    if pos == 'Center Back':
        params = ['Ball Playing CB', 'Ball Carrying CB', 'Stopper', 'Aerial CB']

    elif pos == 'Full Back':
        params = ['Defensive FB', 'Inverted Wing Back', 'Wing Back', 'Attacking FB']

    elif pos == 'Midfielder':
        params = ['Box-to-box', 'Attacking Playmaker', 'Deep Lying Playmaker', 'Ball Winner']

    elif pos == 'Forward':
        params = ['Advanced Forward', 'Target Man', 'False 9']

    players = df.loc[df['Player'] == playerName]

    club = players.Team.unique()
    club = club.tolist()
    club = club[0]

    league = players.Comp.unique()
    league = league.tolist()
    league = league[0]

    #Valores que pretendemos visualizar no radar chart, acedemos ao index 0 para obtermos os valores dentro da lista correta
    values = players[params].values[0]

    # instantiate PyPizza class
    baker = PyPizza(
        params=params,                  # list of parameters
        straight_line_color="#F2F2F2",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        straight_line_limit=100.0,        # max limit of straight lines
        last_circle_lw=0,               # linewidth of last circle
        other_circle_lw=0,              # linewidth for other circles
        inner_circle_size=0.4,          # size of inner circle
    )

    # plot pizza
    fig, ax = baker.make_pizza(
        values,                     # list of values
        figsize=(8, 8),             # adjust figsize according to your need
        color_blank_space="same",   # use same color to fill blank space
        blank_alpha=0.4,            # alpha for blank-space colors
        param_location=104.7,         # where the parameters will be added
        kwargs_slices=dict(
            facecolor="#043484", edgecolor="#F2F2F2",
            zorder=2, linewidth=1
        ),                          # values to be used when plotting slices
        kwargs_params=dict(
            color="#000000", fontsize=12,
            va="center"
        ),                          # values to be used when adding parameter
        kwargs_values=dict(
            color="#000000", fontsize=12,
            zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="#043484",
                boxstyle="round,pad=0.2", lw=1
            )
        )                           # values to be used when adding parameter-values
    )

    fig.set_facecolor('#E8E8E8')

    fig_text(s =  playerName,
                x = 0.5, y = 1.07,
                color='#181818',
                fontweight='bold', ha='center',
                fontsize=28)

    fig_text(s =  'Rank vs Players Position | Season 21/22',
                x = 0.5, y = 1.02,
                color='#181818',
                fontweight='bold', ha='center',
                fontsize=12)
    
    # add image player
    add_image('Images/Players/' + league + '/' + club + '/' + playerName + '.png', fig, left=0.12, bottom=0.95, width=0.12, height=0.14)

    # add image club
    add_image('Images/Clubs/' + league + '/' + club + '.png', fig, left=0.82, bottom=0.97, width=0.10, height=0.10)







