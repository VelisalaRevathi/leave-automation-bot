# main.py

import leave_request_handler
import google_sheet_handler
import summary_generator
import email_sender
from datetime import datetime
import pandas as pd

def run_daily_approvals():
    """
    WORKFLOW 1: Fetches unread leave request emails and processes them for approval.
    """
    print("\n🚀 Starting: Daily Leave Approval Workflow...")
    
    # Get all unread leave request emails
    requests = leave_request_handler.get_leave_requests()
    
    if requests:
        # Get the main summary sheet data, which is needed for processing
        df, spreadsheet, summary_ws, headers = google_sheet_handler.get_sheet_data()
        
        # Ensure all sheet data was loaded correctly before proceeding
        if all([df is not None, spreadsheet, summary_ws, headers]):
            leave_request_handler.process_requests(requests, df, spreadsheet, summary_ws, headers)

def run_monthly_summaries():
    """
    WORKFLOW 2: Generates and sends a summary email to every employee for the current month.
    """
    print("\n🚀 Starting: Send Monthly Summaries Workflow...")
    current_month = datetime.now().strftime('%b')
    print(f"🗓  Current Month Identified: {current_month}")

    # --- THIS IS THE FIXED LINE ---
    # It now correctly unpacks all 4 values returned by the function.
    employee_df, _, _, _ = google_sheet_handler.get_sheet_data()
    if employee_df is None:
        return

    # Get data from the current month's sheet
    df_monthly = google_sheet_handler.get_monthly_dataframe()

    print(f"\nProcessing {len(employee_df)} employee records...\n" + "-"*30)

    for index, employee in employee_df.iterrows():
        employee_name = employee['Name']
        employee_email = employee['Email']

        if not isinstance(employee_email, str) or '@' not in employee_email:
            print(f"⚠  Skipping {employee_name}: Invalid or missing email address.")
            continue
        
        # Default values
        wfh_count = 0
        sandwich_leaves = 0
        
        # Calculate WFH and Sandwich leaves from the monthly sheet if it exists
        if df_monthly is not None and not df_monthly.empty:
            employee_monthly_records = df_monthly[df_monthly['Name'] == employee_name]
            if not employee_monthly_records.empty:
                if 'W' in employee_monthly_records.columns:
                    wfh_count = pd.to_numeric(employee_monthly_records['W'], errors='coerce').fillna(0).sum()
                if 'S' in employee_monthly_records.columns:
                    sandwich_leaves = pd.to_numeric(employee_monthly_records['S'], errors='coerce').fillna(0).sum()
        
        email_subject = f"Your Leave Summary for {current_month}-2025"
        email_body = summary_generator.generate_summary(employee, current_month, wfh_count, sandwich_leaves)

        print(f"📧 Sending summary to {employee_name} ({employee_email})...")
        was_sent = email_sender.send_email(recipient_email=employee_email, subject=email_subject, body=email_body)

        if was_sent:
            print(f"✅ Email sent successfully.")
        else:
            print(f"❌ Failed to send email.")
        print("-" * 30)

def main():
    """
    Main function to run the HR automation tool with a user menu.
    """
    print("🚀 HR Automation Tool 🚀")
    print("="*40)

    while True:
        print("\nPlease choose an option:")
        print("  1. Process Daily Leave Approvals")
        print("  2. Send Monthly Summaries")
        print("  3. Exit")
        
        choice = input("👉 Enter your choice (1, 2, or 3): ")

        if choice == '1':
            run_daily_approvals()
        elif choice == '2':
            run_monthly_summaries()
        elif choice == '3':
            print("👋 Exiting the program.")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
        
        print("\n🎉 Task finished. Returning to menu.")


if __name__ == "__main__":
    main()