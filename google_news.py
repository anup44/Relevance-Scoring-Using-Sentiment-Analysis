from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import pandas as pd
from datetime import datetime, timezone

list_names = ['europe pharmaceuticals']

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

for fund_name in list_names:
    googlenews=GoogleNews(start='09/25/2020',end='09/25/2020')
    num=0
    list=[]
    for i in range(0,2,1):
        print("page "+str(i+1))
        if i==0:
            googlenews.search(fund_name)
        else:
            googlenews.getpage(i)
        result=googlenews.result()
        df=pd.DataFrame(result) 
        for ind in df.index:
            dict={}
            article = Article(df['link'][ind], config=config)
            try:
                article.download()
                article.parse()
                article.nlp()
                print (article.title, num)
                try:
                    dict['date'] = article.publish_date.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%Y-%m-%d  %H:%M")
                except:
                    dict['date'] = df['date'][ind]
                    print ('****no date*****')
                dict['Date1']=df['date'][ind]
                dict['Media']=df['media'][ind]
                dict['Author']=article.authors
                dict['Title']=article.title
                dict['Article']=article.text
                dict['Summary']=article.summary
                dict['link'] = df['link'][ind]
                list.append(dict)
                num +=1
            except Exception as e:
                print (e)
                print ('lol')
        googlenews.clear()
    news_df=pd.DataFrame(list)
    news_df.to_excel("test1/" + "forexnews" + "_" + str(num) + '_' + datetime.now().strftime('%Y-%m-%d_%H-%M') + ".xlsx")
    print(fund_name,num)
# print(df.head())