# AskMeGPT
AskMeGpt is an automated twitter bot developped in Python that implements "chat-gpt" tool with OpenAI API. https://twitter.com/AskMeGPT

# Setup
<h2>Project installation</h2>
1. Clone the project.<br>
2. Once the project is cloned, open a terminal within the project directory and run <code>pip install -r requirements.txt</code>.

<h2>Configuration of the twitter bot and credentials</h2>
1. Go to https://developer.twitter.com/en/portal/projects-and-apps create an application.<br>
2. Once the configuration is done, retrieve all the tokens.<br>
3. Save your twitter <code>bot_id</code>, <code>consumer_key</code>, <code>consumer_secret</code>, <code>access_token</code>, <code>access_token_secret</code> and the <code>bearer_token</code> into <code>config.json</code>.

<h2>Get your OpenAI session token</h2>
1. Go to https://beta.openai.com/signup and log in or sign up.<br>
2. Follow the instructions to get an <code>api_key</code>.<br>
3. Save your <code>api_key</code> into <code>config.json</code>.

<h2>Running</h2>
<code>python3 main.py</code> or <code>py main.py</code>

# Result example
![image](https://user-images.githubusercontent.com/75832820/209193708-7df7441e-fca3-45a4-98ea-686100593727.png)
