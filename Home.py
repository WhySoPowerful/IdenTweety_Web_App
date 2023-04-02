import streamlit as st
import tweepy
import botometer
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

# Function to set app background color
def set_background_color():
    st.markdown(
        """
        <style>
        body {
            background-color: #F9F9F9;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to set app logo and title
def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.imgur.com/GGVshv0.png);
                background-repeat: no-repeat;
                padding-top: 50px;
                background-size: contain;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Function to authenticate with Twitter API and Botometer
def authenticate():
    rapidapi_key = os.environ.get('RAPIDAPI_KEY')  # Access the API key from an environment variable
    twitter_app_auth = {
        'consumer_key': os.environ.get('TWITTER_CONSUMER_KEY'),
        'consumer_secret': os.environ.get('TWITTER_CONSUMER_SECRET'),
        'access_token': os.environ.get('TWITTER_ACCESS_TOKEN'),
        'access_token_secret': os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'),
    }
    bom = botometer.Botometer(
        wait_on_ratelimit=True,
        rapidapi_key=rapidapi_key,
        **twitter_app_auth
    )
    auth = tweepy.OAuthHandler(
        twitter_app_auth['consumer_key'],
        twitter_app_auth['consumer_secret']
    )
    auth.set_access_token(
        twitter_app_auth['access_token'],
        twitter_app_auth['access_token_secret']
    )
    api = tweepy.API(auth, wait_on_rate_limit=True)

    return bom, api

# Main function to run the app
def main():
    # Set page layout
    st.set_page_config(
        page_title='IdenTweety',
        page_icon=':bird:',
        layout='wide',
        initial_sidebar_state='expanded'
    )

    set_background_color()
    add_logo()

    bom, api = authenticate()

    # Create page sections
    header = st.container()
    input_section = st.container()
    output_section = st.container()

    # Set header section
    with header:
        st.markdown("<hr style='border: 1px solid #33C5FF; border-radius: 2px;'>", unsafe_allow_html=True)

    # Set input section
    with input_section:
        st.markdown("<h2 style='text-align: center; color: #33C5FF;'>Enter a Twitter Handle</h2>", unsafe_allow_html=True)
        st.markdown(
            """
            <style>
                #twitter-handle {
                    width: 250px;
                    margin-left: auto;
                    margin-right: auto;
                    display: block;
                }
                #identify-button {
                    width: 100px;
                    margin-left: auto;
                    margin-right: auto;
                    display: block;
                }
                .no-banner {
                    text-align: center;
                    font-weight: bold;
                    color: red;
                    font-size: larger;
                    margin-top: 10px;
                }
                .no-bio {
                    text-align: center;
                    font-weight: bold;
                    color: red;
                    font-size: larger;
                    margin-top: 10px;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        col1, col2, col3 = st.columns([1, 1, 1])
        user_input_widget = col2.empty()
        user_input = user_input_widget.text_input('', '', key="twitter-handle")

        identify_button = col2.button('Identify', key='identify-button')
        if identify_button:
            if not user_input:
                st.warning("Please enter a Twitter handle.")
                
        if user_input:
            if user_input[0] == '@':
                user_input = user_input[1:]
            try:
                user = api.get_user(user_input)
                profile_image_url = user.profile_image_url.replace('_normal', '')
                try:
                    profile_banner_url = user.profile_banner_url
                except AttributeError:
                    profile_banner_url = ''
                followers_count = user.followers_count
                friends_count = user.friends_count
                if profile_banner_url:
                    st.markdown("<center><img src='{}' width='600'></center>".format(profile_banner_url), unsafe_allow_html=True)
                else:
                    st.markdown("<p class='no-banner'>No Banner</p>", unsafe_allow_html=True)
                st.markdown("<center><img src='{}' width='200'></center>".format(profile_image_url), unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center; color: var(--main-text-color);'>@{user_input}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: var(--secondary-text-color);'>{user.name}</p>", unsafe_allow_html=True)
                try:
                    bio = user.description
                except AttributeError:
                    bio = ''
                if bio:
                    st.markdown(f"<p style='text-align: center; color: var(--secondary-text-color);'>{user.description}</p>", unsafe_allow_html=True)
                else:
                    st.markdown("<p class='no-bio'>No Bio</p>", unsafe_allow_html=True)
                st.markdown("<hr style='border: 1px solid #33C5FF; border-radius: 2px;'>", unsafe_allow_html=True)
                st.write('')
                col1, col2, col3 = st.columns([1,2,1])
                col2.markdown("<h3 style='text-align: center; color: #33C5FF;'>Stats</h3>", unsafe_allow_html=True)
                col1.markdown(f"<h4 style='text-align: center; color: var(--main-text-color);'>Followers: <span style='color: #00FF00;'>{followers_count}</span></h4>", unsafe_allow_html=True)
                col3.markdown(f"<h4 style='text-align: center; color: var(--main-text-color);'>Following: <span style='color: #00FF00;'>{friends_count}</span></h4>", unsafe_allow_html=True)

                # A work in progress
                # You can adjust the weights based on the importance of each category in your specific use case.
                # In this example, we assign weights to each category (content, friend, network, sentiment, and temporal) and calculate the overall bot score using the weighted average.

                # weights = {
                #     "content": 0.25,
                #     "friend": 0.25,
                #     "network": 0.25,
                #     "sentiment": 0.15,
                #     "temporal": 0.1
                # }

                # for screen_name, result in bom.check_accounts_in(follower_screen_names):
                #     try:
                #         scores = result['raw_scores']['english']
                #         rescaled_scores = {key: round(value * 5, 2) for key, value in scores.items()}  # Rescale raw scores to range 0 to 5
                #         weighted_scores = {key: rescaled_scores[key] * weights[key] for key in rescaled_scores}
                #         overall_bot_score = round(sum(weighted_scores.values()), 2)
                #         follower_screen_names_bot_scores[screen_name] = {"overall": overall_bot_score, "detailed_scores": rescaled_scores}
                #     except Exception:
                #         follower_screen_names_bot_scores[screen_name] = 'NaN'

                follower_screen_names = [f'@{follower.screen_name}' for follower in tweepy.Cursor(api.followers, user_input).items(20)]
                follower_screen_names_bot_scores = {}
                for screen_name, result in bom.check_accounts_in(follower_screen_names):
                    try:
                        scores = result['raw_scores']['english']
                        rescaled_scores = {key: round(value * 5, 2) for key, value in scores.items()}  # Rescale raw scores to range 0 to 5
                        overall_bot_score = round(sum(rescaled_scores.values()) / len(rescaled_scores), 2)
                        follower_screen_names_bot_scores[screen_name] = {"overall": overall_bot_score, "detailed_scores": rescaled_scores}
                    except Exception:
                        follower_screen_names_bot_scores[screen_name] = 'NaN'

                result = bom.check_account(f'@{user_input}')
                st.markdown("<hr style='border: 1px solid #33C5FF; border-radius: 2px;'>", unsafe_allow_html=True)
                st.markdown("<h2 style='color: #33C5FF;'>Botometer Results</h2>", unsafe_allow_html=True)
                col1, col2 = st.columns([1,1])
                col1.markdown("<h3 style='text-align: center; color: var(--main-text-color);'>User Scores</h3>",unsafe_allow_html=True)
                col1.write(result)
                col2.markdown("<h3 style='text-align: center; color: var(--main-text-color);'>Follower Scores</h3>",unsafe_allow_html=True)
                col2.write({key: value["overall"] if value != 'NaN' else value for key, value in follower_screen_names_bot_scores.items()})

                st.markdown("<h3 style='text-align: center; color: var(--main-text-color);'>Detailed Follower Scores</h3>", unsafe_allow_html=True)
                st.write({key: value["detailed_scores"] if value != 'NaN' else value for key, value in follower_screen_names_bot_scores.items()})

            except tweepy.TweepError:
                st.error("Failed to fetch user data. Please check if the handle is valid.")

# Set output section
    with output_section:
        st.markdown("<hr style='border: 1px solid #33C5FF; border-radius: 2px;'>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: var(--secondary-text-color);'>Created with ❤️ by Team 06</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()