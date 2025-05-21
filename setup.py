#!/usr/bin/env python3
"""
Setup Script for Client Report Automation

This script sets up the environment for the client report automation workflow,
including creating the initial directory structure.
"""

import os
import sys
import subprocess
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("setup.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_directory_structure(base_dir, client_names=None):
    """
    Create the initial directory structure for client reports.
    
    Args:
        base_dir (str): Base directory for client reports
        client_names (list, optional): List of client names. If None, create only the base directory.
        
    Returns:
        bool: True if directory creation was successful, False otherwise
    """
    try:
        # Create base directory
        os.makedirs(base_dir, exist_ok=True)
        logger.info(f"Created base directory: {base_dir}")
        
        # Create client directories if specified
        if client_names:
            for client_name in client_names:
                client_dir = os.path.join(base_dir, client_name)
                os.makedirs(client_dir, exist_ok=True)
                
                # Create subdirectories
                os.makedirs(os.path.join(client_dir, "Strategy_Deck"), exist_ok=True)
                os.makedirs(os.path.join(client_dir, "Monthly_Data"), exist_ok=True)
                os.makedirs(os.path.join(client_dir, "Generated_Reports"), exist_ok=True)
                os.makedirs(os.path.join(client_dir, "Processed_Data"), exist_ok=True)
                
                logger.info(f"Created directory structure for client: {client_name}")
        
        return True
    except Exception as e:
        logger.error(f"Error creating directory structure: {e}")
        return False

def create_env_file(slack_token=None, slack_channel=None, report_base_url=None):
    """
    Create .env file with environment variables.
    
    Args:
        slack_token (str, optional): Slack bot token
        slack_channel (str, optional): Default Slack channel
        report_base_url (str, optional): Base URL for reports
        
    Returns:
        bool: True if file creation was successful, False otherwise
    """
    try:
        with open(".env", "w") as f:
            f.write("# Environment variables for Client Report Automation\n\n")
            
            if slack_token:
                f.write(f"SLACK_BOT_TOKEN={slack_token}\n")
            else:
                f.write("# SLACK_BOT_TOKEN=your_slack_bot_token\n")
            
            if slack_channel:
                f.write(f"SLACK_DEFAULT_CHANNEL={slack_channel}\n")
            else:
                f.write("# SLACK_DEFAULT_CHANNEL=#client-reports\n")
            
            if report_base_url:
                f.write(f"REPORT_BASE_URL={report_base_url}\n")
            else:
                f.write("# REPORT_BASE_URL=https://client-reports.example.com\n" )
        
        logger.info("Created .env file")
        return True
    except Exception as e:
        logger.error(f"Error creating .env file: {e}")
        return False

def main():
    """
    Main entry point for the script.
    """
    parser = argparse.ArgumentParser(description="Setup Script for Client Report Automation")
    parser.add_argument("--base-dir", default="Client_Monthly_Reports", help="Base directory for client reports")
    parser.add_argument("--clients", nargs="+", help="List of client names to create directories for")
    parser.add_argument("--slack-token", help="Slack bot token")
    parser.add_argument("--slack-channel", help="Default Slack channel")
    parser.add_argument("--report-base-url", help="Base URL for reports")
    
    args = parser.parse_args()
    
    success = True
    
    # Create directory structure
    success = create_directory_structure(args.base_dir, args.clients) and success
    
    # Create .env file
    success = create_env_file(args.slack_token, args.slack_channel, args.report_base_url) and success
    
    if success:
        logger.info("Setup completed successfully")
        print("\nSetup completed successfully!")
        print(f"Base directory: {args.base_dir}")
        if args.clients:
            print(f"Created directories for clients: {', '.join(args.clients)}")
        print("\nNext steps:")
        print("1. Upload client strategy decks to [Client_Name]/Strategy_Deck/")
        print("2. Create monthly data directories in [Client_Name]/Monthly_Data/")
        print("3. Upload performance screenshots and highlights to monthly directories")
        print("4. Run the automation script: python client_report_automation.py [base_dir]")
        return 0
    else:
        logger.error("Setup failed")
        print("\nSetup failed. Please check the log file for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
