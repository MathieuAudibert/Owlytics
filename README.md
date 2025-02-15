# Fetch custom data with Owlytics 🦉

Currently not working on customs due to 

![https://riot-api-libraries.readthedocs.io/en/latest/specifics.html#match](/public/img/image.png)

Working on ranked tho !

## Requirements
- Python
- Riot api key : https://developer.riotgames.com/

## Usage 

1. Clone the repository
2. Run `pip install -r requirements.txt`
3. Create a .env file and write this inside: RIOT_API="RGAPI-YOURRIOTAPI" (wich you can claim on https://developer.riotgames.com/)
4. Create a folder "matches" inside `/utils` and then inside "matches.xlsx" "matches.txt" 
5. Run the launcher (in `/utils`) with `python launcher.py`
6. You can retrieve your game id by going in the league client > Profile > Match History > The game you want to retrieve data about > Game ID 

   ![img](/public/img/image-1.png)

7. Get the data in either matches/matches.xlsx or matches/matches.txt
