# google_sheet_handler.py
import gspread
import pandas as pd
from datetime import datetime

# --- Configuration ---
SERVICE_ACCOUNT_FILE = 'service-account-key.json'
GOOGLE_SHEET_NAME = 'Add your Google Sheet Name'  # Make sure this is your correct sheet name

# --- READ FUNCTIONS (For both workflows) ---

def get_sheet_data():
    """
    Connects to the main summary sheet ("Summary 2025") and reads all data.
    Returns the dataframe, spreadsheet object, worksheet object, and headers.
    """
    try:
        gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
        spreadsheet = gc.open(GOOGLE_SHEET_NAME)
        worksheet = spreadsheet.worksheet("Summary 2025")
        
        # Handles the two-row header structure
        header_row1 = worksheet.row_values(1)
        header_row2 = worksheet.row_values(2)
        final_headers = []
        for i, h1 in enumerate(header_row1):
            h2 = header_row2[i] if i < len(header_row2) else ''
            if h2 and h2 in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
                final_headers.append(h2)
            elif h1:
                final_headers.append(h1)
        
        data_rows = worksheet.get_all_values()[2:]
        df = pd.DataFrame(data_rows, columns=final_headers)
        
        print("✅ Main summary sheet data loaded successfully.")
        return df, spreadsheet, worksheet, final_headers
    except Exception as e:
        print(f"❌ An error occurred while accessing the Summary Sheet: {e}")
        return None, None, None, None

def get_monthly_dataframe():
    """
    Reads the data from the current month's sheet.
    """
    try:
        current_month_year = datetime.now().strftime('%B %Y')
        gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
        sh = gc.open(GOOGLE_SHEET_NAME)
        worksheet = sh.worksheet(current_month_year)
        
        all_data = worksheet.get_all_values()
        header = all_data[0]
        data_rows = all_data[1:]
        
        df_monthly = pd.DataFrame(data_rows, columns=header)
        
        print(f"✅ Monthly sheet '{current_month_year}' loaded successfully.")
        return df_monthly
    except gspread.exceptions.WorksheetNotFound:
        print(f"❌ ERROR: Worksheet for the current month '{current_month_year}' not found.")
        return None
    except Exception as e:
        print(f"❌ An error occurred while fetching monthly data: {e}")
        return None

# --- WRITE FUNCTIONS (For Daily Approval workflow) ---

def update_monthly_sheet(spreadsheet, employee_name, details):
    """
    Updates the current month's sheet with approved leave/WFH requests.
    """
    try:
        current_month_year = datetime.now().strftime('%B %Y')
        worksheet = spreadsheet.worksheet(current_month_year)
        header = worksheet.row_values(1)
        
        # Find the employee's row
        cell = worksheet.find(employee_name)
        if not cell:
            print(f"❌ Could not find '{employee_name}' in the monthly sheet.")
            return

        # Update cells for each approved date
        for item in details:
            day_str = str(item['date'].day)
            if day_str in header:
                day_col = header.index(day_str) + 1
                request_type_code = 'L'
                if item['type'] == 'HALF_DAY':
                    request_type_code = 'H'
                elif item['type'] == 'WFH':
                    request_type_code = 'W'
                worksheet.update_cell(cell.row, day_col, request_type_code)

        # Recalculate monthly totals for that employee
        row_values = worksheet.row_values(cell.row)
        lm_count = row_values.count('L') + (row_values.count('H') * 0.5)
        w_count = row_values.count('W')
        
        # Update LM (Leave Monthly) and W (WFH) columns
        if 'LM' in header:
            worksheet.update_cell(cell.row, header.index('LM') + 1, lm_count)
        if 'W' in header:
            worksheet.update_cell(cell.row, header.index('W') + 1, w_count)
        
        print(f"✅ Monthly sheet updated for {employee_name}.")
    except Exception as e:
        print(f"❌ An error occurred while updating the monthly sheet: {e}")

def update_summary_sheet(summary_worksheet, headers, employee_index, leave_items, wfh_items, df):
    """
    Updates the main "Summary 2025" sheet with new leave and WFH totals.
    """
    try:
        # Calculate totals from the approved request
        total_leave_days = sum(0.5 if item['type'] == 'HALF_DAY' else 1.0 for item in leave_items)
        total_wfh_days = len(wfh_items)

        # Get current values from the DataFrame
        current_used = float(df.loc[employee_index, 'Used'])
        current_wfh = float(df.loc[employee_index, 'WFH'])
        total_leaves = float(df.loc[employee_index, 'Total'])

        # Calculate new values
        new_used = current_used + total_leave_days
        new_wfh = current_wfh + total_wfh_days
        new_available = total_leaves - new_used
        
        # Find column numbers for updating
        used_col = headers.index('Used') + 1
        available_col = headers.index('Available') + 1
        wfh_col = headers.index('WFH') + 1
        
        # The employee_index from the DataFrame corresponds to the row in the sheet
        # We add 3 because sheet rows are 1-based and there are 2 header rows
        sheet_row = int(employee_index) + 3

        # Update the cells in the summary sheet
        summary_worksheet.update_cell(sheet_row, used_col, new_used)
        summary_worksheet.update_cell(sheet_row, available_col, new_available)
        summary_worksheet.update_cell(sheet_row, wfh_col, new_wfh)

        print(f"✅ Main summary sheet updated.")
    except Exception as e:
        print(f"❌ An error occurred while updating the summary sheet: {e}")