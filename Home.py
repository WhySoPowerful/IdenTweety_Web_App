import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

import streamlit as st
import tweepy
import botometer
import sqlite3
import bcrypt
import csv
import base64
from io import StringIO

# Set page layout
st.set_page_config(
    page_title='IdenTweety',
    page_icon=':bird:',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Database functions
def create_connection():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            user_type TEXT NOT NULL
        );
    ''')
    conn.commit()
    return conn
    
def register_user(conn, username, password, user_type):
    try:
        # Hash the password before storing it in the database
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with conn:
            conn.execute(
                "INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)", (username, hashed_password, user_type)
            )
        return True
    except sqlite3.IntegrityError:
        return False
    
def authenticate_user(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT password, user_type FROM users WHERE username=?", (username,))
    row = cursor.fetchone()

    if row:
        stored_password, user_type = row
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return user_type
    return None

def signout():
    st.session_state.logged_in = False
    st.session_state.pop("username", None)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

conn = create_connection()

if not st.session_state.logged_in:
    with st.sidebar: 
        st.title("IdenTweety")
        st.subheader("Login / Signup")
        menu = ["Login", "SignUp"]
        choice = st.selectbox("Menu", menu)
        
        if choice == "Login":
            st.subheader("Login")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            if st.button("Login"):
                if username and password:
                    user_type = authenticate_user(conn, username, password)
                    if user_type:
                        st.success(f"Logged in as {username} ({user_type})")
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_type = user_type
                        st.experimental_rerun()
                    else:
                        st.warning("Invalid username or password")
                else:
                    st.error("Please fill in all fields")

        elif choice == "SignUp":
            st.subheader("Signup")
            new_username = st.text_input("New username", placeholder="Enter a new username")
            new_password = st.text_input("New password", type="password", placeholder="Enter a new password")
            confirm_password = st.text_input("Confirm password", type="password", placeholder="Confirm your password")
            user_type = st.selectbox("Select User Type", ["Basic", "Pro", "Enterprise"])
            
            if st.button("Signup"):
                if new_username and new_password and confirm_password:
                    if len(new_username) >= 4 and len(new_password) >= 8:
                        if new_password == confirm_password:
                            if register_user(conn, new_username, new_password, user_type):
                                st.success(f"Account created for {new_username}")
                            else:
                                st.warning("Username already exists")
                        else:
                            st.warning("Passwords do not match")
                    else:
                        st.warning("Username must be at least 4 characters, and password must be at least 8 characters long")
                else:
                    st.error("Please fill in all fields")
else:
    user_type = st.session_state.user_type
    st.title(f"🎉 Welcome {user_type} Member 🎉")
    st.sidebar.markdown(f"**Signed in as {st.session_state.username} ({user_type})**")
    if st.sidebar.button("Sign out"):
        signout()
        st.experimental_rerun()

st.markdown("---")
st.header("🏠 Home")
if not st.session_state.logged_in:
    st.markdown("""
    ## Welcome to the Secure Login / Signup System! 🔒
    
    **To get started, please login or sign up using the sidebar menu.**
    
    Enjoy your stay and feel free to explore our amazing app! 😃
    """)
else:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        ## Thank you for using our software <span style='color:lime'>{st.session_state.username}</span>! 🎊
        
        You're now logged in and ready to enjoy all the features we have to offer. 
        
        If you have any questions or need assistance, don't hesitate to reach out. Happy browsing! 😊
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        ## Understanding the Scores 📊

        Our app provides various scores to help you understand the likelihood of a Twitter account being a bot. 

        - **Overall Bot Score**: Ranging from 0 to 5, it's the average of Content, Friend, Network, Sentiment, Temporal, and Language scores. Higher scores indicate a higher likelihood of the account being a bot.
        - **Universal Score**: Ranging from 0 to 1, it represents the likelihood of the account being a bot based on a universal model, irrespective of the language.
        - **Content, Friend, Network, Sentiment, Temporal, and Language Scores**: Each ranges from 0 to 5, and they represent different aspects of an account's behavior, which can indicate bot-like activity.

        In general, higher scores suggest a higher chance of the account being a bot. Be cautious while interacting with accounts that have high scores.
        
        To learn more about each score, please refer to our documentation.
        """)
        
def save_results_to_csv(user_input, result, follower_screen_names_bot_scores):
    file_buffer = StringIO()
    writer = csv.writer(file_buffer)
    writer.writerow(["User", "Overall Bot Score", "Universal Score", "Content Score", "Friend Score", "Network Score", "Sentiment Score", "Temporal Score", "Language Score"])

    user_scores = result['raw_scores']['english']
    rescaled_user_scores = [round(value * 5, 2) for value in user_scores.values()]
    overall_bot_score = round(sum(rescaled_user_scores) / len(rescaled_user_scores), 2)
    universal_score = round(result['cap']['universal'], 2)
    writer.writerow([user_input, overall_bot_score, universal_score, *rescaled_user_scores])

    for follower, score in follower_screen_names_bot_scores.items():
        if score != 'NaN':
            detailed_scores = score["detailed_scores"]
            overall_bot_score_follower = score["overall"]
            universal_score_follower = score["universal"]
            writer.writerow([follower, overall_bot_score_follower, universal_score_follower, *detailed_scores.values()])
        else:
            writer.writerow([follower, 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'])

    file_buffer.seek(0)
    return file_buffer.getvalue()

def create_download_link(csv_data, title="Download CSV file", filename="botometer_results.csv"):
    b64 = base64.b64encode(csv_data.encode()).decode()
    button_style = """
    <style>
        .download-btn {
            color: #33C5FF;
            background-color: #FFF;
            border: 2px solid #33C5FF;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.3s;
        }
        .download-btn:hover {
            color: #FFF;
            background-color: #33C5FF;
            border-color: #1F8DC6;
        }
    </style>
    """
    button_html = f'<a class="download-btn" href="data:file/csv;base64,{b64}" download="{filename}">{title}</a>'
    return button_style + button_html

if st.session_state.logged_in:
    # Set app background color
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

    # Set app logo and title
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

    st.markdown("<h1 style='text-align: center; color: #33C5FF;'>Bot or Not?</h1>", unsafe_allow_html=True)

    # Call function to add logo
    add_logo()

    # Authenticate with Twitter API and Botometer
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
                        universal_score = round(result['cap']['universal'], 2)
                        follower_screen_names_bot_scores[screen_name] = {"overall": overall_bot_score, "detailed_scores": rescaled_scores, "universal": universal_score}
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

                # Side by side Detailed and Universal Follower Scores
                col3, col4 = st.columns([1,1])
                col3.markdown("<h3 style='text-align: center; color: var(--main-text-color);'>Detailed Follower Scores</h3>", unsafe_allow_html=True)
                col3.write({key: value["detailed_scores"] if value != 'NaN' else value for key, value in follower_screen_names_bot_scores.items()})
                col4.markdown("<h3 style='text-align: center; color: var(--main-text-color);'>Universal Follower Scores</h3>", unsafe_allow_html=True)
                col4.write({key: value["universal"] if value != 'NaN' else value for key, value in follower_screen_names_bot_scores.items()})
                                
                csv_data = save_results_to_csv(user_input, result, follower_screen_names_bot_scores)
                download_link = create_download_link(csv_data)
                st.markdown(download_link, unsafe_allow_html=True)

            except tweepy.TweepError:
                st.error("Failed to fetch user data. Please check if the handle is valid.")
        
    # Set output section
    with output_section:
        st.markdown("<hr style='border: 1px solid #33C5FF; border-radius: 2px;'>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: var(--secondary-text-color);'>Created with ❤️ by Team 06</p>", unsafe_allow_html=True)
        
else:
    st.markdown("Please log in or sign up to access the app.")
    
#Here's an overview of the scoring process in the code:

# Fetch the user's followers using the Tweepy API.
# Check the bot score for each follower using the Botometer API.
# Rescale the raw bot scores to a range of 0 to 5.
# Calculate the overall bot score by averaging the rescaled scores.
# Store the overall bot score and detailed scores for each follower in follower_screen_names_bot_scores.
# Check the bot score for the user (user_input) using the Botometer API.
# Display the user's bot score and the bot scores of their followers in the Streamlit app.
# Save the bot scores to a CSV file.