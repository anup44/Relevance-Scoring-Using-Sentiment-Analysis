# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import csv
import xlrd
import glob
import datetime
import deeppavlov
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# %%
n_delta = 1
NAV_path_list = glob.glob('Mutual Funds data/*.xlsx')
# news_data_path = 'HDFC_2020-08-25-10.csv'
news_data_path = 'test1/newscatcher_search_MF_100.csv'
search_text = ['hdfc mutual fund']

# %%
NAV_path_list


# %%
NAV_dfs = []

# %%
NAV_data = pd.DataFrame(index=pd.date_range('2020-06-01', '2020-08-25'))
NAV_delta_1 = pd.DataFrame(index=pd.date_range('2020-06-01', '2020-08-25'))

for i, path in enumerate(NAV_path_list, 1):
    NAV_df = pd.read_excel(path, skiprows=4, header=0)
    NAV_df = NAV_df[['Net Asset Value', 'NAV date']]
    NAV_df.index = NAV_df['NAV date']
    NAV_dfs.append(NAV_df.copy(deep=True))
    
    NAV_df['Net Asset Value'] = (NAV_df['Net Asset Value'] - NAV_df['Net Asset Value'].mean())/NAV_df['Net Asset Value'].std()
    
    NAV_data = NAV_data.join(NAV_df[['Net Asset Value']].rename(columns={'Net Asset Value': 'NAV' + str(i)}), rsuffix=str(i))
    NAV_delta_1 = NAV_delta_1.join(NAV_df[['Net Asset Value']].rename(columns={'Net Asset Value': 'NAV' + str(i)}).diff(periods=n_delta, axis=0), rsuffix=str(i))


# %%
NAV_data


# %%
# NAV_data.join(NAV_dfs[0].rename(columns={'Net Asset Value': 'NAV1'}), rsuffix='_1')

# %%
sns.set()
sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.lineplot(data=NAV_data, dashes=False) 
# %%

NAV_delta = NAV_data.diff(axis=0)

# %%
NAV_delta
# %%
sns.set()
sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.lineplot(data=NAV_delta.iloc[:, 1:], dashes=False)
# plt.axvline(datetime.datetime(2020,7,1), color='red')
# %%
sentiment_model = deeppavlov.build_model(deeppavlov.configs.classifiers['sentiment_sst_conv_bert'])
classes_vocab = dict(sentiment_model['classes_vocab'])
index_classes = {val: key for key, val in classes_vocab.items()}

# %%
pred_classes = []
dates = []
dates_list = []
scores_list = []
with open(news_data_path, 'r', encoding='utf-8') as data_file:
    reader = csv.reader(data_file, delimiter=',')
    headers = next(reader)
    for row in reader:
        print (datetime.datetime.strptime(row[0], '%Y-%m-%d  %H:%M').strftime('%d-%b-%Y'))
        dates.append(datetime.datetime.strptime(row[0], '%Y-%m-%d  %H:%M').strftime('%d-%b-%Y'))
        dates_list.append(datetime.datetime.strptime(row[0], '%Y-%m-%d  %H:%M'))
        text_list = row[2].split('\n')
        # print (row[2])
        text_list = [x for x in text_list if any([st in x.lower() for st in search_text])]
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
    
# %%
senti_series = pd.Series(scores_list, index=dates_list)
senti_series.index = senti_series.index.floor('D')
senti_series = senti_series.groupby(by=senti_series.index).apply(np.average)
senti_series = senti_series.apply(np.argmax)
senti_series = senti_series.apply(index_classes.get)

# %%

# NAV_data['sentiment'] = senti_series
# NAV_data['sentiment'] = NAV_data['sentiment'].fillna('none')


# %%
NAV_data

# %%
NAV_delta_1

# %%
sentiment_color_map = {'very_positive': 'green',
                        'negative': 'orange',
                        'very_negative': 'red',
                        'neutral': 'blue'
                        }
# %%
# Delta plot for all funds
sns.set()
sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.lineplot(data=NAV_delta_1.iloc[:, 1:], dashes=False)

for d, senti in senti_series.items():
    if senti in sentiment_color_map.keys():
        plt.axvline(d, color=sentiment_color_map[senti])


# %%
# Delta plot for one fund
sns.set()
sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.lineplot(data=NAV_delta_1.iloc[:, 6:7], dashes=False, markers=True)
#sns.scatterplot(x=NAV_delta_1.index, y='NAV7', data=NAV_delta_1, hue=senti_series).set(xlim=(datetime.datetime(2020,6,1), datetime.datetime(2020,8,25)))
plt.axhline(0, color='black')
plt.xlim(datetime.datetime(2020,6,1), datetime.datetime(2020,8,25))
plt.ylim(-1, 1)
for d, senti in senti_series.items():
    if senti in sentiment_color_map.keys():
        plt.plot(d, NAV_delta_1['NAV7'][d], marker='o', color=sentiment_color_map[senti])
# %%
# NAV Data plot all 8 funds
sns.set()
sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.lineplot(data=NAV_data, dashes=False) 

for d, senti in senti_series.items():
    if senti in sentiment_color_map.keys():
        plt.axvline(d, color=sentiment_color_map[senti])

# %%
# Data plot for one fund
sns.set()
sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.lineplot(data=NAV_dfs[6]['Net Asset Value'], dashes=False) 

for d, senti in senti_series.items():
    if senti in sentiment_color_map.keys():
        plt.axvline(d, color=sentiment_color_map[senti])

#%%

sns.set()
sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.lineplot(data=NAV_dfs[6]['Net Asset Value'], dashes=False, markers=True) 

plt.xlim(datetime.datetime(2020,6,1), datetime.datetime(2020,8,25))
# plt.ylim(-1, 1)
for d, senti in senti_series.items():
    if senti in sentiment_color_map.keys():
        plt.plot(d, pd.Series(NAV_dfs[6]['Net Asset Value'], index=NAV_delta_1.index)[d], marker='o', color=sentiment_color_map[senti])

# %%
plt.show()
# %%
# check sentiment scores for one day
senti_series[datetime.datetime(2020,8,12, 7)]
# %%
