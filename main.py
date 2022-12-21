import tweepy
import openai
import json
from PIL import Image, ImageDraw, ImageFont

# Import configuration variables
with open('config.json') as config_file:
    data = json.load(config_file)

bearer_token = data['bearer_token']
consumer_key = data['consumer_key']
consumer_secret = data['consumer_secret']
access_token = data['access_token']
access_token_secret = data['access_token_secret']
key_api = data['key_api']
bot_id = data['bot_id']

# Initialize the Tweepy client
client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_key, access_token=access_token, access_token_secret=access_token_secret)

# Initialize the OpenAI configuration 
openai.api_key = key_api

# Initialize a Streaming Client
class Tweetmentions(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(tweet.text)
        print(tweet.id)
        question = tweet.text
        response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
    )
        response_text = response['choices'][0]['text']
        print(response_text)
        
        image = Image.new("RGB", (600, 600), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 16)
        text = response_text.replace('\n', '')
        text_height = draw.textsize(text, font)
        lines = []
        line = ""
        for word in text.split():
            if draw.textsize(line + " " + word, font)[0] > image.width:
                lines.append(line)
                line = word
            else:
                line += " " + word

        lines.append(line)
        
        total_text_height = len(lines) * text_height

        y = (image.height - total_text_height) // 2

        for line in lines:
            x = (image.width - draw.textsize(line, font)[0]) // 2
            draw.text((x, y), line, fill=(255, 255, 255), font=font)
            y += text_height

        image.save("image.jpg")
        image.show()

stream_mentions = Tweetmentions(bearer_token=bearer_token)
stream_mentions.add_rules(tweepy.StreamRule(bot_id)) 
stream_mentions.filter()