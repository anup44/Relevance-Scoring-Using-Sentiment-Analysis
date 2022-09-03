import csv
import xlrd
import datetime
import deeppavlov
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


news_data_path = 'aylien_data_analysis2020-08-24-20.csv'
NAV_data_path = 'aditya birla.xlsx'
sentiment_model = deeppavlov.build_model(deeppavlov.configs.classifiers['sentiment_sst_conv_bert'])
classes_vocab = dict(sentiment_model['classes_vocab'])
index_classes = {val: key for key, val in classes_vocab.items()}

pred_classes = []
dates = []
dates_list = []
scores_list = []
with open(news_data_path, 'r', encoding='utf-8') as data_file:
    reader = csv.reader(data_file, delimiter=';')
    headers = next(reader)
    for row in reader:
        print (datetime.datetime.strptime(row[0], '%Y-%m-%d  %H:%M').strftime('%d-%b-%Y'))
        dates.append(datetime.datetime.strptime(row[0], '%Y-%m-%d  %H:%M').strftime('%d-%b-%Y'))
        dates_list.append(datetime.datetime.strptime(row[0], '%Y-%m-%d  %H:%M'))
        text_list = row[2].split('\n')
        # print (row[2])
        text_list = [x for x in text_list if 'aditya birla sun life' in x.lower()]
        if not text_list:
            text_list = [row[2]]
        scores = np.average(sentiment_model.compute(text_list, targets=["y_pred_probas"]), axis=0)
        print (scores)
        pred_class = index_classes[np.argmax(scores)]
        pred_classes.append(pred_class)
        scores_list.append(scores)
        # sentiment_score = sum(score_list)/len(score_list)
        print (text_list)
        print (pred_class)
    
# NAV_sheet = xlrd.open_workbook(NAV_data_path).sheet_by_index(0)
NAV_data = pd.read_excel(NAV_data_path, skiprows=4, header=0)
NAV_data = NAV_data[['Net Asset Value', 'NAV date']]
NAV_data.index = NAV_data['NAV date']
# NAV_data = NAV_data[['Net Asset Value']]
# NAV_data.plot()

senti_series = pd.Series(scores_list, index=dates_list)
senti_series.index = senti_series.index.round('D')
senti_series = senti_series.groupby(by=senti_series.index).apply(np.average)
senti_series = senti_series.apply(np.argmax)
senti_series = senti_series.apply(index_classes.get)

df = pd.DataFrame(index=pd.date_range('2020-05-04', '2020-08-25'))
df['Net Asset Value'] = NAV_data['Net Asset Value']
df['sentiment'] = senti_series
df['sentiment'] = df['sentiment'].fillna('none')
df['Net Asset Value'] = df['Net Asset Value'].fillna(method='ffill')
print (df)
print (df.index)
sns.set()
df.index = pd.to_datetime(df.index)
sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.scatterplot(x=df.index, y='Net Asset Value',hue='sentiment',data=df).set(xlim=(datetime.datetime(2020,5,4), datetime.datetime(2020,8,25)))
plt.show()