#!/usr/bin/python

import requests
import pandas as pd
import os

# Script qui recupere la data des games en ligne (et bientot customs) de LoL et les insere dans un fichier excel

RIOT_API_KEY= os.getenv("RIOT_API")
EXCEL_PATH = "/matches/matches.xlsx"
TXT_PATH = "/matches/matches.txt"

match_id = input("Entrer l'id de la game : ")
print("Regions disponibles EUW1, EUN1, NA1, KR, BR1, LA1, LA2, OC1, JP1, TR1, RU (de base EUW1)")
region = input("Entrer la region : ").strip().upper() or "EUW1"

def fetch_data(match_id, region):
    id_cmplt = f"{region}_{match_id}"
    url = f"https://{region.lower()}.api.riotgames.com/lol/match/v5/matches/{id_cmplt}"
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
            #"Pings": joueur['enemyMissingPings'],
            "Win": joueur['win'],
            "dgt": joueur['totalDamageDealt']
        })
    
    return pd.DataFrame(rows)
'''
def save_excel(dataframe, EXCEL_PATH):
    try: 
        if not os.path.exists(EXCEL_PATH):
            with pd.ExcelWriter(EXCEL_PATH, mode='w', engine='openpyxl') as writer:
                dataframe.to_excel(writer, index=False, sheet_name="Match data")
        else: 
            with pd.ExcelWriter(EXCEL_PATH, mode='a', engine='openpyxl') as writer:
                dataframe.to_excel(writer, index=False, sheet_name="Match data")    

    except Exception as e:
        print(f"Erreur lors de l'enregistrement du fichier : {e}")
''' 

def save_txt(data, TXT_PATH):
    try:
        with open(TXT_PATH, 'w', encoding='utf-8') as f:
            f.write(data)
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du fichier : {e}")

if __name__ == "__main__":
    try: 

        print("Recuperation des donnees...")
        match_datares = fetch_data(match_id, region)
        
        df = match_data(match_datares)

        print("Sauvegarde dans le fichier excel...")
        #save_excel(df, EXCEL_PATH)
        save_txt(str(df), TXT_PATH)
    except Exception as e:
        print('Erreur : ', e)