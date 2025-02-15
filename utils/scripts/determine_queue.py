#!/usr/bin/python

# Script qui determine si vous etes dans la "Looser's Queue" ou "Winners Queue" de League Of Legends en fonction de multiples parametres
# Looser's Queue : concept inventé par les joueurs de LoL pour expliquer la malchance qu'ils ont en jeu (RiotGames les placerait dans une queue de perdants)
# Winner's Queue : ^

import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

RIOT_API_KEY = os.getenv("RIOT_API")

def get_puuid(summonerId=None, gameName=None, tagLine=None, region="europe"):
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
        url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={RIOT_API_KEY}"
        res = requests.get(url)
        return res.json()['puuid']

def get_idtag(puuid=None):
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={RIOT_API_KEY}"
    res = requests.get(url)
    id = {
        'gameName': res.json()['gameName'],
        'tagLine': res.json()['tagLine']
    }
    return id

def get_match_history(puuid=None, region=None):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=5&api_key={RIOT_API_KEY}"
    res = requests.get(url)
    return res.json()

def get_match_participants(match_id=None, region=None):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={RIOT_API_KEY}"
    res = requests.get(url)
    if 'status' in res.json() and res.json()['status']['status_code'] == 429:
        print(f"Rate limit exceeded. Retrying after delay for match_id {match_id}")
        time.sleep(2)  
        return get_match_participants(match_id, region)
    if 'info' not in res.json():
        print(f"Error: 'info' key not found in response for match_id {match_id}")
        return [], []
    teamw = []
    teamd = []
    for pl in res.json()['info']['participants']:
        if pl['win']:
            teamw.append({'puuid': pl['puuid']})
        else:
            teamd.append({'puuid': pl['puuid']})
    return teamd, teamw

def get_history_wr(puuid=None, region=None):
    wr = 0
    matches = get_match_history(puuid, region)
    for match_id in matches:
        url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={RIOT_API_KEY}"
        res = requests.get(url)
        if 'status' in res.json() and res.json()['status']['status_code'] == 429:
            print(f"Rate limit exceeded. Retrying after delay for match_id {match_id}")
            time.sleep(2)  
            continue
        if 'info' not in res.json():
            print(f"Error: 'info' key not found in response for match_id {match_id}")
            continue
        for wl in res.json()['info']['participants']:
            if wl['puuid'] == puuid:
                if wl['win']:
                    wr += 1
    return wr

def get_wr_participants_lastgames(puuid=None, region=None):
    histo = get_match_history(puuid, region)
    wr_dict = {}
    for match_id in histo:
        teamd, teamw = get_match_participants(match_id, region)
        for pl in teamd + teamw:
            player_puuid = pl['puuid']
            if player_puuid not in wr_dict:
                wr_dict[player_puuid] = get_history_wr(player_puuid, region)
    return wr_dict

if __name__ == "__main__":
    try:
        print("* = optionnel")
        name = input("Entrer votre nom de joueur (ex: Roi Cap): ")
        tagline = input("Entrer votre riot tag SANS LE HASHTAG (ex: #EUW): ")
        summonerId = None
        puuid = get_puuid(summonerId, name, tagline)

        historique = get_match_history(puuid, "europe")
        print(historique)

        wr = get_history_wr(puuid, "europe")
        print(f"Votre winrate sur les 5 dernieres games est de : {wr}")

        wr_participants = get_wr_participants_lastgames(puuid, "europe")
        print(wr_participants)
    except Exception as e:
        print(f"Erreur lors de la recuperation des donnees : {e}")
