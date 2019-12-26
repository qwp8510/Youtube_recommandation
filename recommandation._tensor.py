import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

points_n = 200
clusters_n = 6
iteration_n = 100


df = pd.read_csv(r'C:\Users\a4793\OneDrive\桌面\python\yt_project\yt_result.csv',encoding='utf-8')

all_books_names = list(df.Title.values)
indices = []  # kneighbors
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

def Show_similar_books(assignment_values, query=None, id=None):
    if id:
        for id in indices[id][1:]:
            print(df.iloc[id]['Title'])
    if query:
        found_id = get_index_from_name(query)
        cluster_id = assignment_values[found_id]
        for k, id in enumerate(assignment_values):
            if id == cluster_id:
                yield df.iloc[k]['Title']

def Recommandtion_main(name):
    global distance, indices
    df['Categorical_binary'] = df['categorical']
    for i,value in enumerate(df['Categorical_binary']):
        Sub_categorical('Categorical_binary',value,i)    
    df['Categorical_binary'] = df['Categorical_binary'].astype('float')

    trial = df[['Views','Like','Dislike','Categorical_binary']]
    data = np.asarray([np.asarray(trial['Views']),np.asarray(trial['Like']),np.asarray(trial['Dislike']),np.asarray(trial['Categorical_binary'])]).T
    cluster_num = int(0.5 + len(data) / clusters_n)

    min_max_scaler = MinMaxScaler()
    books_features = min_max_scaler.fit_transform(data)
    np.round(books_features,4)
    print(np.array(books_features).shape)

    points = tf.constant(np.array(books_features))
    centroids = tf.Variable(tf.slice(tf.random_shuffle(points), [0, 0], [cluster_num, -1]))

    points_expanded = tf.expand_dims(points, 0)
    centroids_expanded = tf.expand_dims(centroids, 1)

    distances = tf.reduce_sum(tf.square(tf.subtract(points_expanded, centroids_expanded)), 2)
    assignments = tf.argmin(distances, 0)

    means = []
    for c in range(cluster_num):
        means.append(tf.reduce_mean(
          tf.gather(points, 
                    tf.reshape(
                      tf.where(
                        tf.equal(assignments, c)
                      ),[1,-1])
                  ),reduction_indices=[1]))

    new_centroids = tf.concat(means, 0)

    update_centroids = tf.assign(centroids, new_centroids)
    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)
        for step in range(iteration_n):
            [_, centroid_values, points_values, assignment_values] = sess.run([update_centroids, centroids, points, assignments])
            
        print("count:",len(points_values))

    for title in (Show_similar_books(assignment_values, name)):
        print(title)
    # 修改，可以分超多群，再把相同群歸為一類

if __name__ == '__main__':
    title_name = input('輸入百萬youtuber影片:')
    Recommandtion_main(title_name)