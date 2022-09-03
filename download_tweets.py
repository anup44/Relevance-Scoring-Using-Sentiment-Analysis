#python libraries
import datetime
import tweepy
import csv

SEARCH_TERM = "standardchartered"

#Keys and access for Twitter
consumer_key = 'eScHHZT7Z6R1TUfRJrVZH8ecZ'
consumer_secret = 'ZuSpQB1wfkQ9YxfaF4B19ylxdGGR4qg1NRLutkJ48IFUy40urr'
access_token = '581045901-CoRGhIjTgMzZtXpnihCfHIykxwhABqRlaeTq88I9'
access_token_secret = 'cA5VU1QCUvlM04P2ylZrToXlOFJWLOlmTdraDGNFNNF1g'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

filename = 'twitter_data_analysis'+(datetime.datetime.now().strftime("%Y-%m-%d-%H"))+'.csv'

with open (filename, 'w', newline='', encoding='utf-8') as csvFile:
    csvWriter = csv.writer(csvFile)
    #using tweepy Cursor
    i = 0

    for tweet in tweepy.Cursor(api.search, q=SEARCH_TERM, lang = 'en').items(500):
    #writing a csv file
        print (i)
        i += 1
        tweets_encoded = tweet.text.encode('utf-8')
        tweets_decoded = tweets_encoded.decode('utf-8')
        out = [datetime.datetime.now().strftime("%Y-%m-%d  %H:%M"), tweet.id, tweet.user.screen_name, tweets_decoded, tweet.created_at, tweet.geo, tweet.place.name if tweet.place else None, tweet.coordinates, tweet._json["user"]["location"]]
        print (out)
        csvWriter.writerow(out)