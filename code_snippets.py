# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
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


# %%
statuses1 = api.search(q='@StanChartIN -filter:retweets', lamg='en', count=100)


# %%
len(statuses1)


# %%
users = [s.user.screen_name for s in statuses1]


# %%
users[:100]


# %%
statuses1[1].text


# %%
statuses1[2].text


# %%
statuses1 = api.search(q='@StanChartIN -filter:retweets', lamg='en', count=100, tweet_mode='extended')


# %%
statuses1[2].full_text


# %%
import deeppavlov


# %%
senti_model = deeppavlov.build_model(deeppavlov.configs.classifiers.sentiment_sst_conv_bert)


# %%
topic_model = deeppavlov.build_model(deeppavlov.configs.classifiers.topic_ag_news)

# %%
business_twwets = list(filter(lambda x: topic_model([x])==['3'], [status.full_text for status in statuses1]))


# %%
for bt in business_twwets:
    print (bt)
    print ()
    print ()
    print ()
    print ()

# %%
for bt in business_twwets:
    print (bt)
    print (senti_model([bt]))
    print ()
    print ()
    print ()
    print ()


# %%
###########################################################################
# Tweets having mentions of @StanChartIN
# %%
#python libraries

import datetime
import tweepy
import csv

#Keys and access for Twitter

consumer_key = 'eScHHZT7Z6R1TUfRJrVZH8ecZ'
consumer_secret = 'ZuSpQB1wfkQ9YxfaF4B19ylxdGGR4qg1NRLutkJ48IFUy40urr'
access_token = '581045901-CoRGhIjTgMzZtXpnihCfHIykxwhABqRlaeTq88I9'
access_token_secret = 'cA5VU1QCUvlM04P2ylZrToXlOFJWLOlmTdraDGNFNNF1g'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# %%
statuses1 = api.search(q='@StanChartIN -filter:retweets', lamg='en', count=100, tweet_mode='extended')


# %%
import deeppavlov


# %%
senti_model = deeppavlov.build_model(deeppavlov.configs.classifiers.sentiment_sst_conv_bert)


# %%
topic_model = deeppavlov.build_model(deeppavlov.configs.classifiers.topic_ag_news)
# 1-World, 2-Sports, 3-Business, 4-Sci/Tech

# %%
for t in statuses1:
    print (t.full_text)
    print ()
    print ('topic:', topic_model([t.full_text]))
    print ('Sentimen:', senti_model([t.full_text]))
    print ()
    print ()
    print ()
    print ()

# %%
business_twwets = list(filter(lambda x: topic_model([x])==['3'], [status.full_text for status in statuses1]))


# %%
for bt in business_twwets:
    print (bt)
    print ()
    print ('sentiment:', senti_model([bt]))
    print ()
    print ()
    print ()
    print ()


# %%
dict(topic_model['classes_vocab'])

# %%
dict(senti_model['classes_vocab'])


# %%
###########################################################################
# statuses posted by a specific user

statuses_user = api.user_timeline(screen_name='Huobi_Research', count=1000, page=1, tweet_mode='extended')

# %%
len(statuses_user)


# %%
mentions_statuses = [s for s in statuses_user if '@StanChart' in s.full_text]

# %%
len(mentions_statuses)
# %%
print (mentions_statuses[0].full_text)
print ()
print ()
print ('topic:', topic_model([mentions_statuses[0].full_text]))
print ('sentiment:', senti_model([mentions_statuses[0].full_text]))
# %%

# %%
##########################################################################
# AYLIEN topic and sentiment

from __future__ import print_function
import csv
import time
from datetime import datetime, timezone
import aylien_news_api
from aylien_news_api.rest import ApiException
import deeppavlov
from pprint import pprint
configuration = aylien_news_api.Configuration()

# Configure API key authorization: app_id
configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = '4549c74b'

# Configure API key authorization: app_key
configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = 'dee76b905ed2890671cd5b69c969816c'

# Defining host is optional and default to https://api.aylien.com/news
configuration.host = "https://api.aylien.com/news"
# Create an instance of the API class
api_instance = aylien_news_api.DefaultApi(aylien_news_api.ApiClient(configuration))

opts = {
  'text': '"Standard Chartered"',
  'sort_by': 'published_at',
  'sort_direction': 'desc',
  'per_page': 100
}
# %%
try:
    # List Stories
    api_response = api_instance.list_stories(**opts)
    # pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->list_stories: %s\n" % e)


# %%
with open('test.txt', 'w', encoding='utf-8') as f:
    for st in api_response.stories:
        f.write(st.title + '\n')
        f.write('\n')
        f.write(st.body + '\n')
        f.write('\n')
        f.write('topic: ' + str(topic_model([st.body])) + '\n')
        f.write('sentiment: ' + str(senti_model([st.body])) + '\n')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('\n')
# %%
