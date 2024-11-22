import tweepy
import secret
from transformers import pipeline
from transformers import BertTokenizer, BertForSequenceClassification

# Authenticate to Twitter using Twitter API v2
client = tweepy.Client(bearer_token=secret.BEARER_TOKEN)  # requires secret.py, which is not included in the repository cause idw my keys to be exposed. ask from han yi

# Load pre-trained model and tokenizer
# REQUIRES TO FINE TUNE MODEL FIRST! this is done at task6-bert.py so pls run "python api/task6-bert.py" first
tokenizer = BertTokenizer.from_pretrained('./fine-tuned-bert')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)

# Load pre-trained sentiment analysis pipeline
sentiment_pipeline = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

def fetch_tweets(query, max_results=10, tweet_fields=['text', 'lang']):
    while True:
        try:
            response = client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=tweet_fields)
            return response.data
        except tweepy.errors.TooManyRequests:
            print("Rate limit exceeded. Waiting for 15 minutes.")
            return []
            #time.sleep(15 * 60)  # Wait for 15 minutes before retrying

def analyze_sentiment(tweets, collection):
    sentiments = []
    for tweet in tweets:
        result = sentiment_pipeline(tweet.text)
        sentiments.append(result[0])
    
    if sentiments != []:
        store_tweets(tweets, sentiments, collection)
    
    return sentiments

def store_tweets(tweets, sentiments, collection):
    for tweet, sentiment in zip(tweets, sentiments):
        tweet_data = {
            'text': tweet.text,
            'lang': tweet.lang,
            'sentiment': sentiment
        }
        collection.insert_one(tweet_data)
    print("Tweets and sentiments stored in MongoDB.")

def section6_data(collection):
    query = 'flight delay'
    tweets = fetch_tweets(query=query, max_results=10, tweet_fields=['text', 'lang'])
    tweet_texts = [tweet for tweet in tweets if tweet.lang == 'en']
    sentiments = analyze_sentiment(tweet_texts, collection)

    """Query MongoDB to retrieve data for section 6."""
    documents = collection.find({"query": query})
    return list(documents)