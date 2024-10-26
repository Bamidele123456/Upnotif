import feedparser
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import html
import time
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# URL of the RSS feed you want to monitor
RSS_FEED_URL = 'https://www.upwork.com/ab/feed/topics/rss?securityToken=238f630ca7317a07ae15f20f0f28475516e53e2e52bab353019ec92bc1006f3cdd874a207f60359b60840bbe3882ae1c9f593f48db9b670fb0b73d163aa7f38f&userUid=1527382565055983616&orgUid=1527382565055983617'

# MongoDB connection
uri = "mongodb+srv://Bamidele1:1631324de@mycluster.vffurcu.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['upwork']
user = db['users']

# Verify MongoDB connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Function to send email
def send_email(heading, email, description, link):
    sender_email = "bamideleprecious85@gmail.com"
    password = "fhdr vwep reuq laxg"
    subject = "Upwork Job"
    body = f"Title: {heading}\n\nDescription: {description}\n\nLink: {link}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, email, message.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to fetch the first RSS entry
def fetch_first_rss_entry(rss_url):
    feed = feedparser.parse(rss_url)
    if not feed.entries:
        print("No entries found in the RSS feed")
        return None

    first_entry = feed.entries[0]
    heading = first_entry.title
    description_html = first_entry.description

    soup = BeautifulSoup(description_html, 'html.parser')
    description_text = soup.get_text(separator=' ').strip()
    description_text = html.unescape(description_text)

    job_link = first_entry.link
    return {"heading": heading, "description": description_text, "job_link": job_link}

# Main function to check the feed and send notifications
def check_feed_and_notify():
    users = user.find()
    for detail in users:
        email = detail.get("email")
        heading = detail.get("heading", '')

        new_entry = fetch_first_rss_entry(detail['rss'])
        if new_entry and new_entry['heading'] != heading:
            send_email(new_entry['heading'], email, new_entry['description'], new_entry['job_link'])
            user.update_one({"email": email}, {"$set": {"heading": new_entry['heading']}})

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_feed_and_notify, 'interval', minutes=2)
    scheduler.start()

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
