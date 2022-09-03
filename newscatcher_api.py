from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import pandas as pd
from datetime import datetime, timezone
from datetime import datetime
from time import mktime
from pygooglenews import GoogleNews

gn = GoogleNews(lang = 'en', country = 'USA')

# res = gn.search('"hdfc mutual fund" OR "HDFC MF"', helper = True, from_ = '2020-06-01', to_ = '2020-08-25', proxies=None, scraping_bee=None)
res = gn.search('japan integrated circuits,', helper = True, from_ = '2020-11-01', to_ = '2020-11-25', proxies=None, scraping_bee=None)

art_list = []
for num, ent in enumerate(res['entries']):
    art_dict = {}
    art = Article(ent['link'])
    try:
        art.download()
        art.parse()
        print (art.title, num)
    except Exception as e:
        print (e, num)
        print ('lol')
    else:
        art.nlp()
        art_dict['date'] = datetime.fromtimestamp(mktime(ent['published_parsed']))
        art_dict['title'] = art.title
        art_dict['text'] = art.text
        art_dict['summary'] = art.summary
        art_dict['source'] = ent['source']
        art_list.append(art_dict)

news_df1 = pd.DataFrame(art_list)
news_df1.to_excel("test1/" + "forexnews" + "_" + str(num) + '_' + datetime.now().strftime('%Y-%m-%d_%H-%M') + ".xlsx", 'encoding=utf-8')