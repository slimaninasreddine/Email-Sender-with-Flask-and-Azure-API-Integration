from flask import Flask, request, render_template, redirect, url_for
import requests
import csv
import os
from time import sleep
from dotenv import load_dotenv
import secrets
import base64
import mimetypes

# Generate a random Flask secret key for session management
secretstoken_hex = secrets.token_hex(16)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = secretstoken_hex
print(secretstoken_hex)

# Microsoft Graph API credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = "common"  # Use "common" for personal accounts
REDIRECT_URI = "http://localhost:5000/callback"
# This scope gives access to Graph API. Use '.default' for all permissions granted on app registration.
SCOPES = "https://graph.microsoft.com/.default"

# OAuth endpoints
AUTH_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

# Global access token
access_token = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    auth_request_url = (
        f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"
        f"&response_mode=query&scope={SCOPES}&state=12345"
    )
    return redirect(auth_request_url)

@app.route("/callback")
def callback():
    global access_token
    code = request.args.get("code")
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": SCOPES,
    }
    token_response = requests.post(TOKEN_URL, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")
    return redirect(url_for("send_email"))

@app.route("/send_email", methods=["GET", "POST"])
def send_email():
    if request.method == "POST":
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Get the CSV file and form fields
        csv_file = request.files["csv_file"]
        subject = request.form["subject"]
        body_template = request.form["body"]

        # Save CSV file
        csv_file_path = os.path.join(upload_dir, csv_file.filename)
        csv_file.save(csv_file_path)
        
        # Process multiple attachments. Use getlist to receive all files.
        attachments = request.files.getlist("attachment")

        # Save attachments and store their paths
        attachment_paths = []
        for attach in attachments:
            if attach.filename:
                path = os.path.join(upload_dir, attach.filename)
                attach.save(path)
                attachment_paths.append(path)

        # Read CSV and send emails
        with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            if "email" not in reader.fieldnames or "Dear" not in reader.fieldnames:
                return "Error: The CSV file must contain 'email' and 'Dear' columns."
            
            for row in reader:
                recipient_email = row["email"]
                recipient_name = row["Dear"]
                personalized_body = body_template.replace("{Dear}", recipient_name)

                send_email_via_graph(recipient_email, subject, personalized_body, attachment_paths)
                sleep(15)  # Pause 5 seconds between each email

        return "Emails sent successfully!"
    
    return render_template("send_email.html")

def send_email_via_graph(to_email, subject, body, attachment_paths=None):
    global access_token

    # Build the email payload with HTML body
    email_data = {
        "message": {
            "subject": subject,
            "body": {"contentType": "HTML", "content": body},
            "toRecipients": [{"emailAddress": {"address": to_email}}],
            "attachments": []
        },
        "saveToSentItems": "true"
    }

    # Process every attachment in the list if provided
    if attachment_paths:
        for attachment_path in attachment_paths:
            try:
                with open(attachment_path, "rb") as file_obj:
                    file_content = file_obj.read()
                if not file_content:
                    print(f"Failed to read attachment {attachment_path}. No content found.")
                    continue
                # Encode file in Base64
                encoded_content = base64.b64encode(file_content).decode("utf-8")
                # Determine MIME type based on file extension
                content_type, _ = mimetypes.guess_type(attachment_path)
                if content_type is None:
                    content_type = "application/octet-stream"
                email_data["message"]["attachments"].append({
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": os.path.basename(attachment_path),
                    "contentType": content_type,
                    "contentBytes": encoded_content
                })
            except Exception as e:
                print(f"Error processing attachment {attachment_path}: {e}")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        url="https://graph.microsoft.com/v1.0/me/sendMail",
        headers=headers,
        json=email_data
    )

    if response.status_code == 202:
        print(f"Email sent successfully to {to_email}!")
    else:
        print(f"Failed to send email to {to_email}: {response.json()}")

if __name__ == "__main__":
    app.run(debug=True)
