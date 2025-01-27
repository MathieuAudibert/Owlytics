#!/usr/bin/python

# Script qui recupere la data des games en ligne (et bientot customs) de LoL et les insere dans un fichier excel

import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
RIOT_API_KEY= os.getenv("RIOT_API")
EXCEL_PATH = "matches/matches.xlsx"
TXT_PATH = "matches/matches.txt"
REGION_MAPPING = {
    "EUW1": "europe",
    "EUN1": "europe",
    "TR1": "europe",
    "RU": "europe",
    "NA1": "americas",
    "BR1": "americas",
    "LA1": "americas",
    "LA2": "americas",
    "KR": "asia",
    "JP1": "asia",
    "OC1": "sea"
}
match_id = input("Entrer l'id de la game : ")
print("Regions disponibles : EUW1, EUN1, NA1, KR, BR1, LA1, LA2, OC1, JP1, TR1, RU (par défaut : EUW1)")
region = input("Entrer la region : ").strip().upper() or "EUW1"
region_prefix = REGION_MAPPING.get(region, "europe")

def fetch_data(match_id, region, region_prefix):
    id_cmplt = f"{region}_{match_id}"
    url = f"https://{region_prefix}.api.riotgames.com/lol/match/v5/matches/{id_cmplt}"
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
    os.makedirs(os.path.dirname(TXT_PATH), exist_ok=True)  
    try:
        with open(TXT_PATH, 'w', encoding='utf-8') as f:
            f.write(data)
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du fichier : {e}")

if __name__ == "__main__":
    try: 

        print("Recuperation des donnees...")
        match_data_res = fetch_data(match_id, region, region_prefix)
        
        df = match_data(match_data_res)

        print("Sauvegarde dans le fichier excel...")
        #save_excel(df, EXCEL_PATH)
        save_txt(df.to_string(index=False), TXT_PATH)
    except Exception as e:
        print('Erreur : ', e)