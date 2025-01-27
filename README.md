# Fetch custom data

Currently not working on customs due to 

![https://riot-api-libraries.readthedocs.io/en/latest/specifics.html#match](image.png)

Working on ranked tho !

## Requirements
- Python
- Riot api key : https://developer.riotgames.com/

## Usage 

1. Clone the repo
2. Run `pip install requests pandas openpyxl`
3. Create a .env file and write this inside: RIOT_API="RGAPI-YOURRIOTAPI"
4. Create a folder "matches" and then inside "matches.xlsx" "matches.txt" 
5. Run the script with `python script.py`
6. Get the data in either matches/matches.xlsx or matches/matches.txt