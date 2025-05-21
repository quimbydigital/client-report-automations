#!/bin/bash
# Installation script for Client Report Automation

echo "Installing Client Report Automation..."

# Update system
sudo yum update -y || sudo apt-get update -y

# Install required packages
if command -v yum &> /dev/null; then
    # Amazon Linux / CentOS / RHEL
    sudo yum install -y python3 python3-pip git tesseract tesseract-langpack-eng poppler-utils nodejs npm
else
    # Ubuntu / Debian
    sudo apt-get install -y python3 python3-pip git tesseract-ocr tesseract-ocr-eng poppler-utils nodejs npm
fi

# Install Python dependencies
pip3 install -r requirements.txt

# Create directory structure
python3 setup.py --base-dir ~/Client_Monthly_Reports

echo "Installation complete!"
echo "Next steps:"
echo "1. Create a Slack app following the slack_app_deployment_guide.md"
echo "2. Set up your .env file with your Slack token"
echo "3. Follow the monthly_workflow_guide.md to start using the system"
