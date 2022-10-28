import pandas as pd

import pymysql

import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, Integer, Float, Boolean
from sqlalchemy import MetaData
from sqlalchemy import select

import math
import ipywidgets as widgets

from pandas.core.common import SettingWithCopyWarning
from IPython.display import display, Math, Latex

import tqdm as tqdm
import os

import warnings
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


def toCSV(url):
    df = pd.read_csv(url)

    return df

def getDataAthletic():
    dataHome = []
    dataAway = []
    dataEvents = []
    data = []
    Match_ID = 0
    for file in tqdm.tqdm(os.listdir(r'Data/Home/Athletic')):
        if file.endswith('.csv'):

            players = toCSV('Data/Home/Athletic/' + file)
            players.drop(columns=['Unnamed: 0'], inplace=True)
            players.fillna(0, inplace=True)
            players = players[['playerId', 'name', 'shirtNo']]
            players.drop_duplicates(inplace=True)

            players = pd.concat([players], axis=0, ignore_index=True)

            dataHome.append(players)

    for file in tqdm.tqdm(os.listdir(r'Data/Away/Athletic')):
        if file.endswith('.csv'):

            playersAway = toCSV('Data/Away/Athletic/' + file)
            playersAway.drop(columns=['Unnamed: 0'], inplace=True)
            playersAway.fillna(0, inplace=True)
            playersAway = playersAway[['playerId', 'name', 'shirtNo']]
            playersAway.drop_duplicates(inplace=True)

            playersAway = pd.concat([playersAway], axis=0, ignore_index=True)

            dataAway.append(playersAway)

    for file in tqdm.tqdm(os.listdir(r'Data/Events/Athletic')):
        if file.endswith('.csv'):

            eventsDF = toCSV('Data/Events/Athletic/' + file)

            eventsDF.rename(columns={'type.displayName': 'typedisplayName',
                                'outcomeType.displayName': 'outcomeTypedisplayName'}, inplace=True)

            eventsDF.drop(columns=['Unnamed: 0'], inplace=True)
            eventsDF.fillna(0, inplace=True)
            eventsDF.drop_duplicates(inplace=True)

            eventsDF['Match_ID'] = Match_ID + 1

            eventsDF = pd.concat([eventsDF], axis=0, ignore_index=True)

            dataEvents.append(eventsDF)

            Match_ID = Match_ID + 1

    playersHome = pd.concat(dataHome)

    playersAway = pd.concat(dataAway)

    playersHome_Away = pd.concat([playersHome, playersAway], axis=0)

    events = pd.concat(dataEvents)

    eventsPlayers = events.merge(playersHome_Away[['playerId', 'name', 'shirtNo']], on='playerId').reset_index(drop=True)
    eventsPlayers.drop(eventsPlayers.index[0], axis=0, inplace=True)
    eventsPlayers.drop_duplicates(inplace=True)
    eventsPlayers.fillna(0, inplace=True)
    eventsPlayers.reset_index(drop=True, inplace=True)
    #eventsPlayers.sort_values(by=['Match_ID'], ascending=True)

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

    clubColors = {'Corinthians' : '#ff0000',
                'Avai' : '#00679a',
                'Flamengo' : '#ff0000',
                'Palmeiras' : '#046434',
                'Manchester City' : ['#7bb1d8', '#062e63'],
                'Liverpool' : ['#d40424', '#e2e1ab'],
                'Norwich City' : ['#00a650', '#fff200'],
                'Villarreal' : ['#f2e166', '#065283'],
                'Athletic Club' : ['#ff0000', 'white'],
                'Real Madrid' : ['#1a346e', 'white'],
                'FC Barcelona' : ['#c2043a', '#06274c'],
                'Deportivo Alavés' : ['#7bb1d8', 'white']}

    La_Liga = ['Athletic Club', 'FC Barcelona', 'Real Madrid', 'Atlético Madrid', 'Sevilla', 'Real Sociedad', 'Villareal', 'Valencia', 'Real Betis',
            'Getafe', 'Espanyol', 'Celta Vigo', 'Osasuna', 'Mallorca', 'Deportivo Alavés', 'Elche', 'Cádiz', 'Rayo Vallecano']

    Ligue1 = ['PSG', 'Lille', 'Rennes', 'Montepellier', 'Monaco', 'Lyon', 'Lens', 'Marselha']

    Bundesliga = ['Bayern', 'Dortmund', 'Leipzig', 'Leverkusen', 'Wolfsburg', 'Monchengladbach', 'Hoffenheim', 'Frankfurt', 'Stuttgart', 'Freiburg', 'Mainz', 'Auhsburg',
                'Hertha', 'Koln', 'Union Berlim', 'Arminia Bielfield', 'Bochum']

    PremierLeague = ['Manchester City', 'Liverpool', 'Chelsea', 'Tottenham', 'Arsenal', 'West Ham', 'Man United', 'Wolves', 'Aston Villa', 'Newcastle', 'Leicester',
                    'Everton', 'Leeds', 'Southampton', 'Crystal Palace', 'Brighton', 'Brentford', 'Norwich', 'Watford', 'Burnley']

    SerieA = ['Milan', 'Inter', 'Juventus', 'Napoli', 'Roma', 'Lazio', 'Fiorentina', 'Sassuolo', 'Spezia', 'Atalanta', 'Torion', 'Bologna',
            'Cagliari', 'Verona', 'Genoa', 'Udinese', 'Sampdoria', 'Empoli', 'Venezia', 'Salernitana']

    Brasil = ['Flamengo', 'Corinthians', 'São Paulo', 'Santos', 'Internacional', 'Botafogo', 'Santos', 'Red Bull Bragantino', 'Atlético Mineiro']

    eventsPlayers['League'] = None

    for x in La_Liga:
        if x in eventsPlayers.team.unique():
            eventsPlayers['League'] = 'La Liga'

    for x in Bundesliga:
        if x in eventsPlayers.team.unique():
            eventsPlayers['League'] = 'Bundesliga'

    for x in PremierLeague:
        if x in eventsPlayers.team.unique():
            eventsPlayers['League'] = 'Premier League'

    for x in Ligue1:
        if x in eventsPlayers.team.unique():
            eventsPlayers['League'] = 'Ligue 1'
            
    for x in SerieA:
        if x in eventsPlayers.team.unique():
            eventsPlayers['League'] = 'Serie A'
            
    for x in Brasil:
        if x in eventsPlayers.team.unique():
            eventsPlayers['League'] = 'Brasileirao'

    data.append(eventsPlayers)

    # see pd.concat documentation for more info
    eventsPlayers = pd.concat(data)

    return eventsPlayers

#Function that read csv file and join them to our table in sql
def connect_csv_SQL(csvFile, tableName, connection, if_exists, index):
    df = pd.read_csv(csvFile)

    df.drop(['Unnamed: 0'], axis=1, inplace=True)

    df.to_sql(name=tableName, con=connection, if_exists=if_exists, index=index)