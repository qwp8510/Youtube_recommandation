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

def sum_top_ten_views():
    sum_ten_video_views = df['Views'].sort_values(ascending=False)[:10]
    sum_ten_video_title = sum_ten_video_views.index.map(lambda x: df.iloc[x,:]['Title'])
    sum_ten_video_channel = sum_ten_video_views.index.map(lambda x: df.iloc[x,:]['Channel'])

    sum_ten_video_df = pd.DataFrame({'Channel':sum_ten_video_channel,'Title':sum_ten_video_title.values,'Views':sum_ten_video_views.values})
    print(sum_ten_video_df)

def sum_top_ten_like():
    sum_ten_video_like = df['Like'].sort_values(ascending=False)[:10]
    sum_ten_video_title = sum_ten_video_like.index.map(lambda x: df.iloc[x,:]['Title'])
    sum_ten_video_channel = sum_ten_video_like.index.map(lambda x: df.iloc[x,:]['Channel'])

    sum_ten_video_df = pd.DataFrame({'Channel':sum_ten_video_channel,'Title':sum_ten_video_title.values,'Like':sum_ten_video_like.values})
    print(sum_ten_video_df)

def sum_top_ten_dislike():
    sum_ten_video_dislike = df['Dislike'].sort_values(ascending=False)[:10]
    sum_ten_video_title = sum_ten_video_dislike.index.map(lambda x: df.iloc[x,:]['Title'])
    sum_ten_video_channel = sum_ten_video_dislike.index.map(lambda x: df.iloc[x,:]['Channel'])

    sum_ten_video_df = pd.DataFrame({'Channel':sum_ten_video_channel,'Title':sum_ten_video_title.values,'Dislike':sum_ten_video_dislike.values})
    print(sum_ten_video_df)


if __name__ == '__main__':
    #sum_top_ten_views()
    sum_top_ten_like()
    sum_top_ten_dislike()