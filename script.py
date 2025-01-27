#!/usr/bin/python

import requests
import pandas as pd
import os

# Script qui recupere la data des games customs de LoL et les insere dans un fichier excel

RIOT_API_KEY= os.getenv("RIOT_API")
EXCEL_PATH= os.getenv("EXCEL_PATH")

match_id = input("Entrer l'id de la game : ")

def fetch_data(match_id):
    url = f"https://euw1.api.riotgames.com/lol/matches/v5/matches/{match_id}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        print(f"Error : {res.status_code}, {res.json()}")
        return None
    
    return res.json()

def match_data(data):
    rows = []

    for joueur in data['info']['participants']:
        rows.append({
            "Joueur": joueur['summonerName'],
            "Champion": joueur['championName'],
            "Kills": joueur['kills'],
            "Deaths": joueur['deaths'],
            "Assists": joueur['assists'],  
            "Pings": joueur['enemyMissingPings'],
            "Win": joueur['win'],
            "kda": joueur['kda'],
            "dgt": joueur['totalDamageDealt']
        })
        return pd.DataFrame(rows)

def save_excel(dataframe, EXCEL_PATH):
    try: 
        with pd.ExcelWriter(EXCEL_PATH, mode='a', if_sheet_exists='replace') as writer:
            dataframe.to_excel(writer, index=False, sheet_name="https://github.com/MathieuAudibert/Data-5V5-intso")
        print(f'Fichier enregistrer avec succes : {EXCEL_PATH}')
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du fichier : {e}")
    
if __name__ == "__main__":
    try: 
        print("Recuperation des donnees...")
        match_data = fetch_data(match_id)
        
        df = match_data(match_data)

        print("Sauvegarde dans le fichier excel...")
        save_excel(df, EXCEL_PATH)
    except Exception as e:
        print('Erreur : ', e)