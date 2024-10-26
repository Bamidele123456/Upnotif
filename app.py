from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template, request, json, redirect, jsonify, send_file, Blueprint, flash, send_file, \
    session, abort, url_for
import feedparser
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import html


scheduler = BackgroundScheduler()
scheduler.start()





uri = "mongodb+srv://Bamidele1:1631324de@mycluster.vffurcu.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['upwork']
user= db['users']

client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365*10)


def private(heading,email, description, link):
    # Email configuration
    sender_email = "bamideleprecious85@gmail.com"
    receiver_email = email
    password = "fhdr vwep reuq laxg"
    # Email content
    subject = "Upwork Job"
    body = f"Title: {heading}\n\nEmail:{email}\n\nDescription: {description}\n\n\nLink: {link}"

    # Constructing the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Sending the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
def fetch_first_rss_entry(rss):
    feed = feedparser.parse(rss)

    if not feed.entries:
        print("No entries found in the RSS feed")
        return

    # Fetching only the first entry
    first_entry = feed.entries[0]
    heading = first_entry.title  # Heading of the job
    description_html = first_entry.description  # Description of the job (HTML format)

    # Use BeautifulSoup to strip HTML tags from the description
    soup = BeautifulSoup(description_html, 'html.parser')
    description_text = soup.get_text(separator=' ')  # Get text content, separated by spaces
    description_text = html.unescape(description_text)  # Unescape HTML entities
    description_text = ' '.join(description_text.split())  # Get text content, separated by newlines

    job_link = first_entry.link  # Link to apply for the job
    return {
        "heading": heading,
        "description": description_text,
        "job_link": job_link
    }



@app.route("/testing")
def test():
    return render_template("signup.html")


@app.route('/testingp', methods=['POST'])
def testingp():

    rss = request.form['rss']
    email = request.form['email']
    detail = fetch_first_rss_entry(rss)
    heading = detail['heading']
    description = detail['description'],
    link = detail['job_link']
    details = {
        "email":email,
        "rss":rss,
        "heading":heading
    }
    user.insert_one(details)
    session['email'] = email

    private(heading, email, description, link)
    return redirect("/next")


@app.route('/next')
def next():
    email = session.get('email')
    detail = user.find_one({"email": email})
    if detail:
        heading = detail.get("heading", '')
        rss = detail.get("rss",'')
        ndetail = fetch_first_rss_entry(rss)
        nheading = ndetail['heading']
        ndescription = ndetail['description'],
        nlink = ndetail['job_link']
        if not heading == nheading:
            private(nheading, email, ndescription, nlink)
    return 'started'





if __name__ == "__main__":
    scheduler.add_job(next, 'interval', minutes=5)
    app.run(host="localhost", port=8080)










