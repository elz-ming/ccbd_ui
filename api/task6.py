import tweepy
import secret
import numpy as np
from datetime import datetime, timedelta
import time
from scipy.special import softmax
from transformers import AutoModelForSequenceClassification, AutoConfig, AutoTokenizer

# Authenticate to Twitter using Twitter API v2
client = tweepy.Client(bearer_token=secret.BEARER_TOKEN)  # requires secret.py, which is not included in the repository cause idw my keys to be exposed. ask from han yi

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# Load DistilBERT model and tokenizer
# model_name_d = "distilbert-base-uncased-finetuned-sst-2-english"
# tokenizer_d = AutoTokenizer.from_pretrained(model_name_d)
# config_d = AutoConfig.from_pretrained(model_name_d)
# model_d = AutoModelForSequenceClassification.from_pretrained(model_name_d)

# # Load BERT model and tokenizer
# model_name_b = 'bert-base-uncased'
# tokenizer_b = BertTokenizer.from_pretrained(model_name_b)
# config_b = BertConfig.from_pretrained(model_name_b)
# model_b = BertForSequenceClassification.from_pretrained(model_name_b)

def sentiment_labels(text, model, tokenizer, config):
    encoded_input = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    return config.id2label[ranking[0]]

# Load pre-trained sentiment analysis pipeline
# sentiment_pipeline = pipeline('sentiment-analysis', model=model,tokenizer=tokenizer)

def fetch_tweets(db):
    query = 'flight delay'
    max_results= 50
    tweet_fields= ['text', 'lang', 'created_at']
    collection = db['tweets'] 

    while True:
        try:
            response = client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=tweet_fields,
                )
            for tweet in response.data:
                if not collection.find_one({'text': tweet['text']}):
                    collection.insert_one(tweet.data)
            
            return list(collection.find()) if collection.find() else []
        except tweepy.errors.TooManyRequests as e:
            reset_time = int(e.response.headers.get("x-rate-limit-reset"))
            print(f"Rate limit exceeded. Wait for {(reset_time - int(time.time()))} seconds to run again.")
            data = list(collection.find()) if collection.find() else []
            return data
        
def categorise_by_date(sentiments):
    for sentiment in sentiments:
        created_at = sentiment['created_at']
        
        if created_at:
            date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S.%fZ')
            
            sentiment['date'] = date.strftime('%d-%m-%Y')
        #     print(f"date: {created_at}")
        # elif not isinstance(created_at, datetime):
        #     print(f"Unexpected type for created_at: {type(created_at)}")
        #     continue
        # if created_at.month == 9:
        #     sentiment['month'] = 'September'
        # elif created_at.month == 10:
        #     sentiment['month'] = 'October'
        # elif created_at.month == 11:
        #     sentiment['month'] = 'November'
        # else:
        #     print(f"Missing created_at for tweet: {sentiment['text']}")
        print(f"sentiment: {sentiment}")        
    return sentiments

def store_tweets(sentiments, db):
    collection = db['output']
    for sentiment_data in sentiments:
        if not collection.find_one({'text': sentiment_data['text']}):
            collection.insert_one(sentiment_data)
    print("Tweets and sentiments stored in MongoDB.")

def retrieve_tweets(db):
    collection = db['output']
    sentiment_data = collection.find()
    print(sentiment_data)
    return sentiment_data
    
def section6_data(db):
    tweets = fetch_tweets(db)
    sentiments = []
    for tweet in tweets:
        tweet_data = {
            'text': tweet['text'],
            'lang': tweet['lang'],
            'created_at': tweet['created_at'],
            'sentiment': sentiment_labels(tweet['text'], model, tokenizer, config)
        }
        sentiments.append(tweet_data)
    
    categorised_sentiments = categorise_by_date(sentiments)
    store_tweets(categorised_sentiments, db)     

    return categorised_sentiments