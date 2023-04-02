# IdenTweety - Twitter Bot Detector
IdenTweety is a Twitter bot detection app created using Python, powered by Streamlit, Tweepy, and Botometer libraries. The app provides a user-friendly interface to input a Twitter handle and analyze the account for bot-like behavior. It retrieves user information such as profile picture, name, description, and follower/following count. IdenTweety also computes bot scores for the input account and its followers using Botometer's machine learning algorithms. This helps users identify potentially automated accounts or disinformation campaigns on Twitter.

To set up and use the app, follow the instructions in the README.md file, which guides you through installing required dependencies, obtaining API keys from Botometer and Twitter, and running the app locally using Streamlit. With IdenTweety, you can conveniently assess the authenticity of Twitter accounts and gain insights into their followers' bot scores.
## Requirements
Requires Python 3.8+.
## Dependencies
- botometer
- python-dotenv
- secure-smtplib
- streamlit
- tweepy
## Setup
1. `pip install -r requirements.txt`
2. Follow the following instructions to [Generate an API Key for Botometer](https://rapidapi.com/OSoMe/api/botometer-pro/details)
3. Follow the following instructions to [Generate an API Key for Twitter](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api)
4. Modify `.env` file with your API Key information for the Home page and Email/Password for the Support page
## Run
- From inside of the root folder: `streamlit run Home.py`