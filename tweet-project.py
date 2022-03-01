# Install all necessary packages
!pip install textblob
!pip install tweepy
!pip install matplotlib
!pip install emojis

# Import Libraries
import tweepy
import json
import emojis
import datetime as d
import pandas as pd
import numpy as np
import textblob as tb

# API credentials and settings
consumer_key = "###"
consumer_secret = "###"
access_token = "###"
access_token_secret = "###"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

# Parameter and data extraction
text_query = '###'
language = 'en'
count = 2000
end_date = d.datetime(2021, 4, 6)
searchedTw = [status for status in tweepy.Cursor(api.search, q = text_query, lang =l anguage, until = end_date).items(max_tweets)]

# Turn the extracted data into JSON format and decode the emojis into string
dict_list = []
for each_json_tweet in searchedTw:
  dict_list.append(each_json_tweet._json)

with open('tweet_json_Data.txt', 'w') as file: 
  file.write(json.dumps(dict_list,indent=4))

demo_list = []
with open('tweet_json_Data.txt', encoding = 'utf-8') as json_file:
  all_data = json.load(json_file)
  for each_dictionary in all_data:
    tweet_id = each_dictionary['id']
    text = each_dictionary['text']
    created_at = each_dictionary['created_at']
    demo_list.append({'tweet_id':str(tweet_id), 'text':emojis.decode(str(text)), 'created_at':str(created_at)})

# Integrating datas into data frame
tweet_df = pd.DataFrame(demo_list,columns = ['tweet_id', 'text', 'created_at'])
tweet_df.to_csv('tweet_data.csv')

# Data cleaning and sentiment analysis
df = pd.read_csv('tweet_data.csv')
def remove_pattern(input_txt, pattern):
  r = re.findall(pattern, input_txt)
  for i in r:
    input_txt = re.sub(i, '', input_txt)
      
  return input_txt 

df['text'] = np.vectorize(remove_pattern)(df['text'], "@[\w]*")
df['text'] = np.vectorize(remove_pattern)(df['text'], "RT")
df['text'] = np.vectorize(remove_pattern)(df['text'], "#")
df['text'] = np.vectorize(remove_pattern)(df['text'], ":")
df['polarity'] = df.apply(lambda x: tb.TextBlob(x['text']).sentiment.polarity, axis = 1)
df['polarity'] = df['polarity'].astype(float)

df.to_csv('tweet_data_processed.csv')
