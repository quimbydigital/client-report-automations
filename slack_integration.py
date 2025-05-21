#!/usr/bin/env python3
"""
Slack Integration Module for Client Report Automation

This module provides Slack integration for the client report automation workflow,
including notifications and slash commands.
"""

import os
import logging
import json
from flask import Flask, request, Response
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("slack_integration.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize Slack client
slack_token = os.getenv("SLACK_BOT_TOKEN")
slack_client = WebClient(token=slack_token)
default_channel = os.getenv("SLACK_DEFAULT_CHANNEL", "#client-reports")

class SlackIntegration:
    """
    Provides Slack integration for the client report automation workflow.
    """
    
    @staticmethod
    def notify_report_ready(client_name, month, url, channel=None):
        """
        Send a notification that a report is ready.
        
        Args:
            client_name (str): Name of the client
            month (str): Month of the report
            url (str): URL to the report
            channel (str, optional): Slack channel to send the notification to
            
        Returns:
            bool: True if the notification was sent successfully, False otherwise
        """
        if not channel:
            channel = default_channel
        
        try:
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"📊 {client_name} Report Ready for {month}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"The monthly performance report for *{client_name}* is now ready for review."
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*<{url}|View Report>*"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "Please review before sharing with the client."
                        }
                    ]
                }
            ]
            
            result = slack_client.chat_postMessage(
                channel=channel,
                blocks=blocks,
                text=f"📊 {client_name} Report Ready for {month}"
            )
            
            logger.info(f"Sent report ready notification for {client_name} to {channel}")
            return True
        except SlackApiError as e:
            logger.error(f"Error sending report ready notification: {e}")
            return False
    
    @staticmethod
    def notify_missing_data(client_name, month, missing_items, channel=None):
        """
        Send a notification about missing data.
        
        Args:
            client_name (str): Name of the client
            month (str): Month of the report
            missing_items (list): List of missing items
            channel (str, optional): Slack channel to send the notification to
            
        Returns:
            bool: True if the notification was sent successfully, False otherwise
        """
        if not channel:
            channel = default_channel
        
        try:
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"⚠️ Missing Data for {client_name} ({month})"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"The following items are missing for *{client_name}* for *{month}*:"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "\n".join([f"• {item}" for item in missing_items])
                    }
                }
            ]
            
            result = slack_client.chat_postMessage(
                channel=channel,
                blocks=blocks,
                text=f"⚠️ Missing Data for {client_name} ({month})"
            )
            
            logger.info(f"Sent missing data notification for {client_name} to {channel}")
            return True
        except SlackApiError as e:
            logger.error(f"Error sending missing data notification: {e}")
            return False
    
    @staticmethod
    def notify_error(client_name, month, error, channel=None):
        """
        Send a notification about an error.
        
        Args:
            client_name (str): Name of the client
            month (str): Month of the report
            error (str): Error message
            channel (str, optional): Slack channel to send the notification to
            
        Returns:
            bool: True if the notification was sent successfully, False otherwise
        """
        if not channel:
            channel = default_channel
        
        try:
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"❌ Error Processing {client_name} ({month})"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"An error occurred while processing *{client_name}* for *{month}*:"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"```{error}```"
                    }
                }
            ]
            
            result = slack_client.chat_postMessage(
                channel=channel,
                blocks=blocks,
                text=f"❌ Error Processing {client_name} ({month})"
            )
            
            logger.info(f"Sent error notification for {client_name} to {channel}")
            return True
        except SlackApiError as e:
            logger.error(f"Error sending error notification: {e}")
            return False

@app.route("/slack/commands", methods=["POST"])
def handle_command():
    """
    Handle Slack slash commands.
    
    Returns:
        Response: Flask response
    """
    # Verify request
    # In a production environment, you should verify the request signature
    
    # Parse request
    command = request.form.get("command")
    text = request.form.get("text")
    user_id = request.form.get("user_id")
    channel_id = request.form.get("channel_id")
    
    logger.info(f"Received command: {command} {text} from {user_id} in {channel_id}")
    
    # Handle commands
    if command == "/manus-generate":
        # Generate report for a client
        if not text:
            return Response("Please specify a client name. Usage: /manus-generate [client-name]", 200)
        
        # In a real implementation, this would trigger the report generation process
        # For now, we'll just return a message
        return Response(f"Generating report for {text}... This may take a few minutes.", 200)
    
    elif command == "/manus-status":
        # Check status of all client reports
        # In a real implementation, this would check the status of all client reports
        # For now, we'll just return a message
        return Response("Checking status of all client reports...", 200)
    
    elif command == "/manus-help":
        # Show help
        help_text = """
*Client Report Automation Commands*

*/manus-generate [client-name]*
Generate a report for a specific client

*/manus-status*
Check the status of all client reports

*/manus-help*
Show this help message
"""
        return Response(help_text, 200)
    
    else:
        return Response(f"Unknown command: {command}", 200)

if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=5000)
