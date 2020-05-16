import os
import sys
import csv
import tweepy
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup


consumer_key = "6pn124ebmlqUI9KnBAM8WStNg"
consumer_secret = "Y6mK9pKhuON4ICNbAApIXxjeBxdJvxLQLK2YxwN4xtJKP7sshj"
access_key = "889868416340938752-oE3WDOWzGuPcwAW12URF0EDjRx3L62z"
access_secret = "VHIxohkMnukpdUnIKs6ug6yIISyG9Ew2THea3XYVTjfYm"

def getTwitterHandles():
    url = "https://cryptoweekly.co/100/"
    client = urlopen(url)
    pageHtml = client.read()
    pageSoup = soup(pageHtml, "html.parser")

    profiles = pageSoup.findAll("div", {"class" : "testimonial-wrapper"})
    res = []
    for person in profiles:
        res.append(person.findAll("div", {"class" : "author"}))
    for i in range(len(res)):
        res[i] = res[i][0].findAll("a")[0].text[1:]

    client.close()
    return res

def get_tweets(username):
    outfile = "data/tweets/" + username + "_tweets.csv"
    since_id, res_old = 0, 0
    if os.path.exists(outfile):
        print("File already exists! Prepending...")
        with open(outfile, newline='', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            res_old = list(reader)
            since_id = int(res_old[1][1])
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    number_of_tweets = int(sys.argv[2])
    res = [["username", "id", "time", "likes", "retweets", "text"]]
    i = 0
    try:
        for tweet in tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode='extended', since_id=since_id).items(number_of_tweets):
            res.append([username, tweet.id_str, tweet.created_at, tweet.favorite_count, tweet.retweet_count, tweet.full_text.replace('\n', '\\n')])
            if i % 1000 == 0:
                print('Tweet number in progress:', i)
            i += 1
    except: pass
    if res_old:
        res += res_old[1:]

    if len(res) < 2: 
        print("No tweet could be retrieved. Perhaps, the account is invalid or has not tweeted.")
    else:
        with open(outfile, 'w', encoding='utf-8', errors='ignore') as f:
            writer = csv.writer(f, lineterminator='\n', delimiter=',', quoting=csv.QUOTE_ALL)
            writer.writerows(res)
        print("Success! Exported to:", outfile)


if __name__ == '__main__':
    if sys.argv[1].lower() != 'all':
        get_tweets(sys.argv[1])
    else:
        handles = getTwitterHandles()
        for handle in handles:
            if handle in ['livio_huobi', 'jlvdv', 'polychain']:
                continue
            get_tweets(handle)