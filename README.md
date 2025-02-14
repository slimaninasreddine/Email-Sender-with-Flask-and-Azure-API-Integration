# Bulk Email Sender with Flask and Azure API Integration

This project is a **Flask-based web application** that allows users to send bulk emails with rich-text formatting and attachments using the **Microsoft Graph API**. The application supports personalization of email content using data from a CSV file, and it integrates with Azure for secure authentication and email sending.

---

## Features
- **Rich Text Editor**: Compose emails with bold text, italics, images, and more.
- **Bulk Email Sending**: Send personalized emails to multiple recipients using a CSV file.
- **Attachments**: Upload and send multiple attachments with your emails.
- **Azure Authentication**: Securely authenticate using the Microsoft Graph API.
- **HTML Email Support**: Send emails with rich-text formatting (HTML).

---

## Prerequisites
1. **Python 3.9+** installed on your machine.
2. An **Azure account** with access to the Azure portal.
3. A registered application in Azure Active Directory (AAD) with Microsoft Graph API permissions.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/slimaninasreddine/Email-Sender-with-Flask-and-Azure-API-Integration.git
cd bulk-email-sender
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```


---

## Step-by-Step Guide to Set Up Azure API

### Step 1: Register an Application in Azure AD
1. Log in to the [Azure Portal](https://portal.azure.com/).
2. Navigate to **Azure Active Directory > App registrations**.
3. Click on **+ New registration**.
4. Fill in the following details:
   - **Name**: Enter a name for your app (e.g., "Bulk Email Sender").
   - **Supported account types**: Select **Accounts in any organizational directory and personal Microsoft accounts (e.g., Skype, Xbox)**.
   - **Redirect URI**:
     - Select "Web" and enter `http://localhost:5000/callback`.
5. Click **Register**.

---

### Step 2: Configure API Permissions
1. In your app's overview page, go to **API Permissions**.
2. Click on **+ Add a permission > Microsoft Graph > Delegated permissions**.
3. Add the following permissions:
   - `Mail.Send`
   - `User.Read`
4. Click on **Grant admin consent for [Your Tenant Name]**.

---

### Step 3: Generate a Client Secret
1. Go to the **Certificates & Secrets** section.
2. Click on **+ New client secret**.
3. Provide a description (e.g., "Flask App Secret") and set an expiration period.
4. Click **Add**, then copy the secret value (you won't be able to see it again).

---

### Step 4: Note Down Required Values
From your app's overview page, note down the following:
- **Application (client) ID**
- **Directory (tenant) ID**
- The client secret you generated earlier.

---

## Configuration

1. Create a `.env` file in the project root directory:
```plaintext
FLASK_SECRET_KEY=your_random_secret_key_here
CLIENT_ID=your_application_client_id_here
CLIENT_SECRET=your_client_secret_here
TENANT_ID=common  # Use 'common' for personal accounts or your tenant ID for organizational accounts
```

2. Replace placeholders (`your_random_secret_key_here`, `your_application_client_id_here`, etc.) with your actual values from Azure.

---

## Running the Application

1. Start the Flask app:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`.

---

## Usage

### Upload CSV File Format
The CSV file should have two columns:
- `email`: The recipient's email address.
- `Dear`: The recipient's name.

Example:
```csv
email,Dear
example1@example.com,John
example2@example.com,Jane
```

### Steps to Send Emails:
1. Log in using your Microsoft account via Azure authentication.
2. Upload the CSV file containing recipient details.
3. Compose your email using the rich-text editor.
4. Attach files (optional).
5. Click "Send Email."

---

## Troubleshooting

### Common Issues & Fixes

#### Issue: "InvalidAuthenticationToken"
- Ensure that you are using a valid access token from Azure.
- Check that your app has the correct permissions (`Mail.Send`, `User.Read`).

#### Issue: "No file uploaded"
- Ensure that your form includes `enctype="multipart/form-data"`.

#### Issue: "JWT is not well formed"
- Verify that your `.env` file contains correct values for `CLIENT_ID`, `CLIENT_SECRET`, and `TENANT_ID`.

---

## Technologies Used

- Flask (Python Web Framework)
- Microsoft Graph API (for email sending)
- HTML5 & CSS (Frontend)
- JavaScript (Rich Text Editor)


---

With this setup guide, you can quickly configure and deploy the Bulk Email Sender application while integrating securely with Azure's Microsoft Graph API!

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52444344/2f5c33c3-a870-43a2-892d-9167ebb163f2/contact.csv
[2] https://learn.microsoft.com/fi-fi/azure/developer/python/tutorial-python-managed-identity-cli
[3] https://www.eginnovations.com/documentation/Office-365/Registering-MS-Graph-App-On-Azure-AD.htm
[4] https://uwconnect.uw.edu/it?id=kb_article_view&sysparm_article=KB0034053
[5] https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
[6] https://mailtrap.io/blog/flask-email-sending/
[7] https://learn.microsoft.com/en-us/azure/developer/python/tutorial-containerize-simple-web-app-for-app-service
[8] https://stackoverflow.com/questions/68575490/register-an-application-in-azure-ad-using-the-graph-api
[9] https://learn.microsoft.com/en-au/power-apps/developer/data-platform/walkthrough-register-app-azure-active-directory
[10] https://stackoverflow.com/questions/53906301/hosting-flaskpython-api-on-azure-api
[11] https://learn.microsoft.com/en-us/azure/active-directory-b2c/microsoft-graph-get-started?tabs=applications
[12] https://learn.microsoft.com/vi-vn/azure/healthcare-apis/register-application
[13] https://learn.microsoft.com/en-us/samples/azure-samples/flask-app-on-azure-functions/azure-functions-python-create-flask-app/
[14] https://learn.microsoft.com/en-us/graph/app-registration
[15] https://learn.microsoft.com/en-au/entra/identity-platform/quickstart-register-app
[16] https://learn.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=bash
[17] https://learn.microsoft.com/en-us/graph/auth-register-app-v2?view=graph-rest-1.0
[18] https://www.youtube.com/watch?v=dCTjP2JkWAs
[19] https://www.youtube.com/watch?v=qqinLLccL2E
[20] https://www.youtube.com/watch?v=2eh0RLnWp08
[21] https://www.bdrsuite.com/blog/microsoft-365-for-beginners-azure-app-registration-permissions-step-by-step-part-38/
[22] https://www.youtube.com/watch?v=L6zwKy7ZgTM
[23] https://www.youtube.com/watch?v=gai4zKpA4cI
[24] https://flask-ckeditor.readthedocs.io/en/latest/
[25] https://flask.palletsprojects.com/en/stable/
[26] https://stackoverflow.com/questions/71143583/send-bulk-emails-in-background-task-with-flask
[27] https://www.gitauharrison.com/articles/rich-text
[28] https://flask.palletsprojects.com/en/stable/lifecycle/
[29] https://www.mlcs.xyz/tutorials/send_email_using_flask
[30] https://stackoverflow.com/questions/44633860/flask-form-with-rich-text-in-place-editing
[31] https://github.com/shubhtoy/Bulk-Email-Sender-Flask-Mailgun
[32] https://www.youtube.com/watch?v=ZxG_HDEJ3nI
[33] https://mailtrap.io/blog/flask-send-email-gmail/
[34] https://www.reddit.com/r/flask/comments/1bb8w30/rich_text_editors/
[35] https://pypi.org/project/Flask-Mail/
[36] https://froala.com/blog/general/easily-upload-images-to-your-server-with-python-flask/
[37] https://www.bairesdev.com/blog/what-is-flask/
[38] https://roytuts.com/how-to-send-bulk-emails-with-attachments-using-python-and-flask/
[39] https://www.youtube.com/watch?v=5jnAnnxZGQQ
[40] https://en.wikipedia.org/wiki/Flask_(web_framework)
[41] https://github.com/marktennyson/flask-mailing
