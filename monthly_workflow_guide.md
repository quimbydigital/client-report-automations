# Monthly Automation Workflow Guide

This guide explains the monthly workflow for the client report automation system, including how to prepare data, trigger the automation, and review the results.

## Monthly Workflow Overview

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Data Upload    │     │  Automation     │     │  Report         │
│  - Screenshots  │ ──> │  Trigger        │ ──> │  Generation     │
│  - Highlights   │     │  - Slack        │     │  - Processing   │
│  - Monthly data │     │  - Manual       │     │  - Website      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
│
▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Client         │     │  Deployment     │     │  Slack          │
│  Review         │ <── │  - Hosting      │ <── │  Notification   │
│  - Feedback     │     │  - URL          │     │  - Report ready │
│  - Approval     │     │  - Archive      │     │  - Status       │
└─────────────────┘     └─────────────────┘     └─────────────────┘

## Step 1: Monthly Data Preparation (Account Manager Task)

At the beginning of each month, account managers need to prepare the data for the previous month's reports:

1. **Create Monthly Directory**:
   - Navigate to each client's folder: `Client_Monthly_Reports/[Client_Name]/Monthly_Data/`
   - Create a new directory for the month: `YYYY_MM_MonthName` (e.g., `2025_05_May`)

2. **Gather Performance Screenshots**:
   - Take screenshots of performance dashboards from various platforms:
     - Facebook insights/analytics
     - Instagram insights
     - TikTok analytics
     - Other relevant platforms
   - Save screenshots with descriptive filenames:
     - `facebook_overview_may.png`
     - `instagram_engagement_may.png`
     - `tiktok_performance_may.png`

3. **Create Highlights Text File**:
   - Create a text file named `[MonthName]_Highlights.txt` (e.g., `May_Highlights.txt`)
   - Write a brief summary of what the client did well
   - Include any key observations or achievements
   - Format as plain text with clear paragraphs

4. **Upload Files to Monthly Directory**:
   - Place all screenshots and the highlights text file in the client's monthly directory
   - Ensure all files are properly named and formatted

## Step 2: Triggering the Automation

Once the data is prepared, you can trigger the automation process in one of two ways:

### Option 1: Using Slack Commands (Recommended)

1. **Generate Report for a Specific Client**:
   - Open Slack and type: `/manus-generate [Client_Name]`
   - Example: `/manus-generate ClientA`
   - The system will acknowledge the command and begin processing

2. **Check Status of All Reports**:
   - Type: `/manus-status`
   - This will show the current status of all client reports
   - Example statuses: "Not started", "Processing", "Complete", "Error"

3. **Get Help with Commands**:
   - Type: `/manus-help`
   - This will display all available commands and their usage

### Option 2: Manual Execution

1. **Run the Automation Script**:
   - SSH into your server
   - Navigate to the automation directory
   - Run: `python client_report_automation.py Client_Monthly_Reports --client [Client_Name] --month [YYYY_MM_MonthName] --slack-channel #client-reports`
   - To process all clients: `python client_report_automation.py Client_Monthly_Reports --slack-channel #client-reports`

## Step 3: Automated Processing

The system will automatically perform the following steps:

1. **PDF Extraction**:
   - Extract KPIs and content pillars from the client's strategy deck
   - Store the extracted information in a structured JSON format

2. **Image Analysis**:
   - Process screenshots to extract performance metrics
   - Identify platform-specific metrics (engagement rate, growth, etc.)
   - Store the extracted metrics in a structured JSON format

3. **Insight Generation**:
   - Compare extracted metrics against KPIs
   - Analyze trends across platforms
   - Incorporate account manager highlights
   - Generate data-driven insights and a key takeaway

4. **Report Generation**:
   - Create a professional, responsive website for the client's monthly report
   - Include visualizations, metrics, insights, and screenshot gallery
   - Add chronological archive functionality
   - Provide PDF download option

5. **Deployment**:
   - Deploy the generated website to a public URL
   - Store deployment information for future reference

## Step 4: Notification and Review

Once the report is generated and deployed, the system will:

1. **Send Slack Notification**:
   - Notify the specified Slack channel that the report is ready
   - Include the client name, month, and URL to the report
   - Provide a button to view the report

2. **Account Manager Review**:
   - Account managers should review the generated report
   - Check for accuracy and presentation
   - Make note of any issues or improvements

3. **Client Sharing**:
   - Once approved, account managers can share the report URL with clients
   - Consider adding a personalized message when sharing

## Step 5: Archiving and Maintenance

The system automatically handles archiving:

1. **Chronological Archive**:
   - Each new report is added to the client's archive
   - Previous months' reports remain accessible via the archive section

2. **File Management**:
   - All processed data is stored in the client's `Processed_Data` directory
   - Generated websites are stored in the client's `Generated_Reports` directory

## Best Practices for Efficient Monthly Workflow

1. **Prepare Data Early**:
   - Gather screenshots and write highlights as soon as the month ends
   - Don't wait until the last minute to prepare the data

2. **Use Consistent Naming**:
   - Follow a consistent naming convention for files and directories
   - This helps the system correctly identify and process the data

3. **Review Generated Reports Promptly**:
   - Check reports soon after they're generated
   - This allows time for any necessary corrections

4. **Document Any Issues**:
   - Keep track of any problems or limitations
   - This helps improve the system over time
