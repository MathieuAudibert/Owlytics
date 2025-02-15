#!/usr/bin/python
 
# Script qui determine si vous etes dans la "Looser's Queue" ou "Winners Queue" de League Of Legends en fonction de multiples parametres
# Looser's Queue : concept inventé par les joueurs de LoL pour expliquer la malchance qu'ils ont en jeu (RiotGames les placerait dans une queue de perdants)
# Winner's Queue : ^

# Determinants : 
# 5 dernieres games de l'equipe du joueur
# 5 dernieres games du joueur
# 5 dernieres games de l'equipe adverse
# wr moyen de l'equipe du joueur
# wr moyen de l'equipe adverse
from dotenv import load_dotenv
load_dotenv()

import requests
import pandas as pd
import os

RIOT_API_KEY= os.getenv("RIOT_API")

def get_puuid(summonerId=None, gameName=None, tagLine=None, region="EUW1"):
    """ Recupere le player user id puuid en fonction de son id de joueur ou son nom#tag

    Args: 
        summonerId (str): id du joueur
        gameName (str): nom du joueur
        tagLine (str): tag du joueur
        region (str): region du joueur
    
    Returns:    
        puuid (str): player user id
    """
    if summonerId is not None: 
        url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summonerId}?api_key={RIOT_API_KEY}"
        res = requests.get(url)
        return res.json()['puuid']
    else:
        url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/a/{gameName}/{tagLine}?api_key={RIOT_API_KEY}"
        res = requests.get(url)
        return res.json()['puuid']

def get_idtag(puuid=None):
    """ Recupere le idtag du joueur en fonction de son puuid

    Args: 
        puuid (str): player user id
    
    Returns:    
        idtag (dict): dictionnaire contenant le nom et le tag du joueur
    """
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={RIOT_API_KEY}"
    res = requests.get(url)
    
    id = {
        'gameName': res.json()['gameName'],
        'tagLine': res.json()['tagLine']
    }

    return id

def get_match_history(puuid=None, region=None):
    """ Recupere l'historique des games du joueur en fonction de son puuid

    Args: 
        puuid (str): player user id
        region (str): region du joueur
    
    Returns:    
        match_history (dict): dictionnaire contenant l'historique des games du joueur
    """
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=5&api_key={RIOT_API_KEY}"
    res = requests.get(url)
    return res.json()

def get_match_participants(match_id=None, region=None):
    """ Recupere les participants d'une game en fonction de son id et de la region

    Args: 
        match_id (str): id de la game
        region (str): region de la game
    
    Returns:    
        match_data (dict): dictionnaire contenant les participants de la game
    """
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={RIOT_API_KEY}"
    res = requests.get(url)
    
    for pl in res.json()['info']['participants']:
        if pl['win'] == True:
            teamw = {'puuid' : pl['puuid']}
        else:
            teamd = {'puuid' : pl['puuid']}
        data = teamw, teamd
    return data  

def get_wr_participants_lastgames(puuid=None, region=None):
    """ Recupere le winrate des participants des 5 dernieres games du joueur

    Args: 
        puuid (str): player user id
        region (str): region du joueur
    
    Returns:    
        wr (dict): dictionnaire contenant le winrate des participants des 5 dernieres games du joueur
    """
    match_history = get_match_history(puuid=puuid, region=region)
    wr = "0%"
    

    