# -*- coding: UTF-8 -*-  
'''
在LINUX系统中运行,首先确保有图形库
功能：对聊天记录内容进行词频统计
参考：http://blog.csdn.net/qq_28219759/article/details/51803506
'''
import jieba #分词包
import numpy as np
import codecs #
import pandas as pd
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud,ImageColorGenerator

#请修改为自己的数据路经
datapath = '/home/shaomingguang/draw_word_cloud/'
with codecs.open(datapath+"love.txt",'r') as file:
  content = file.read()

#分词并筛选
segs = jieba.cut(content)
segment = [seg for seg in segs if len(seg)>1 and seg!='\r\n']
#用DataFrame进行操作
words_df = pd.DataFrame({'segment':segment})
print words_df.head()
stopwords = pd.read_csv(datapath+"HIT_stop.txt",index_col=False,quoting=3,sep='\t',names=['stopword'],encoding = 'utf-8')#确保同为utf-8编码
print stopwords.head(20)
#删除停用词中的词语
words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
words_stat = words_df.groupby(by=['segment'])['segment'].agg({"count_num":np.size})
#统计并输出出现频率
words_stat = words_stat.reset_index().sort(columns="count_num",ascending=False)
print words_stat
'''
绘制词云
注意：需要调用中文字体库,Ubuntu中有自己的中文库，可查询位置
'''
fonts_path = '/usr/share/fonts/opentype/noto/'
wordcloud = WordCloud(font_path=fonts_path+'NotoSansCJK.ttc',background_color="black")
wordcloud = wordcloud.fit_words(words_stat.head(100).itertuples(index=False))
plt.imshow(wordcloud)
plt.show()

bimg_path = '/home/shaomingguang/draw_word_cloud/'
bimg = imread(bimg_path+'love2.jpg')
wordcloud = WordCloud(font_path=fonts_path+'NotoSansCJK.ttc',background_color="white",mask=bimg)
wordcloud = wordcloud.fit_words(words_stat.head(100).itertuples(index=False))
bimgColors = ImageColorGenerator(bimg)
plt.axis("off")
plt.imshow(wordcloud.recolor(color_func=bimgColors))
plt.show()

