import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title='IdenTweety Pricing')

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
        [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }

        .plan {
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 4px;
            padding: 20px;
            margin: 10px;
            flex: 0 0 calc(33% - 20px);
        }

        /* Light mode styles */
        @media (prefers-color-scheme: light) {
            .plan {
                background-color: white;
            }
        }

        /* Dark mode styles */
        @media (prefers-color-scheme: dark) {
            .plan {
                background-color: #444;
            }
        }

        .plan-name {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }

        .plan-price {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }

        .plan-accounts {
            text-align: center;
            margin-bottom: 20px;
        }

        .plan-feature {
            font-size: 16px;
            margin-bottom: 10px;
        }

        .plan-save {
            font-size: 14px;
            color: #3f9b0b;
            text-align: center;
            margin-top: 10px;
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
st.title('IdenTweety Pricing')

st.markdown('''
Choose the perfect plan for your needs. Compare our different plans and their features below. Save more with our higher tier plans!
''')

# Section 2: Pricing Table
st.header('Pricing Plans')

# Plan details
plans = [
    {
        "name": "Basic",
        "price": "Free",
        "accounts": "10 accounts/month",
        "features": [
            "Basic bot detection",
            "Access to IdenTweety web app",
            "Email support",
            "Online knowledge base",
        ],
        "save": "Community forum access",
        "payment_link": "https://forms.gle/nHYRXfwy4Cibf8Wj9"
    },
    {
        "name": "Pro",
        "price": "$9.99/month",
        "accounts": "100 accounts/month",
        "features": [
            "Advanced bot detection",
            "Priority email support",
            "API access",
            "Customizable reports",
        ],
        "save": "Save 10% with annual billing",
        "payment_link": "https://forms.gle/nHYRXfwy4Cibf8Wj9"
    },
    {
        "name": "Enterprise",
        "price": "Contact Us",
        "accounts": "Unlimited accounts",
        "features": [
            "Dedicated account manager",
            "SLA & custom contracts",
            "Onboarding & training",
            "Priority 24/7 support",
        ],
        "save": "Custom pricing for your needs",
        "payment_link": "https://forms.gle/nHYRXfwy4Cibf8Wj9"
    },
]

# Display plans
plan_cards = ""

for plan in plans:
    plan_html = f"""
    <div class="plan">
        <div class="plan-name">{plan["name"]}</div>
        <div class="plan-price">{plan["price"]}</div>
        <div class="plan-accounts">{plan["accounts"]}</div>
    """

    for feature in plan["features"]:
        plan_html += f'<div class="plan-feature">{feature}</div>'

    if plan["save"]:
        plan_html += f'<div class="plan-save">{plan["save"]}</div>'

    # Add the Buy Now button
    plan_html += f'<div style="text-align:center;"><a href="{plan["payment_link"]}" target="_blank"><button style="padding: 10px; background-color: #3f9b0b; border: none; color: white; font-size: 16px; cursor: pointer; border-radius: 4px;">Buy Now</button></a></div>'

    plan_html += "</div>"
    plan_cards += plan_html

st.markdown(f'<div style="display: flex; justify-content: center; flex-wrap: wrap;">{plan_cards}</div>', unsafe_allow_html=True)

# Section 3: Contact Information
st.header('Contact Us for Custom Plans')

email_address = "identweetyswe@gmail.com"
contact_form_link = "https://forms.gle/9qCgPvvFWVyDNwoS9"

st.markdown(
    f'''
If you have specific requirements or need a custom plan tailored to your needs, please feel free to contact us at <a href="mailto:{email_address}">{email_address}</a> or fill out our <a href="{contact_form_link}" target="_blank">contact form</a>.
''',
    unsafe_allow_html=True,
)
