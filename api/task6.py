import tweepy
import secret
from transformers import pipeline

# Authenticate to Twitter using Twitter API v2
client = tweepy.Client(bearer_token=secret.BEARER_TOKEN)  # requires secret.py, which is not included in the repository. ask from han yi

# Load pre-trained sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

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
        result = sentiment_pipeline(tweet.text)
        sentiments.append(result[0])
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
    sentiments = analyze_sentiment(tweet_texts)
    store_tweets(tweet_texts, sentiments, collection)

    """Query MongoDB to retrieve data for section 6."""
    documents = collection.find({"query": query})
    return list(documents)