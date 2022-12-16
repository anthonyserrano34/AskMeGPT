# Imports
import tweepy
import openai
import json
import time

# Import configuration variables
with open('config.json') as config_file:
    data = json.load(config_file)

# Credentials
API_KEY = data['API_KEY']
API_SECRET_KEY = data['API_SECRET_KEY']
BEARER_TOKEN = data['BEARER_TOKEN']
ACCESS_TOKEN = data['ACCESS_TOKEN']
ACCESS_SECRET_TOKEN = data['ACCESS_SECRET_TOKEN']
OPENAI_API_KEY = data['OPENAI_API_KEY']
BOT_ID = data['BOT_ID']

# accès à l'API de Twitter
client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_SECRET_TOKEN)

# accès à l'API d'OpenAI
openai.api_key = OPENAI_API_KEY

class tweetMentions(tweepy.StreamingClient):
    def on_connect(self):
        print("Connected.")

    def on_tweet(self, tweet):
        print(tweet.text)
        print(tweet.id)
        question = tweet.text
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=question,
            max_tokens=70,
            n=1,
            stop=["?"]
        )
        print(response)
        try:
            client.create_tweet(text=response, in_reply_to_tweet_id=tweet.id)
        except:
            print("Erreur")
        time.sleep(15)
    
stream_mentions = tweetMentions(BEARER_TOKEN)
stream_mentions.add_rules(tweepy.StreamRule(BOT_ID)) 
stream_mentions.filter()