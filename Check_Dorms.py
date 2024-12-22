import requests
from bs4 import BeautifulSoup
import smtplib
import schedule
import time
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

# Configuration
# Replace with the target URL
URL = 'https://www.stwdo.de/en/living-houses-application/current-housing-offers'
CHECK_TEXT = "No results found for the given search criteria."

# Function to check the page


def check_page():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    if CHECK_TEXT in soup.text:
        print("found it")
        send_notification()

# Function to send email notification


def send_notification():
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        subject = "Offer Alert!"
        body = f"Visit {URL} - The offer is available."
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(EMAIL, TO_EMAIL, message)
    print("Notification sent!")


check_page()
# Schedule the bot to run hourly
schedule.every(1).hours.do(check_page)

# Keep the bot running
while True:
    schedule.run_pending()
    time.sleep(1)
