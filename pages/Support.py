import streamlit as st
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

def send_email(to_email, email_body):
    # Replace with your email address and password
    your_email = os.environ.get('YOUR_EMAIL')
    your_password = os.environ.get('YOUR_PASSWORD')

    msg = MIMEMultipart()
    msg["From"] = your_email
    msg["To"] = to_email
    msg["Subject"] = "New Feedback"

    msg.attach(MIMEText(email_body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(your_email, your_password)
        text = msg.as_string()
        server.sendmail(your_email, to_email, text)
        server.quit()
    except Exception as e:
        print(f"Error: {e}")

st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title='IdenTweety Support')

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
        h3 {
            text-align: center;
            font: bold 20px Courier;
        }
        body {
            color: #2c3e50;
        }
        .stTextInput>div>div>input {
            font-size: 1rem;
        }
        .stMarkdown h3:hover {
            background-color: rgba(0, 0, 0, 0.05);
            border-radius: 4px;
            cursor: pointer;
        }
    </style>
    """, unsafe_allow_html=True
)

add_logo()

st.title("IdenTweety Support Center")

faq_dict = {
    "1. What is IdenTweety?": "IdenTweety is a Twitter bot detection tool that determines whether a Twitter account is likely to be run by a bot or a human.",
    "2. How does IdenTweety work?": "IdenTweety uses a tool called Botometer to analyze Twitter accounts and determine the likelihood that they are run by bots.",
    "3. What is Botometer?": "Botometer is a machine learning tool that analyzes various characteristics of Twitter accounts, such as the content of their tweets and their follower networks, to determine the likelihood that they are bots.",
    "4. What are the different sections of the IdenTweety Home app?": "The IdenTweety app has three main sections: the header section, the input section, and the output section.",
    "5. What is the header section of the IdenTweety app?": "The header section of the IdenTweety app contains the app logo and title, as well as a horizontal line to separate it from the rest of the page.",
    "6. What is the input section of the IdenTweety app?": "The input section of the IdenTweety app allows users to enter a Twitter handle that they would like to analyze.",
    "7. What is the output section of the IdenTweety app?": "The output section of the IdenTweety app displays the results of the bot detection analysis for the entered Twitter handle.",
    "8. What information does the output section display?": "The output section displays information such as the Twitter handle's profile picture, follower and following counts, and the results of the bot detection analysis.",
    "9. Can IdenTweety analyze multiple Twitter handles at once?": "No, IdenTweety can only analyze one Twitter handle at a time.",
    "10. How accurate is IdenTweety's bot detection analysis?": "The accuracy of IdenTweety's bot detection analysis depends on the accuracy of Botometer's machine learning algorithms.",
    "11. Does IdenTweety store any user data?": "No, IdenTweety does not store any user data.",
    "12. Can I use IdenTweety to analyze my own Twitter account?": "Yes, you can use IdenTweety to analyze your own Twitter account.",
    "13. Can I use IdenTweety to analyze Twitter accounts in languages other than English?": "Yes, Botometer supports analysis of Twitter accounts in multiple languages.",
    "14. Is IdenTweety free to use?": "Yes, IdenTweety is free to use.",
    "15. Who developed IdenTweety?": "IdenTweety was developed by Team 06.",
    "16. What are the system requirements for using IdenTweety?": "To use IdenTweety, you need an internet connection and a web browser that supports Streamlit, the Python library used to create the app.",
    "17. Can I use IdenTweety to analyze Twitter accounts that are private?": "No, IdenTweety cannot analyze Twitter accounts that are private or that the user does not have access to.",
    "18. How long does it take for IdenTweety to analyze a Twitter account?": "The time it takes for IdenTweety to analyze a Twitter account depends on various factors, such as the size of the Twitter account's follower network and the current load on Botometer's servers.",
    "19. What should I do if I receive an error message when using IdenTweety?": "If you receive an error message when using IdenTweety, double-check that the Twitter handle you entered is valid and try again. If the problem persists, contact the IdenTweety development team for support.",
    "20. Can I use IdenTweety for commercial purposes?": "Yes, you can use IdenTweety for commercial purposes as long as you comply with the Botometer API terms of service and any other relevant laws and regulations."
}

def display_faq(question, answer, search_term=None):
    if search_term:
        question = re.sub(f'({search_term})', r'<mark>\1</mark>', question, flags=re.IGNORECASE)
    st.markdown(f"**{question}**", unsafe_allow_html=True)
    st.write(answer)

def search_results(user_search, faq_dict):
    found = False
    for question, answer in faq_dict.items():
        if re.search(user_search.lower(), question.lower()):
            display_faq(question, answer, user_search)
            found = True
    return found

faq = st.container()
faq_exp = faq.expander('Frequently Asked Questions', expanded=True)
with faq_exp:
    for question, answer in faq_dict.items():
        display_faq(question, answer)

search = st.container()
with search:
    st.markdown("<h3>Search for answers</h3>", unsafe_allow_html=True)
    user_search = st.text_input("Type your question here")

    if user_search:
        st.write("Search results:")
        found = search_results(user_search, faq_dict)
        if not found:
            st.write("No results found. Please submit your question to our support team.")

submit_question = st.container()
with submit_question:
    st.markdown("<h3>Submit a question</h3>", unsafe_allow_html=True)
    google_form_link = "https://forms.gle/Kif2poynZkgYjN3a6"
    st.write("If you have a question that's not answered in our FAQ or search results, please submit your question using the button below.")
    if st.button("Submit a question"):
        st.write(f"Click [here]({google_form_link}) to open the Google Form and submit your question.")

forum = st.container()
forum_exp = forum.expander("Community Forums")
with forum_exp:
    st.write("Check out our community forums for more help and discussion topics:")
    st.write("1. [Twitter Developer Community](https://twittercommunity.com/)")
    st.write("2. [BotLab Forum](https://forum.botlab.org/)")
    st.write("3. [Python Forum](https://python-forum.io/)")
    st.write("4. [Stack Overflow Community](https://stackoverflow.com/)")

feedback = st.container()
with feedback:
    st.markdown("<h3>Feedback</h3>", unsafe_allow_html=True)
    st.write("Please leave your feedback below to help us improve our product. We value your input.")
    user_feedback = st.text_area("Your feedback here")
    feedback_email = os.environ.get('YOUR_FEEDBACK_EMAIL')  # Replace with the email address where you want to receive feedback
    
    if st.button("Submit feedback"):
        if user_feedback:
            send_email(feedback_email, user_feedback)
            st.success("Thank you for your feedback! We appreciate your input.")
        else:
            st.warning("Please enter your feedback before submitting.")

contact = st.container()
with contact:
    st.markdown("<h3>Contact Us</h3>", unsafe_allow_html=True)
    st.write("If you need further assistance, please don't hesitate to contact us:")
    st.write("Phone: +1 (404) 456-7890")
    st.write("Email: [identweetyswe@gmail.com](mailto:identweetyswe@gmail.com)")