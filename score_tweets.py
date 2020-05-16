import re
import glob
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def get_clean(tweet):
    res = re.sub('@\S+', '', tweet)
    res = re.sub(r"http\S+", "", res)
    return res

def get_sentiment(sent, vader):
    return vader.polarity_scores(sent).get('compound')

def get_df_list(dirpath):
    tweets = sorted(glob.glob(dirpath + "/*"))
    res = []
    for n in range(len(tweets)):
        df = pd.read_csv(tweets[n], parse_dates=['time'], index_col='time')
        df['sentiment'] = df['text'].apply(lambda x: get_sentiment(get_clean(x), vader))
        df['count'] = 1
        del df['username'], df['id'], df['text']
        df = df.resample("D").agg({'likes' : 'sum', 'retweets' : 'sum', 'sentiment' : 'sum', 'count' : 'sum'})
        res.append(df)
    return res

def get_df_added(df_list):
    res = df_list[0]
    for i in range(1, len(df_list)):
        res = res.add(df_list[i], fill_value=0)
    return res

def process_and_export(df, filepath):
    df['likes_avg'] = df['likes'] / df['count']
    df['retweets_avg'] = df['retweets'] / df['count']
    df['sentiment_avg'] = df['sentiment'] / df['count']
    df = df.fillna(0)
    df.to_csv(filepath)
    print("Successfully exported to:", filepath)
    return df


if __name__ == '__main__':
    vader = SentimentIntensityAnalyzer()
    res = get_df_list('data/tweets')
    df = get_df_added(res)
    process_and_export(df, 'data/tweets_influencers.csv')