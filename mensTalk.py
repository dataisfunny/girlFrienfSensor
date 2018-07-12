
# coding: utf-8

# In[2]:


import time
from gtts import gTTS
from pygame import mixer
import tempfile
import os.path

#此函數會呼叫Google翻譯，請Google小姐幫我們唸出賀詞並錄成mp3
#如果沒有指定對象，會使用tempfile當播放完音檔自動刪掉檔案
#如果有指定對象，會啟動檔案檢查後再執行錄音、儲存與播放

def mensTalk(sentence, lang, who = "nobady", loop=1):
    #初始化mixer
    mixer.init()
    fileName='{}.mp3'.format(who)
    #音檔路徑
    path="./audio/"
    
    #如果有talk to特定對象即非nobady
    if who != "nobady" :
        #檢查檔案是否存在如果不存在再啟動錄音與播放
        if os.path.isfile(path+fileName) is True: 
         mixer.music.load(path+fileName)
         mixer.music.play(loop)
        else :
         tts=gTTS(text=sentence, lang=lang)
         tts.save(path+'{}.mp3'.format(who))
         mixer.music.load(path+fileName)
         mixer.music.play(loop)
    #進入nobady模式使用tempfile進行暫時錄音與播放
    else :
        with tempfile.NamedTemporaryFile(delete=True) as fp:
          tts=gTTS(text=sentence, lang=lang)
          tts.save('{}.mp3'.format(fp.name))
          mixer.music.load('{}.mp3'.format(fp.name))
          mixer.music.play(loop)
          

            


# In[6]:


#範例一 
dic={"孫爺爺":"孫爺爺新年快樂年年有今日歲歲有今朝",
     "蔡姊":"蔡阿姨新年快樂台灣好聲音場場爆滿",
     "志玲姊姊":"志玲姊姊新年快樂小喬嫁入大戶人家",
     "阿武":"阿武新年快樂世界越快心則慢",
     "發哥":"發哥新年快樂賭神拍續集問鼎奧斯卡",
     "范爺":"范爺新年快樂橫掃演藝圈進軍好萊塢",
     "阿妹":"阿妹新年快樂寫信告訴我今夜你要夢什麼"}

for key, value in dic.items():
  mensTalk(sentence=value,lang="zh",who=key) 
  print(key)
  time.sleep(8)

#範例二
value="happy new year although i don't know who are you"
mensTalk(sentence=value,lang="en",who="其他人")


# In[3]:




