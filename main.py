import tweepy
import openai
import json
from PIL import Image, ImageDraw, ImageFont
import warnings
from tqdm import tqdm

# Ignore deprecation warning (because of the Pillow new update..)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Import variable configuration
def load_config():
    print(f"   █████████           █████      ██████   ██████            █████████  ███████████  ███████████\r\n  ███░░░░░███         ░░███      ░░██████ ██████            ███░░░░░███░░███░░░░░███░█░░░███░░░█\r\n ░███    ░███   █████  ░███ █████ ░███░█████░███   ██████  ███     ░░░  ░███    ░███░   ░███  ░ \r\n ░███████████  ███░░   ░███░░███  ░███░░███ ░███  ███░░███░███          ░██████████     ░███    \r\n ░███░░░░░███ ░░█████  ░██████░   ░███ ░░░  ░███ ░███████ ░███    █████ ░███░░░░░░      ░███    \r\n ░███    ░███  ░░░░███ ░███░░███  ░███      ░███ ░███░░░  ░░███  ░░███  ░███            ░███    \r\n █████   █████ ██████  ████ █████ █████     █████░░██████  ░░█████████  █████           █████   \r\n░░░░░   ░░░░░ ░░░░░░  ░░░░ ░░░░░ ░░░░░     ░░░░░  ░░░░░░    ░░░░░░░░░  ░░░░░           ░░░░░    \r\n                                                                                                \r\n                                                                                                \r\n                                                                                                ")
    with open('config.json') as config_file:
        data = json.load(config_file)
    return data

# Constants variables
data = load_config()
BEARER_TOKEN = data['bearer_token']
CONSUMER_KEY = data['consumer_key']
CONSUMER_SECRET = data['consumer_secret']
ACCESS_TOKEN = data['access_token']
ACCESS_TOKEN_SECRET = data['access_token_secret']
KEY_API = data['key_api']
BOT_ID = data['bot_id']
openai.api_key = KEY_API

# Initialize a Tweepy OAuth 1 to use the Twitter V1 API
def initialize_twitter_api():
    auth = tweepy.OAuth1UserHandler(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth)
    return api

api = initialize_twitter_api()

def generate_response_image(response_text):
    # Generate response text as image using Pillow library to bypass the tweet characters limit (280)
    image = Image.new("RGB", (600, 600), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 16)
    text = response_text.replace('\n', '')
    text_width, text_height = draw.textsize(text, font)
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
    try:
        image.save("image.jpg")
        #image.show() /!\ Uncomment only for debug.
    except Exception as e:
        print(f"Unable to save the image : {e}")
        return

def post_response_to_twitter(api, tweet, response_text):
    # Post the response image to twitter.
    generate_response_image(response_text)
    try:
        media = api.media_upload('image.jpg')
        api.update_status(
            status="",
            in_reply_to_status_id=tweet.id,
            auto_populate_reply_metadata=True,
            media_ids=[media.media_id_string]
        )
    except tweepy.error.TweepError as e:
        print(f"Unable to post the image to Twitter : {e}")
        return

def get_response_from_openai(question):
    # Send the question and get the response from the OpenAI API.
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            max_tokens=2048,
            prompt=question,
        )
        response_text = response['choices'][0]['text']
        return response_text
    except openai.api_errors.ApiError as e:
        print(f"Unable to get the response from OpenAI API : {e}")
        return

def process_tweet(tweet):
    # Check if the tweet author is the bot himself, if true return as we don't want the bot to respond to himself to avoid loop.
    if (str(tweet.author_id) == str(BOT_ID)):
        return
    else:
        print(f"\n#############")
        with tqdm(total=3) as pbar:
            pbar.set_description("Getting tweet informations")
            tqdm.write(f"\nUser ID : {tweet.author_id} \nMessage : {tweet.text}")
            pbar.update(1)
            question = tweet.text
            pbar.set_description("Getting response from OpenAI")
            response_text = get_response_from_openai(question)
            pbar.update(1)
            tqdm.write(f"{response_text}\n")
            pbar.set_description("Posting response to Twitter")
            post_response_to_twitter(api, tweet, response_text)
            pbar.update(1)
            pbar.set_description("Tweet posted")
            pbar.close()
            print(f"\n#############")

# Initiallize a Streaming Client from Tweepy
class Tweetmentions(tweepy.StreamingClient):
    def on_connect(self):
        print(f" __   __             ___        __           ___  __  ___       __          __        ___  __   \r\n/  ` /  \\ |\\ | |\\ | |__  \\_/ | /  \\ |\\ |    |__  /__`  |   /\\  |__) |    | /__` |__| |__  |  \\  \r\n\\__, \\__/ | \\| | \\| |___ / \\ | \\__/ | \\|    |___ .__/  |  /~~\\ |__) |___ | .__/ |  | |___ |__/ .\r\n                                                                                                ")
        
    def on_tweet(self, tweet):
        process_tweet(tweet)

# Initialize the streaming client
stream_mentions = Tweetmentions(bearer_token=BEARER_TOKEN)
# Add rules to get bot mentions
stream_mentions.add_rules(tweepy.StreamRule(BOT_ID)) 
# Filter to get the author_id in `tweet` object
stream_mentions.filter(tweet_fields=['author_id'])