import pandas as pd

import warnings
warnings.filterwarnings("ignore")

from pandas.core.common import SettingWithCopyWarning

import warnings
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

import matplotlib as plt
from matplotlib import font_manager

font_path = 'Fonts/Gagalin-Regular.otf'
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

#Courier New

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()

#############################################################################################################################################################

eventsPlayers = pd.read_csv('Data/opta/optaData.csv')

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
              'Flamengo' : ['#ff0000', '#181818'],
              'Palmeiras' : ['#046434', '#e8e8e8'],
              ###################################
              'Manchester City' : ['#7bb1d8', '#062e63'],
              'Liverpool' : ['#d40424', '#e2e1ab']}

def optaTable(df):
    #Criação das listas para cada evento
    Pass = []

    Aerial = []

    Foul = []

    BallRecovery = []

    BallTouch = []

    BlockedPass = []

    Challenge = []

    Clearance = []

    Interception = []

    Dispossessed = []

    TakeOn = []

    Goal = []

    #Criação da lista de jogadores
    teamID = df['teamId'].unique()

    teamID = teamID.tolist()


    #Criação dos dataFrames para cada evento
    Pass_Sum = df.loc[df['typedisplayName'] == 'Pass']
    
    Aerial_Sum = df.loc[df['typedisplayName'] == 'Aerial']

    Foul_Sum = df.loc[df['typedisplayName'] == 'Foul']

    BallRecovery_Sum = df.loc[df['typedisplayName'] == 'BallRecovery']

    BallTouch_Sum = df.loc[df['typedisplayName'] == 'BallTouch']

    BlockedPass_Sum = df.loc[df['typedisplayName'] == 'BlockedPass']

    Challenge_Sum = df.loc[df['typedisplayName'] == 'Challenge']

    Clearance_Sum = df.loc[df['typedisplayName'] == 'Clearance']

    Interception_Sum = df.loc[df['typedisplayName'] == 'Interception']

    Dispossessed_Sum = df.loc[df['typedisplayName'] == 'Dispossessed']

    TakeOn_Sum = df.loc[df['typedisplayName'] == 'TakeOn']

    Goal_Sum = df.loc[df['typedisplayName'] == 'Goal']

    #Ciclo For de atribuição dos valores a cada jogador
    for team in teamID:
        Pass.append(Pass_Sum.loc[Pass_Sum['teamId'] == team, 'typedisplayName'].count())
        Aerial.append(Aerial_Sum.loc[Aerial_Sum['teamId'] == team, 'typedisplayName'].count())
        Foul.append(Foul_Sum.loc[Foul_Sum['teamId'] == team, 'typedisplayName'].count())
        BallRecovery.append(BallRecovery_Sum.loc[BallRecovery_Sum['teamId'] == team, 'typedisplayName'].count())
        BallTouch.append(BallTouch_Sum.loc[(BallTouch_Sum['teamId'] == team), 'typedisplayName'].count())
        BlockedPass.append(BlockedPass_Sum.loc[(BlockedPass_Sum['teamId'] == team), 'typedisplayName'].count())
        Challenge.append(Challenge_Sum.loc[(Challenge_Sum['teamId'] == team), 'typedisplayName'].count())
        Clearance.append(Clearance_Sum.loc[(Clearance_Sum['teamId'] == team), 'typedisplayName'].count())
        Interception.append(Interception_Sum.loc[(Interception_Sum['teamId'] == team), 'typedisplayName'].count())
        Dispossessed.append(Dispossessed_Sum.loc[(Dispossessed_Sum['teamId'] == team), 'typedisplayName'].count())
        TakeOn.append(TakeOn_Sum.loc[(TakeOn_Sum['teamId'] == team), 'typedisplayName'].count())
        Goal.append(Goal_Sum.loc[(Goal_Sum['teamId'] == team), 'typedisplayName'].count())

    data = {
    'TakeOn' : TakeOn,
    'Goal' : Goal,
    'Passes' : Pass,
    'Aerial' : Aerial,
    'Foul' : Foul,
    'BallRecovery' : BallRecovery,
    'BallTouch' : BallTouch,
    'BlockedPass' : BlockedPass,
    'Challenge' : Challenge,
    'Clearance' : Clearance,
    'Interception' : Interception,
    'Dispossessed' : Dispossessed,
    }

    df = pd.DataFrame(data)

    return df