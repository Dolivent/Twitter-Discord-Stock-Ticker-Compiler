import requests
import os
import json
import Compiler
import following
import datetime
import sys
import csv
from dotenv import load_dotenv
import guildsaver
import subprocess

tickers = {}

def auth():
    load_dotenv()  # take environment variables from .env.
    return os.environ.get("BEARER_TOKEN")

def create_url(username):
    query = "from:{} -is:reply -is:retweet".format(username)
    url = "https://api.twitter.com/2/tweets/search/recent?query={}".format(query)
    return url

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def get_ticker(text, username):
    end = [" ", ".", ",", "\n"]
    index = text.find("$") #Finds location of the ticker in the tweets text
    ticker = ""
    next_text = text[index::] #finds all remaining text after the $
    for i in next_text:
        if i in end: #Searches for the end of the ticker by seeking end (space, period, comma, next paragraph)
            break
        ticker += i # Ticker is all text between the $ and the end (space, period, comma, next paragraph)
    text = text.replace(ticker, "") #Deletes ticker from the tweet
    ticker = ticker.replace(ticker[1:], ticker[1:].upper()) # Extracts ticker and capitalises
    if ticker[1:].isalpha():
        count_ticker(ticker, username)
    if "$" in text:
        get_ticker(text, username)

def count_ticker(ticker, username):
    if ticker in tickers.keys():
        ticker_authors = tickers[ticker]
        if username in ticker_authors.keys():
            tickers[ticker][username] += 1
        else:
            tickers[ticker][username] = 1
    else:
        tickers[ticker] = {username: 1}

def print_tickers():
    total = []
    prefixed_tickers = []
    for result in tickers.items():
        ticker = result[0]
        authors = result[1]
        count = 0
        for j in authors.values():
            count += j
        total.append((count, ticker))
    total.sort()
    for element in total:
        print(element[1] + " -> " + str(element[0]))
        print(json.dumps(tickers[element[1]], indent=4))
        prefixed_tickers.append("{}, ".format(element[1][1:]))

    most_mentioned_tickers = []
    for set in total:
        mentions = int(set[0])
        ticker_prefixed = set[1]

        if mentions >= 3:
            most_mentioned_tickers.append("{}".format(ticker_prefixed[1:]))
    most_mentioned_tickers = (', '.join(most_mentioned_tickers))
    prefixed_tickers = (''.join(prefixed_tickers))

    return prefixed_tickers, most_mentioned_tickers

def main():
    list_tweets = []
    set_tweets = set()
    tl = following.main()
    bearer_token = auth()

    for username in tl:
        url = create_url(username)
        headers = create_headers(bearer_token)
        json_response = connect_to_endpoint(url, headers)
        if "data" in json_response.keys(): #If the tweet isnt blank....
            for tweet in json_response['data']:
                text = tweet["text"]  #...and if the tweet contains text...
                list_tweets.append(text)
                if "$" in text: #...then run get_ticker() to retrieve tickers
                    get_ticker(text, username)

    for text in list_tweets:  # Extracts all words in tweets in set variable set_tweets
        for word in text.split():
            if word == "":
                continue
            set_tweets.add(word.upper())

    # Read discord text file

    list_discord = []
    now = datetime.datetime.now().strftime("%y%m%d")
    compiled_title = "Z Discord compiled " + now + ".txt"
    with open(compiled_title, 'r', encoding="utf-8") as rf:
        list_discord.append(rf.read())

    set_discord = set()
    for text in list_discord:  # Extracts all words in tweets in set variable set_tweets
        for word in text.split():
            if word == "":
                continue
            set_discord.add(word.upper())

    socials_set = set.union(set_tweets, set_discord)
    socials_set = list(socials_set)
    socials_set = (', '.join(socials_set)) # convert set to text

    socials_set = str(socials_set).replace("\n", ",") #remove all symbols
    socials_set = str(socials_set).replace(".", "")
    socials_set = str(socials_set).replace("!", "")
    socials_set = str(socials_set).replace("$", "")
    socials_set = str(socials_set).replace("(", "")
    socials_set = str(socials_set).replace(")", "")
    socials_set = str(socials_set).replace("/", "")
    socials_set = str(socials_set).replace("\\", "")
    socials_set = str(socials_set).replace("%", "")
    socials_set = str(socials_set).replace("-", "")
    socials_set = str(socials_set).replace("@", "")
    socials_set = str(socials_set).replace("?", "")
    socials_set = str(socials_set).replace(":", "")
    socials_set = str(socials_set).replace(";", "")
    socials_set = str(socials_set).replace("\"", "")
    socials_set = str(socials_set).replace("\'", "")
    socials_set = str(socials_set).replace("#", "")
    socials_set = str(socials_set).replace("]", "")
    socials_set = str(socials_set).replace("[", "")
    socials_set = str(socials_set).replace("+", "")
    socials_set = str(socials_set).replace(",,", ",")

    socials_set = socials_set.split(", ") # converts string to list
    socials_set = set(socials_set)

    prefixed_tickers, most_mentioned_tickers = print_tickers()

    unprefixed_tickers = Compiler.unprefixed_tickers(socials_set) # Returns compiled string
    compiled = "###Most Mentioned, " + most_mentioned_tickers + ", ###Other Tickers" + prefixed_tickers + unprefixed_tickers

    now = datetime.datetime.now().strftime("%y%m%d %H")
    compiled_title = "ZZZ Watchlist " + now + ".txt"
    compiled_file = open(compiled_title, 'w', encoding="utf-8")
    compiled_file.write(compiled)
    compiled_file.close()

if __name__ == "__main__":
    subprocess.call('python guildsaver.py', shell = True)
    main()

