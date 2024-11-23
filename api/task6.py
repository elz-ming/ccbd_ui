import tweepy
import secret
import numpy as np
from scipy.special import softmax
from transformers import pipeline
from transformers import AutoModelForSequenceClassification, AutoConfig, AutoTokenizer
from transformers import BertTokenizer, BertForSequenceClassification, BertConfig

# Authenticate to Twitter using Twitter API v2
client = tweepy.Client(bearer_token=secret.BEARER_TOKEN)  # requires secret.py, which is not included in the repository cause idw my keys to be exposed. ask from han yi

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# Load DistilBERT model and tokenizer
model_name_d = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer_d = AutoTokenizer.from_pretrained(model_name_d)
config_d = AutoConfig.from_pretrained(model_name_d)
model_d = AutoModelForSequenceClassification.from_pretrained(model_name_d)

# Load BERT model and tokenizer
model_name_b = 'bert-base-uncased'
tokenizer_b = BertTokenizer.from_pretrained(model_name_b)
config_b = BertConfig.from_pretrained(model_name_b)
model_b = BertForSequenceClassification.from_pretrained(model_name_b)

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

def fetch_tweets(query, max_results=10, tweet_fields=['text', 'lang']):
    while True:
        try:
            response = client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=tweet_fields)
            return response.data
        except tweepy.errors.TooManyRequests:
            print("Rate limit exceeded. Waiting for 15 minutes.")
            return []
            #time.sleep(15 * 60)  # Wait for 15 minutes before retrying

def analyze_sentiment(tweets):
    sentiments = []
    for tweet in tweets:
        result = sentiment_labels(tweet.text, model, tokenizer, config)
        tweet_data = {
            'text': tweet.text,
            'lang': tweet.lang,
            'sentiment': result
        }
        sentiments.append(tweet_data)
        
    return sentiments

def store_tweets(sentiments, collection):
    for sentiment_data in sentiments:
        collection.insert_one(sentiment_data)
    print("Tweets and sentiments stored in MongoDB.")

def section6_data(collection):
    query = 'flight delay'
    tweets = fetch_tweets(query=query, max_results=10, tweet_fields=['text', 'lang'])
    tweet_texts = [tweet for tweet in tweets if tweet.lang == 'en']
    sentiments = analyze_sentiment(tweet_texts)
    #     store_tweets(sentiments, collection)

    #Query MongoDB to retrieve data for section 6
    # documents = collection.find()
    # print(documents)

    return sentiments