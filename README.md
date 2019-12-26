# Youtube_recommandation
# 使用方式 

![head](https://github.com/qwp8510/Youtube_recommandation/blob/master/read_img/1569825054594.jpg)  
可以先看看我們的database的樣子 一共有八個特徵  
  
## Visualization
可以使用裡面的函式查看資料分布  
![visualization](https://github.com/qwp8510/Youtube_recommandation/blob/master/read_img/1569824823013.jpg)  
  
## Recommadation
接著使用我們監督式學習訓練出的結果看看推薦效果  
![visualization](https://github.com/qwp8510/Youtube_recommandation/blob/master/read_img/1569824781782.jpg)  
  
# 自行建立Database
可以從crawling中找到我爬取youtube資料的py檔，我是先將想抓取的youtuber(台灣前百大)網址先放進txt檔之後讀取。  
  
   
## 發展方向
之後會將程式更加自動化，能夠直接抓取資料丟到model做預測，並且目前model訓練是利用點閱、喜歡、不喜歡、類別來訓練，未來會嘗試利用NLP去把標題也考慮進訓練資料特徵中。  
並且會利用Django呈現在網頁上，能夠呈現更好的視覺化、表格化，整體運作模式更加自動化。
