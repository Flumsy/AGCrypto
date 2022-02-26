import os
import webbrowser
import sys
import time
import json
import requests
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

# Authors: Brandon McGuckin and Jamie van Noten

print("\u001b[36;1m" + "What would you like to explore?")
print("\u001b[34;1m" + "1 Tokens")
print("\u001b[34;1m" + "2 Yields")
print("\u001b[34;1m" + "3 News")
print("")
choice = int(input())

def tokens():
    print("\u001b[36;1m" + "Please start with your choice of category for token!")
    print("------------------------------")
    time.sleep(2)



    # Get categories
    r = requests.request("GET", "https://api.coingecko.com/api/v3/coins/categories/list")
    data = json.loads(r.text)
    num = 0
    for key in data:
        print(num, key["name"])
        num = num + 1



    # Find all tokens in category
    invalidInput = True

    while invalidInput == True:
        inputCategory = int(input())
        if (inputCategory in range(0, 132)):
            cat = data[inputCategory]["category_id"]
            p = requests.request("GET", "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=" + cat + "&order=market_cap_desc")
            pData = json.loads(p.text)
            jsonStr = json.dumps(pData, indent=4)
            f = open("temp.json", "w")
            f.write(jsonStr)
            invalidInput = False
        
        else: 
            print("")   
            print("Please try again with a valid category.")


    # Max MCAP
    print("")
    print("\u001b[36;1m" + "Select maximum market capitalization.")
    print("")
    print("\u001b[34;1m" + "1  $10,000,000")
    print("\u001b[34;1m" + "2  $50,000,000")
    print("\u001b[34;1m" + "3  $100,000,000")
    print("\u001b[34;1m" + "4  $500,000,000")
    print("\u001b[34;1m" + "5  $1,000,000,000")
    print("\u001b[34;1m" + "6  $10,000,000,000")
    print("\u001b[34;1m" + "7  No Max")

    maxCapInput = False
    while maxCapInput == False: 
        maxCap = int(input())
        if maxCap in range(1,8):
            maxCapInput = True
        else:
            print("")
            print("Please select a valid option.")
        

    # Min MCAP
    print("")
    print("\u001b[36;1m" + "Select minimum market capitalization.")
    print("")
    print("\u001b[34;1m" + "0  No Min")
    print("\u001b[34;1m" + "1  $10,000,000")
    print("\u001b[34;1m" + "2  $50,000,000")
    print("\u001b[34;1m" + "3  $100,000,000")
    print("\u001b[34;1m" + "4  $500,000,000")
    print("\u001b[34;1m" + "5  $1,000,000,000")
    print("\u001b[34;1m" + "6  $10,000,000,000")

    minCapInput = False
    while minCapInput == False: 
        minCap = int(input())
        if minCap in range(0,7):
            if (minCap > maxCap):
                print("")
                print("Your minimum is greater than your maximum, please select a valid option.")
            elif (minCap == maxCap):
                print("")
                print("Your minimum is equal to your maximum, please select a valid option.")  
            elif (maxCap > minCap):
                minCapInput = True
        else:
            print("")
            print("Please select a valid option.")


    if maxCap == 1:
        maxCap = 10000000
    elif maxCap == 2:
        maxCap = 50000000
    elif maxCap == 3:
        maxCap = 100000000
    elif maxCap == 4:
        maxCap = 500000000
    elif maxCap == 5:
        maxCap = 1000000000
    elif maxCap == 6:
        maxCap = 10000000000
    elif maxCap == 7:
        maxCap = 10000000000000000000000

    if minCap == 0:
        minCap = 1
    elif minCap == 1:
        minCap = 10000000
    elif minCap == 2:
        minCap = 50000000
    elif minCap == 3:
        minCap = 100000000
    elif minCap == 4:
        minCap = 500000000
    elif minCap == 5:
        minCap = 1000000000
    elif minCap == 6:
        minCap = 10000000000

    print('')


    # MarketCap Filtering

    with open('temp.json') as t:
        mcData = json.load(t)

    for key in mcData:
        if(int(key["market_cap"]) <= maxCap and int(key["market_cap"]) >= minCap):
            print(key["name"])








def yields():
    # Get chains
    r = requests.request("GET", "https://api.llama.fi/chains")
    data = json.loads(r.text)

    # Choose minimum TVL
    print("")
    print("\u001b[36;1m" + "Select minimum Total Value Locked (TVL).")
    print("")
    print("\u001b[34;1m" + "1  $100,000,000")
    print("\u001b[34;1m" + "2  $400,000,000")
    print("\u001b[34;1m" + "3  $900,000,000")
    print("\u001b[34;1m" + "4  $2,000,000,000")

    minTVLInput = False
    while minTVLInput == False: 
        minTVL = int(input())
        if minTVL in range(1,5):
            print("")
            minTVLInput = True
        else:
            print("Please select a valid option.")

    if minTVL == 1:
        minTVL = 100000000
    elif minTVL == 2:
        minTVL = 400000000
    elif minTVL == 3:
        minTVL = 900000000
    elif minTVL == 4:
        minTVL = 2000000000
    
    # TVL Filtering

    tvlr = requests.request("GET", "https://api.llama.fi/chains")
    tvlData = json.loads(r.text)
    for v in tvlData:
        if(int(v["tvl"]) >= minTVL):
            print(v["name"])
    
    print("------------------------------")
    print("\u001b[36;1m" + "Select a chain to farm on. (ex: ethereum)\nDISCLAIMER: Not all chains are supported.")
    chainName = input()

    print("------------------------------")
    # Browse on COINDIX
    print("Only stablecoin farms? Y/N")
    farmType = input()
    if(farmType == "Y" or farmType == "y"):
        webbrowser.open("https://coindix.com/?chain=" + chainName.lower() + "&kind=stable&tvl=1m&sort=-base")
    else:
        webbrowser.open("https://coindix.com/?chain=" + chainName.lower() + "&tvl=1m&sort=-base")







def news():
    news = requests.request("GET", "https://cryptopanic.com/api/v1/posts/?auth_token=4062fefd93c20066672783c615ab092f0b59e6ca")
    newsData = json.loads(news.text)
    print("")

    for i in range(10):
        print(i + 1, "\u001b[36;1m" + newsData["results"][i]["title"] + "\n")

    newsLink = int(input("Select the news article you want to open." + "\n"))
    validLink = False
    while validLink == False:
        if(newsLink in range(10)):
                webbrowser.open(newsData["results"][newsLink - 1]["url"])
                validLink = True
        else:
            newsLink = int(input("Please select a valid input." + "\n"))




if (choice == 1):
    tokens()
elif (choice == 2):
    yields()
elif (choice == 3):
    news()
