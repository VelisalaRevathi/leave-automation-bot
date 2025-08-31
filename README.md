# Leave Tracker Bot

🚀 Leave Tracker Bot  is an HR automation tool that helps HR teams manage employee leave requests efficiently.
It automatically:

* Reads leave request emails from Gmail,
* Parses leave dates (Full Day, Half Day, WFH),
* Updates Google Sheets (both monthly & summary sheets),
* Sends approval/rejection replies,
* Generates and emails monthly leave summaries to employees.



📌 Features

✅ Automates *leave approval workflow* from Gmail.
✅ Supports *Full Day, Half Day, and WFH* requests.
✅ Updates both *monthly sheet* and *summary sheet* in Google Sheets.
✅ Sends *email replies* on approval or rejection.
✅ Generates *monthly summary reports* and emails them to employees.
✅ Simple *menu-based interface* for HR.


 🖥 Installation

Step 1: Clone Repository

bash
git clone https://github.com/<your-username>/Leave-Tracker-Bot.git
cd Leave-Tracker-Bot


 Step 2: Create Virtual Environment

bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac


 Step 3: Install Dependencies

bash
pip install --upgrade pip
pip install -r requirements.txt


---

 ⚙ Configuration

 1. Setup Environment Variables

Create a .env file in the project root:

ini
SENDER_EMAIL=your_email@example.com
SENDER_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465


 2. Google Sheets API

* Enable *Google Sheets API* in [Google Cloud Console](https://console.cloud.google.com/).
* Download service-account-key.json and place it in the project root.
* Share your Google Sheet with the *service account email*.

 3. Gmail API

* Enable *Gmail API* in Google Cloud Console.
* Download credentials.json and place it in the project root.
* On first run, authenticate with your Google account — this will generate token.json.

---

 ▶ Usage

Run the main script:

bash
python main.py


You’ll see a menu:


🚀 HR Automation Tool 🚀
========================================
1. Process Daily Leave Approvals
2. Send Monthly Summaries
3. Exit


* *Option 1* → Reads Gmail for unread leave requests, updates sheets, and sends approval/rejection emails.
* *Option 2* → Generates & sends monthly leave summary emails to all employees.

---

 📊 Example Workflows

🔹 Daily Leave Approval

1. Fetches unread Gmail leave request emails.
2. Parses dates and types (Leave, Half-Day, WFH).
3. Updates Google Sheets (monthly + summary).
4. Sends an *approval/rejection email reply*.

🔹 Monthly Leave Summaries

1. Reads employee data from *Summary Sheet*.
2. Fetches current month’s leave/WFH data.
3. Generates a formatted summary table.
4. Sends the report to each employee by email.

---

 👨‍💻 Tech Stack

* *Python 3.9+*
* *Gmail API* (email fetching)
* *Google Sheets API* (leave tracking)
* *pandas* (data processing)
* *smtplib* (sending emails)
* *dateparser* (natural language date parsing)

---

 🔒 Security Notes

* Do *NOT* commit .env, credentials.json, service-account-key.json, or token.json.
* Use .gitignore to keep credentials private.

---
