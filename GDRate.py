import requests
import base64
from itertools import cycle

def xor_cipher(input_string, key):
    return ''.join(chr(ord(c)^ord(k)) for c,k in zip(input_string, cycle(key)))

def main():
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
        data = {
            "accountID": accountID,
            "gjp": encoded_base64,
            "secret": accessSecret,
            "gameVersion": 21,
            "binaryVersion": 35,
            "gdw": 0
        }

        req = requests.post(f'{databaseUrl}requestUserAccess.php', data=data)

        if req.text == "-1":
            print("You are not a Moderator!")
            return 0
        
        elif req.text == "1":
            print("You are now logged in as a Moderator")
        
        elif req.text == "2":
            print("You are now logged in as an Elder Moderator")
        
        rateOrDemon = input("Do yo want to suggest stars for a level (0) or rate a demon level difficulty (1): ")
        if rateOrDemon == "0":
            levelID = input("Level ID: ")
            stars = input("Stars: ")
            feature = input("Feature (0 for no, 1 for yes; default is 0): ")
            data = {
                "gameVersion": 21,
                "binaryVersion": 35,
                "accountID": accountID,
                "gjp": encoded_base64,
                "levelID": levelID,
                "stars": stars,
                "feature": feature,
                "gdw": 0,
                "secret": modSecret
            }

            req = requests.post(f"{databaseUrl}suggestGJStars20.php", data=data)
            print(req.text)
            if req.text == "1":
                print("Success!")
                return 0
            else: 
                print("Something went wrong...")
                return 0

        elif rateOrDemon == "1":
            levelID = input("Level ID: ")
            rating = input("Demon Difficulty (1 for Easy Demon, 2 for Medium Demon, 3 for Hard Demon, 4 for Insane Demon and 5 for Extreme Demon): ")
            headers = {
            }

            data = {
                "gameVersion": 21,
                "binaryVersion": 35,
                "accountID": accountID,
                "gjp": encoded_base64,
                "secret": modSecret,
                "levelID": levelID,
                "rating": rating
            }

            req = requests.post(f'{databaseUrl}rateGJDemon21.php', headers=headers, data=data)

            if req.text == levelID:
                print("Success!")
                return 0
            else:
                print("Something went wrong...")
                return 0
        else:
            print("Wrong option")
            return 0
    except:
        print("An error occured while trying to connect to the database")
        return 0
main()