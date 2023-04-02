import streamlit as st

# Page configuration
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title='IdenTweety About')

# Function to add logo
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

# Custom CSS styles
st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
        [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
        [data-baseweb=base-input] [aria-label=TwitterHandle]{
            text-align: center;
        }
        
        /* Light mode styles */
        @media (prefers-color-scheme: light) {
            h3 {
                color: #333333;
            }
        }
        
        /* Dark mode styles */
        @media (prefers-color-scheme: dark) {
            h3 {
                color: #CCCCCC;
            }
        }
        
        h3 {
            text-align: center;
            font: bold 20px Courier;
        }
        
        body {
            font-family: Arial, sans-serif;
        }
    </style>
    """, unsafe_allow_html=True
)

# Hide fullscreen button
st.markdown('''
<style>
button [title="View fullscreen"]{
    visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# Add logo
add_logo()

# About section
about = st.container()
about_exp = about.expander('About IdenTweety', expanded=True)
with about_exp:
    
    st.markdown("<h3 style='text-align: left'>Thanks for visiting our web app! We're a group of enthusiastic software developers who love creating tools that help users navigate and understand the vast amount of data available on social media platforms like Twitter.</h3>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: left'>Our project is designed to analyze Twitter accounts and determine if they are bots or real people. We recognize that many fake accounts exist, which can spread misinformation, manipulate public opinion, or even commit fraud. That's why we developed a tool that allows users to quickly identify if a Twitter account is likely a bot or a real person.</h3>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: left'>We used the Botometer API to build this tool, which takes into consideration a variety of factors such as tweet frequency, content shared, and overall behavior patterns of the account. This enables users to evaluate Twitter accounts for bot activity using our web application, without needing to create their own code or use command-line interfaces. Accounts receive a score from 0-5, with scores closer to 0 indicating human accounts, and those closer to 5 suggesting bot accounts. A score in the middle implies uncertainty from the API.</h3>""", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: left'>Our goal is to empower users to make more informed decisions about the content they see on Twitter and protect themselves from potential scams or disinformation campaigns. We believe that social media can be a powerful tool for communication and collaboration if used responsibly and ethically. If you have any questions or would like to learn more about our team, please don't hesitate to contact us. We appreciate your interest in our web app!</h3>", unsafe_allow_html=True)

# Technologies Used section
tech = st.container()
tech_exp = tech.expander('Technologies Used')
with tech_exp:
    tech_images = ['./resources/twitter-bot_logo.png', './resources/streamlit_logo.png', './resources/heroku_logo.png']
    tech_captions = [
        "IdenTweety serves as an interface for both the Twitter API and the command-line library Botometer. When a user inputs a Twitter handle, the app fetches information about the account, such as follower and following counts, as well as a list of followers. Concurrently, Botometer analyzes user data through its own API calls to provide scores that indicate bot activity.",
        "We built this app using the Streamlit library, an open-source Python library that simplifies the creation and sharing of beautiful, custom web apps for machine learning and data science. Streamlit's framework offers predefined functions that transform plain text or data objects, like dataframes, into visually appealing and responsive web components.",
        "Our web app is hosted on Heroku, a cloud platform that enables us to easily deploy, manage, and scale our application. By using Heroku, we can ensure that our app remains accessible and responsive to users at all times. This platform allows developers to focus on building feature-rich applications without worrying about infrastructure management and server maintenance."
    ]

    for img, caption in zip(tech_images, tech_captions):
        col1, col2 = st.columns(2)
        with col1:
            st.image(img, width=200)
        with col2:
            st.markdown("<h3 style='text-align: left'>{}</h3>".format(caption), unsafe_allow_html=True)

# Demo section
demo = st.container()
demo_exp = demo.expander('Discover How IdenTweety Works!')
with demo_exp:
    st.markdown("<h3 style='text-align: center;'>Explore the step-by-step guide on how to effectively use IdenTweety, our powerful Twitter bot detector. This comprehensive video tutorial demonstrates how our app leverages the Twitter API to gather account information and the Botometer API to analyze scores for identifying potential bot accounts. Unleash the full potential of IdenTweety to make your Twitter experience safer and more transparent!</h3>", unsafe_allow_html=True)

    # Center the video and set its width using columns
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.video('./resources/demo.mp4')