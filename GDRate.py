import requests
import base64
import os
from itertools import cycle

def xor_cipher(input_string, key):
    return ''.join(chr(ord(c)^ord(k)) for c,k in zip(input_string, cycle(key)))

def main():
    global databaseUrl
    global accessSecret
    global modSecret
    global accountID
    global encoded_base64

    databaseUrl = "http://www.boomlings.com/database/"

    xorKey = "37526"

    accessSecret = "Wmfd2893gb7"
    modSecret = "Wmfp3897gc3"


    databaseUrlRequest = input(f"Please enter your database URL (Press ENTER to keep '{databaseUrl}'): ")

    if databaseUrlRequest != "":
        databaseUrl = databaseUrlRequest

    print(f"Database URL: {databaseUrl}\n")

    accountID = input("Account ID: ")
    password = input("Password: ")

    encoded = xor_cipher(password, xorKey)
    encoded_base64 = base64.b64encode(encoded.encode()).decode()
    encoded_base64 = encoded_base64.replace("+", "-")
    encoded_base64 = encoded_base64.replace("/", "_")
    try:
        headers = {
            "User-Agent": ""
        }
        data = {
            "accountID": accountID,
            "gjp": encoded_base64,
            "secret": accessSecret,
            "gameVersion": 22,
            "binaryVersion": 38,
            "gdw": 0
        }
        req = requests.post(f'{databaseUrl}requestUserAccess.php', data=data, headers=headers)
        os.system('cls' if os.name == 'nt' else 'clear')
        if req.text == "-1":
            print("You are not a Moderator!")
            main()
        
        elif req.text == "1":
            print("You are now logged in as a Moderator")
            rateOrDemonChoice()
        
        elif req.text == "2":
            print("You are now logged in as an Elder Moderator")
            rateOrDemonChoice()
        else:
            print("Wrong Account ID/password")

    except:
        print("An error occured while trying to connect to the database")
        main()
        
def rateOrDemonChoice():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nPress ENTER to go back\n")
    rateOrDemon = input("Do yo want to suggest stars for a level (0) or rate a demon level difficulty (1): ")
    if rateOrDemon == "0":
        suggestStars()
    elif rateOrDemon == "1":
        rateDemon()
    elif rateOrDemon == "":
        main()
    else:
        print("Wrong option")
        rateOrDemonChoice()
        
def suggestStars():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nPress ENTER to go back\n")
    levelID = input("Level ID: ")
    if levelID == "":
        rateOrDemonChoice()
    stars = input("Stars: ")
    if stars == "":
        rateOrDemonChoice()
    feature = input("Rating (0 for star rate only, 1 for Feature rate, 2 for Epic rate, 3 for Legendary rate, 4 for Mythic rate; default is 0): ")
    if feature == "":
        feature = 0

    headers = {
        "User-Agent": ""
    }
    data = {
        "gameVersion": 22,
        "binaryVersion": 38,
        "accountID": accountID,
        "gjp": encoded_base64,
        "levelID": levelID,
        "stars": stars,
        "feature": feature,
        "gdw": 0,
        "secret": modSecret
    }

    req = requests.post(f"{databaseUrl}suggestGJStars20.php", data=data, headers=headers)
    if req.text == "1":
        print("Success!")
        rateOrDemonChoice()
    else: 
        print("Something went wrong...")
        suggestStars()

def rateDemon():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nPress ENTER to go back\n")
    levelID = input("Level ID: ")
    if levelID == "":
        rateOrDemonChoice()
    rating = input("Demon Difficulty (1 for Easy Demon, 2 for Medium Demon, 3 for Hard Demon, 4 for Insane Demon and 5 for Extreme Demon): ")
    if rating == "":
        rateOrDemonChoice()
    headers = {
        "User-Agent": ""
    }

    data = {
        "gameVersion": 22,
        "binaryVersion": 38,
        "accountID": accountID,
        "gjp": encoded_base64,
        "secret": modSecret,
        "levelID": levelID,
        "rating": rating
    }

    req = requests.post(f'{databaseUrl}rateGJDemon21.php', data=data, headers=headers)

    if req.text == levelID:
        print("Success!")
        rateOrDemonChoice()
    else:
        print("Something went wrong...")
        rateDemon()

main()