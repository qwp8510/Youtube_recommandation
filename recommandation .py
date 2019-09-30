import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
from scipy.cluster.vq import kmeans, vq
from sklearn import neighbors
from matplotlib.font_manager import FontProperties 
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)

df = pd.read_csv(r'C:\Users\a4793\OneDrive\桌面\python\yt_project\yt_result.csv',encoding='utf-8')

all_books_names = list(df.Title.values)
indices = 0  # kneighbors
disance = 0  # kneighbors distance

def Sub_categorical(categorical_name,value, index):
    if value == '娛樂':
        df[categorical_name][index] = 0
    if value == '音樂':
        df[categorical_name][index] = 1
    if value == '喜劇':
        df[categorical_name][index] = 2
    if value == '教育':
        df[categorical_name][index] = 3
    if value == '人物與網誌':
        df[categorical_name][index] = 4
    if value == '非營利組織與行動主義':
        df[categorical_name][index] = 5
    if value == '遊戲':
        df[categorical_name][index] = 6
    if value == '電影與動畫':
        df[categorical_name][index] = 7
    if value == '旅行與活動':
        df[categorical_name][index] = 8
    if value == '科學與技術':
        df[categorical_name][index] = 9
    if value == '新聞與政治':
        df[categorical_name][index] = 10
    if value == 'DIY 教學':
        df[categorical_name][index] = 11
    if value == '運動':
        df[categorical_name][index] = 12
    if value == '寵物與動物':
        df[categorical_name][index] = 13

def get_index_from_name(name):
    return df[df['Title']==name].index.tolist()[0]
    

def Get_id_from_partial_name(partial):
    for name in all_books_names:
        if partial in name:
            print(name,all_books_names.index(name))

def Show_similar_books(query=None,id=None):
    if id:
        for id in indices[id][1:]:
            print(df.iloc[id]['Title'])
    if query:
        found_id = get_index_from_name(query)
        for id in indices[found_id][1:]:
            print(df.iloc[id]['Title'])


def Recommandtion_main(name):
    global distance, indices
    df['Categorical_binary'] = df['categorical']
    for i,value in enumerate(df['Categorical_binary']):
        Sub_categorical('Categorical_binary',value,i)    
    df['Categorical_binary'] = df['Categorical_binary'].astype('float')

    trial = df[['Views','Like','Dislike','Categorical_binary']]
    #trial.drop(13337,inplace=True)  # 刪除outlier
    #np.asarray 不會占用內存
    data = np.asarray([np.asarray(trial['Views']),np.asarray(trial['Like']),np.asarray(trial['Dislike']),np.asarray(trial['Categorical_binary'])]).T

    min_max_scaler = MinMaxScaler()
    books_features = min_max_scaler.fit_transform(data)
    np.round(books_features,4)

    model = neighbors.NearestNeighbors(n_neighbors=6, algorithm='ball_tree')
    model.fit(books_features)
    distance, indices = model.kneighbors(books_features)

    Show_similar_books(name)
    
if __name__ == '__main__':
    title_name = input('輸入百萬youtuber影片:')
    Recommandtion_main(title_name)
           