import tweepy
import openai
import json

# Import configuration variables
with open('config.json') as config_file:
    data = json.load(config_file)

bearer_token = data['bearer_token']
key_api = data['key_api']
bot_id = data['bot_id']

client = tweepy.Client(
    bearer_token=bearer_token
)
openai.api_key = key_api

class Tweetmentions(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(tweet.text)
        print(tweet.id)
        question = tweet.text
        response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=question,
        max_tokens=280,
        n=1,
        stop=["?"]
    )
        print(response)

stream_mentions = Tweetmentions(bearer_token=bearer_token)
stream_mentions.add_rules(tweepy.StreamRule(bot_id)) 
stream_mentions.filter()