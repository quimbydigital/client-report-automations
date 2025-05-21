#!/usr/bin/env python3
"""
Main Orchestration Script for Client Report Automation

This script orchestrates the entire client report automation workflow,
including data processing, report generation, and Slack notifications.
"""

import os
import sys
import logging
import argparse
import json
from datetime import datetime
from dotenv import load_dotenv

# Import other modules
try:
    from pdf_extraction import PDFExtractor
    from image_analysis import ImageAnalyzer
    from insight_generation import InsightGenerator
    from report_generator import ReportGenerator
    from slack_integration import SlackIntegration
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all required modules are in the same directory.")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("client_report_automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ClientReportAutomation:
    """
    Main class for client report automation.
    """
    
    def __init__(self, base_dir, slack_channel=None):
        """
        Initialize the client report automation.
        
        Args:
            base_dir (str): Base directory for client reports
            slack_channel (str, optional): Slack channel for notifications
        """
        self.base_dir = base_dir
        self.slack_channel = slack_channel
        self.slack = SlackIntegration()
        
        # Create base directory if it doesn't exist
        os.makedirs(base_dir, exist_ok=True)
    
    def process_client(self, client_name, month=None):
        """
        Process a client's data and generate a report.
        
        Args:
            client_name (str): Name of the client
            month (str, optional): Month to process (directory name)
            
        Returns:
            bool: True if processing was successful, False otherwise
        """
        logger.info(f"Processing client: {client_name}")
        
        client_dir = os.path.join(self.base_dir, client_name)
        
        # Check if client directory exists
        if not os.path.isdir(client_dir):
            logger.error(f"Client directory not found: {client_dir}")
            if self.slack_channel:
                self.slack.notify_error(client_name, month or "Unknown", f"Client directory not found: {client_dir}", self.slack_channel)
            return False
        
        # Get the latest month if not specified
        if not month:
            monthly_data_dir = os.path.join(client_dir, "Monthly_Data")
            if not os.path.isdir(monthly_data_dir):
                logger.error(f"Monthly data directory not found: {monthly_data_dir}")
                if self.slack_channel:
                    self.slack.notify_error(client_name, "Unknown", f"Monthly data directory not found: {monthly_data_dir}", self.slack_channel)
                return False
            
            months = [d for d in os.listdir(monthly_data_dir) if os.path.isdir(os.path.join(monthly_data_dir, d))]
            if not months:
                logger.error(f"No monthly data directories found in: {monthly_data_dir}")
                if self.slack_channel:
                    self.slack.notify_error(client_name, "Unknown", f"No monthly data directories found in: {monthly_data_dir}", self.slack_channel)
                return False
            
            month = sorted(months)[-1]  # Get the latest month
        
        logger.info(f"Processing month: {month}")
        
        # Check for required directories and files
        strategy_deck_dir = os.path.join(client_dir, "Strategy_Deck")
        monthly_data_dir = os.path.join(client_dir, "Monthly_Data", month)
        processed_data_dir = os.path.join(client_dir, "Processed_Data")
        generated_reports_dir = os.path.join(client_dir, "Generated_Reports")
        
        # Create directories if they don't exist
        os.makedirs(processed_data_dir, exist_ok=True)
        os.makedirs(generated_reports_dir, exist_ok=True)
        
        # Check if monthly data directory exists
        if not os.path.isdir(monthly_data_dir):
            logger.error(f"Monthly data directory not found: {monthly_data_dir}")
            if self.slack_channel:
                self.slack.notify_error(client_name, month, f"Monthly data directory not found: {monthly_data_dir}", self.slack_channel)
            return False
        
        # Check for missing files
        missing_items = []
        
        # Check for strategy deck
        strategy_decks = [f for f in os.listdir(strategy_deck_dir) if f.endswith(".pdf")] if os.path.isdir(strategy_deck_dir) else []
        if not strategy_decks:
            missing_items.append("Strategy deck (PDF)")
        
        # Check for screenshots
        screenshots = [f for f in os.listdir(monthly_data_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))] if os.path.isdir(monthly_data_dir) else []
        if not screenshots:
            missing_items.append("Performance screenshots (PNG, JPG)")
        
        # Check for highlights
        highlights_files = [f for f in os.listdir(monthly_data_dir) if f.lower().endswith(".txt") and "highlight" in f.lower()] if os.path.isdir(monthly_data_dir) else []
        if not highlights_files:
            missing_items.append("Highlights text file (TXT)")
        
        # Notify about missing items
        if missing_items:
            logger.warning(f"Missing items for {client_name} ({month}): {', '.join(missing_items)}")
            if self.slack_channel:
                self.slack.notify_missing_data(client_name, month, missing_items, self.slack_channel)
            return False
        
        try:
            # Process strategy deck
            strategy_deck_path = os.path.join(strategy_deck_dir, strategy_decks[0])
            pdf_extractor = PDFExtractor()
            strategy_data = pdf_extractor.extract_data(strategy_deck_path)
            
            # Save strategy data
            strategy_data_path = os.path.join(processed_data_dir, f"{month}_strategy_data.json")
            with open(strategy_data_path, "w") as f:
                json.dump(strategy_data, f, indent=2)
            
            # Process screenshots
            image_analyzer = ImageAnalyzer()
            metrics_data = {}
            
            for screenshot in screenshots:
                screenshot_path = os.path.join(monthly_data_dir, screenshot)
                metrics = image_analyzer.analyze_image(screenshot_path)
                metrics_data[screenshot] = metrics
            
            # Save metrics data
            metrics_data_path = os.path.join(processed_data_dir, f"{month}_metrics_data.json")
            with open(metrics_data_path, "w") as f:
                json.dump(metrics_data, f, indent=2)
            
            # Process highlights
            highlights_path = os.path.join(monthly_data_dir, highlights_files[0])
            with open(highlights_path, "r") as f:
                highlights_text = f.read()
            
            # Generate insights
            insight_generator = InsightGenerator()
            insights = insight_generator.generate_insights(strategy_data, metrics_data, highlights_text)
            
            # Save insights
            insights_path = os.path.join(processed_data_dir, f"{month}_insights.json")
            with open(insights_path, "w") as f:
                json.dump(insights, f, indent=2)
            
            # Generate report
            report_generator = ReportGenerator()
            report_path = os.path.join(generated_reports_dir, month)
            report_url = report_generator.generate_report(
                client_name,
                month,
                strategy_data,
                metrics_data,
                insights,
                highlights_text,
                screenshots=[os.path.join(monthly_data_dir, s) for s in screenshots],
                output_dir=report_path
            )
            
            # Notify report ready
            if self.slack_channel:
                self.slack.notify_report_ready(client_name, month, report_url, self.slack_channel)
            
            logger.info(f"Successfully processed {client_name} for {month}")
            return True
        
        except Exception as e:
            logger.error(f"Error processing {client_name} for {month}: {e}")
            if self.slack_channel:
                self.slack.notify_error(client_name, month, str(e), self.slack_channel)
            return False
    
    def process_all_clients(self, month=None):
        """
        Process all clients in the base directory.
        
        Args:
            month (str, optional): Month to process (directory name)
            
        Returns:
            dict: Dictionary of client names and processing results
        """
        logger.info(f"Processing all clients in {self.base_dir}")
        
        results = {}
        
        # Get all client directories
        client_dirs = [d for d in os.listdir(self.base_dir) if os.path.isdir(os.path.join(self.base_dir, d))]
        
        for client_name in client_dirs:
            results[client_name] = self.process_client(client_name, month)
        
        return results

def main():
    """
    Main entry point for the script.
    """
    parser = argparse.ArgumentParser(description="Client Report Automation")
    parser.add_argument("base_dir", help="Base directory for client reports")
    parser.add_argument("--client", help="Name of the client to process (default: all clients)")
    parser.add_argument("--month", help="Month to process (directory name, default: latest month)")
    parser.add_argument("--slack-channel", help="Slack channel for notifications")
    parser.add_argument("--review", action="store_true", help="Generate reports for review (won't send to clients)")
    
    args = parser.parse_args()
    
    logger.info(f"Starting client report automation with base directory: {args.base_dir}")
    logger.info(f"Client: {args.client if args.client else 'all clients'}")
    logger.info(f"Month: {args.month if args.month else 'latest month'}")
    logger.info(f"Slack channel: {args.slack_channel if args.slack_channel else 'default channel'}")
    logger.info(f"Review mode: {args.review}")
    
    automation = ClientReportAutomation(args.base_dir, args.slack_channel)
    
    if args.client:
        # Process a specific client
        success = automation.process_client(args.client, args.month)
        logger.info(f"Processing {args.client}: {'Success' if success else 'Failed'}")
        return 0 if success else 1
    else:
        # Process all clients
        results = automation.process_all_clients(args.month)
        success_count = sum(1 for result in results.values() if result)
        logger.info(f"Processed {len(results)} clients, {success_count} successful, {len(results) - success_count} failed")
        return 0 if success_count == len(results) else 1

if __name__ == "__main__":
    sys.exit(main())
