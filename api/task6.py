import tweepy
import secret
import time

# Authenticate to Twitter using Twitter API v2
client = tweepy.Client(bearer_token=secret.BEARER_TOKEN) #requires secret.py, which is not included in the repository. ask from han yi

def fetch_tweets(query, max_results=10, tweet_fields=['text', 'lang']):
    while True:
        try:
            response = client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=tweet_fields)
            return response.data
        except tweepy.errors.TooManyRequests:
            print("Rate limit exceeded. Waiting for 15 minutes.")
            #time.sleep(15 * 60)  # Wait for 15 minutes before retrying

# @app.route('/')
# def home():
#     # Fetch tweets
#     query = 'flight delay'
#     tweets = fetch_tweets(query=query, max_results=10, tweet_fields=['text', 'lang'])
#     tweet_texts = [tweet.text for tweet in tweets if tweet.lang == 'en']
#     return render_template('index.html', tweets=tweet_texts)

# if __name__ == '__main__':
#     app.run(debug=True)
