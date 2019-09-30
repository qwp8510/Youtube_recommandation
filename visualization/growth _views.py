import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
from matplotlib.font_manager import FontProperties 
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)

df = pd.read_csv(r'C:\Users\a4793\OneDrive\桌面\python\yt_project\yt_result.csv',encoding='utf-8')

min_video = 0
max_video = 274  #必須符合頻道總影片量

def Growth_views(channel_name):
    #觀看次數隨著影片增加成長曲線
    view_num = df[df['Channel'] == channel_name]['Views'][::-1]
    view_ave = view_num.mean()
    plt.figure(figsize=(10,5))
    plt.xlabel('第n隻影片',fontproperties=font)
    plt.ylabel('觀看次數',fontproperties=font)
    plt.plot(range(min_video,max_video),view_num)
    plt.plot(range(min_video,max_video),np.linspace(view_ave,view_ave,num=len(view_num)))
    plt.show()

def Top_video(channel_name):
    #抓出前十部熱門影片
    ten_video_views = df[df['Channel']==channel_name]['Views'].sort_values(ascending=False)[:10]
    ten_video_title = ten_video_views.index.map(lambda x: df.iloc[x,:]['Title'])

    ten_video_df = pd.DataFrame({'Title':ten_video_title.values,'Views':ten_video_views.values})
    print(ten_video_df)

def Top_like(channel_name):
    #抓除前十部熱門喜歡影片
    ten_video_like = df[df['Channel']==channel_name]['Like'].sort_values(ascending=False)[:10]
    ten_video_title = ten_video_like.index.map(lambda x: df.iloc[x,:]['Title'])

    ten_video_df = pd.DataFrame({'Title':ten_video_title.values,'Like':ten_video_like.values})
    print(ten_video_df)

def Top_dislike(channel_name):
    #抓除前十部熱門喜歡影片
    ten_video_dislike = df[df['Channel']==channel_name]['Dislike'].sort_values(ascending=False)[:10]
    ten_video_title = ten_video_dislike.index.map(lambda x: df.iloc[x,:]['Title'])

    ten_video_df = pd.DataFrame({'Title':ten_video_title.values,'Dislike':ten_video_dislike.values})
    print(ten_video_df)

if __name__ == '__main__':
    channel_name = '小玉'
    Growth_views(channel_name)
    #Top_video(channel_name)
    #Top_like(channel_name)
    #Top_dislike(channel_name)

