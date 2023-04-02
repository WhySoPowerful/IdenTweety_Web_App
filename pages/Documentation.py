import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title='IdenTweety Documentation')

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
    </style>
    """, unsafe_allow_html=True
)

add_logo()

# Section 1: Introduction
st.title('IdenTweety Documentation')

st.markdown('''
Welcome to the IdenTweety documentation! In this document, you will find detailed information about the Twitter API, Botometer API, software functionalities, limitations, human recognition, software capabilities, and testing/troubleshooting of the software.
''')

# Section 2: Twitter API
st.header('Twitter API')

st.markdown('''
The Twitter API allows developers to access and interact with Twitter data programmatically. To use the Twitter API, you will need to create a developer account and obtain API keys and access tokens. You can do this by following the instructions in the [official documentation](https://developer.twitter.com/en/docs/authentication/oauth-1-0a).

With the Twitter API, you can:

1. Retrieve tweets, users, and other data.
2. Post tweets, follow/unfollow users, and perform other actions.
3. Stream tweets in real-time based on specific criteria.

For a full list of available endpoints and detailed documentation, visit the [official Twitter API reference](https://developer.twitter.com/en/docs/api-reference-index).

**Note**: Twitter API has rate limits, which means you can only make a limited number of requests within a specific time window. For more information on rate limits, visit the [official rate limits documentation](https://developer.twitter.com/en/docs/twitter-api/rate-limits).
''')

# Section 3: Botometer API
st.header('Botometer API')

st.markdown('''
Botometer (formerly BotOrNot) is an API developed by the [Observatory on Social Media](https://osome.iuni.iu.edu/) at Indiana University. Botometer API analyzes Twitter accounts and scores them based on the likelihood of being a bot.

To use the Botometer API, you will need to obtain an API key. You can request an API key by [signing up for a Botometer account](https://botometer.iuni.iu.edu/#!/signup). Once you have an API key, you can start making requests to the Botometer API.

The Botometer API returns a score between 0 and 5 for each Twitter account it analyzes. A score closer to 0 indicates the account is more likely to be human, while a score closer to 5 indicates the account is more likely to be a bot. A score in the middle signifies that the API is uncertain.

For more information on how to use the Botometer API and the available endpoints, visit the [official Botometer API documentation](https://botometer.iuni.iu.edu/#!/api).
''')

# Section 4: Human Recognition and Software Capabilities
st.header('Human Recognition and Software Capabilities')

st.markdown('''
IdenTweety uses a combination of the Twitter API and Botometer API to analyze Twitter accounts and determine the likelihood of them being bots. Our software is capable of:

1. Accurately identifying many bot accounts based on their behavior, content, and other factors.
2. Providing users with an easy-to-use interface for analyzing Twitter accounts.
3. Presenting the analysis results in a clear, concise, and visually appealing manner.

However, it is important to note that human recognition is an inherently complex task, and our software may not always be able to accurately identify all bot accounts. In some cases, false positives (identifying real users as bots) and false negatives (identifying bots as real users) may occur. It is recommended to use IdenTweety as a starting point for further investigation and not as the sole basis for determining if an account is a bot or a real person.
''')

# Section 5: Software Functionalities
st.header('Software Functionalities')

st.markdown('''
IdenTweety is designed to provide users with a simple, easy-to-use web application for analyzing Twitter accounts and identifying potential bot activity. The software's main functionalities include:

1. Analyzing Twitter accounts using the Twitter API and Botometer API.
2. Displaying the results in a user-friendly web interface.
3. Allowing users to input Twitter handles and view account information, including bot scores.

To use IdenTweety, simply input a Twitter handle into the text box, and the application will analyze the account and display the results.
''')

# Section 6: Limitations
st.header('Limitations')

st.markdown('''
While IdenTweety is designed to be a useful tool for identifying potential bot accounts, it is important to understand its limitations:

1. The accuracy of the bot scores depends on the accuracy of the Botometer API.
2. The software is subject to the rate limits of both the Twitter API and the Botometer API.
3. False positives and false negatives may occur in the bot detection process.

It is recommended to use IdenTweety as a starting point for further investigation and not as the sole basis for determining if an account is a bot or a real person.
''')

# Section 7: Testing and Troubleshooting
st.header('Testing and Troubleshooting')

st.markdown('''
To ensure that IdenTweety functions as expected and to address any issues that may arise, we recommend the following testing and troubleshooting steps:

1. Test the software with a variety of Twitter accounts, including known bot accounts and real users, to ensure accurate results.
2. Monitor the rate limits of the Twitter API and Botometer API to avoid exceeding the allowed number of requests.
3. Regularly update the software to incorporate the latest changes and improvements from the project's GitHub repository.

If you encounter any issues while using IdenTweety, you can:

1. Review the error messages and traceback information provided by the software to identify the source of the issue.
2. Consult the official documentation of the Twitter API, Botometer API, and Streamlit library for further guidance.
3. Open an issue on the project's [GitHub repository](https://github.com/WhySoPowerful/IdenTweety-Doc) to seek assistance from the development team and the community.

We encourage users to report any issues or suggestions for improvements to help us enhance the software and provide a better experience for all users.
''')

# Section 8: GitHub Link
st.header('GitHub Link')

st.markdown('''
If you have any questions or would like to contribute to the project, please feel free to open an issue or submit a pull request. We appreciate your interest and support!

<a href="https://github.com/WhySoPowerful/IdenTweety-Doc" target="_blank"><img src="https://github.blog/wp-content/uploads/2013/04/0cf7be70-a5e3-11e2-8943-6ac7a953f26d.jpg?resize=1234%2C631" alt="GitHub Logo" width="1100" /></a>
''', unsafe_allow_html=True)