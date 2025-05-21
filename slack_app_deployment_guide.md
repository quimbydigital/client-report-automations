# Slack App Deployment Guide

This guide provides step-by-step instructions for creating and deploying the Slack app for the client report automation workflow.

## 1. Create a New Slack App

1. **Go to the Slack API website**:
   - Visit [https://api.slack.com/apps](https://api.slack.com/apps )
   - Sign in with your Slack workspace credentials

2. **Create a new app**:
   - Click the "Create New App" button
   - Select "From scratch"
   - Enter "Client Report Automation" as the App Name
   - Select your workspace from the dropdown
   - Click "Create App"

## 2. Configure App Features

### Basic Information

1. Navigate to "Basic Information" in the left sidebar
2. Under "Display Information":
   - Upload an app icon (optional)
   - Set the background color to match your brand (optional)
   - Add a short description: "Automates client performance report generation and notifications"

### Bot Token Scopes

1. Navigate to "OAuth & Permissions" in the left sidebar
2. Scroll down to "Scopes" section
3. Under "Bot Token Scopes", click "Add an OAuth Scope"
4. Add the following scopes:
   - `chat:write` (Send messages as the app)
   - `commands` (Add slash commands to the app)
   - `files:read` (Access files in channels & conversations)
   - `files:write` (Upload, edit, and delete files)
   - `channels:read` (View basic information about public channels)
   - `groups:read` (View basic information about private channels)

### Slash Commands

1. Navigate to "Slash Commands" in the left sidebar
2. Click "Create New Command"
3. Configure the first command:
   - Command: `/manus-generate`
   - Request URL: `https://your-server.com/slack/commands` (you'll update this later )
   - Short Description: "Generate a report for a specific client"
   - Usage Hint: "[client-name]"
   - Click "Save"

4. Repeat to create two more commands:
   - Command: `/manus-status`
     - Request URL: `https://your-server.com/slack/commands`
     - Short Description: "Check the status of all client reports"
   
   - Command: `/manus-help`
     - Request URL: `https://your-server.com/slack/commands`
     - Short Description: "Get help with client report commands"

### App Home

1. Navigate to "App Home" in the left sidebar
2. Enable the "Home Tab"
3. Enable "Messages Tab"
4. Check "Allow users to send Slash commands and messages from the messages tab"

## 3. Install the App to Your Workspace

1. Navigate to "Install App" in the left sidebar
2. Click "Install to Workspace"
3. Review the permissions and click "Allow"
4. After installation, you'll be redirected to the "OAuth & Permissions" page
5. Copy the "Bot User OAuth Token" (starts with `xoxb-` ) - you'll need this for your `.env` file

## 4. Set Up the Server

### Option 1: Using AWS (Recommended)

1. **Set up an EC2 instance**:
   - Create a small EC2 instance (t2.micro is sufficient)
   - Use Amazon Linux 2 as the operating system
   - Configure security groups to allow HTTP/HTTPS traffic
   - Connect to your instance using SSH

2. **Install dependencies**:
   ```bash
   sudo yum update -y
   sudo yum install -y python3 python3-pip git
   sudo yum install -y tesseract tesseract-langpack-eng
   sudo yum install -y poppler-utils
