import os

def main():
    ascii = """  
                                                                                ,___,
                                                                                [OvO]  
                                                                                /)__)  
                                                                                --"--
                 ▄██████▄   ▄█     █▄   ▄█       ▄██   ▄       ███      ▄█   ▄████████    ▄████████ 
                ███    ███ ███     ███ ███       ███   ██▄ ▀█████████▄ ███  ███    ███   ███    ███ 
                ███    ███ ███     ███ ███       ███▄▄▄███    ▀███▀▀██ ███▌ ███    █▀    ███    █▀  
                ███    ███ ███     ███ ███       ▀▀▀▀▀▀███     ███   ▀ ███▌ ███          ███        
                ███    ███ ███     ███ ███       ▄██   ███     ███     ███▌ ███        ▀███████████ 
                ███    ███ ███     ███ ███       ███   ███     ███     ███  ███    █▄           ███ 
                ███    ███ ███ ▄█▄ ███ ███▌    ▄ ███   ███     ███     ███  ███    ███    ▄█    ███ 
                 ▀██████▀   ▀███▀███▀  █████▄▄██  ▀█████▀     ▄████▀   █▀   ████████▀   ▄████████▀ 

                 
    """

    print(ascii)

    while True:        
        print("Select your script:")
        print("             (1) Determine if you are in loosersQ or not")
        print("             (2) Fetch datas about a game with GameID")

        choix = input("Choice: ")
        if choix == "1":
            os.system("python3 scripts/determine_queue.py")
        elif choix == "2":
            os.system("python3 scripts/get_gameById.py")
        else:
            print("Choix invalide")

if __name__ == "__main__":
    main()