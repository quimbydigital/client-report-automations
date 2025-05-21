#!/usr/bin/env python3
"""
Report Generator Module for Client Report Automation

This module generates client report websites.
"""

import os
import logging
import json
import shutil
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("report_generator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ReportGenerator:
    """
    Generates client report websites.
    """
    
    def generate_report(self, client_name, month, strategy_data, metrics_data, insights, highlights_text, screenshots, output_dir):
        """
        Generate a client report website.
        
        Args:
            client_name (str): Name of the client
            month (str): Month of the report
            strategy_data (dict): Strategy data extracted from PDF
            metrics_data (dict): Metrics data extracted from images
            insights (dict): Generated insights
            highlights_text (str): Highlights text
            screenshots (list): List of screenshot paths
            output_dir (str): Output directory for the report
            
        Returns:
            str: URL to the generated report
        """
        logger.info(f"Generating report for {client_name} ({month})")
        
        try:
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Create assets directory
            assets_dir = os.path.join(output_dir, "assets")
            os.makedirs(assets_dir, exist_ok=True)
            
            # Copy screenshots to assets directory
            screenshot_paths = []
            for i, screenshot in enumerate(screenshots):
                screenshot_name = f"screenshot_{i+1}{os.path.splitext(screenshot)[1]}"
                screenshot_path = os.path.join(assets_dir, screenshot_name)
                shutil.copy(screenshot, screenshot_path)
                screenshot_paths.append(f"assets/{screenshot_name}")
            
            # Generate HTML
            html = self._generate_html(client_name, month, strategy_data, metrics_data, insights, highlights_text, screenshot_paths)
            
            # Write HTML to file
            index_path = os.path.join(output_dir, "index.html")
            with open(index_path, "w") as f:
                f.write(html)
            
            # Generate CSS
            css = self._generate_css()
            
            # Write CSS to file
            css_path = os.path.join(assets_dir, "style.css")
            with open(css_path, "w") as f:
                f.write(css)
            
            # Generate JavaScript
            js = self._generate_js()
            
            # Write JavaScript to file
            js_path = os.path.join(assets_dir, "script.js")
            with open(js_path, "w") as f:
                f.write(js)
            
            # Get report URL
            report_base_url = os.getenv("REPORT_BASE_URL", "http://localhost" )
            report_url = f"{report_base_url}/{client_name}/{month}"
            
            logger.info(f"Report generated successfully: {report_url}")
            
            return report_url
        
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return ""
    
    def _generate_html(self, client_name, month, strategy_data, metrics_data, insights, highlights_text, screenshot_paths):
        """
        Generate HTML for the report.
        
        Args:
            client_name (str): Name of the client
            month (str): Month of the report
            strategy_data (dict): Strategy data extracted from PDF
            metrics_data (dict): Metrics data extracted from images
            insights (dict): Generated insights
            highlights_text (str): Highlights text
            screenshot_paths (list): List of screenshot paths
            
        Returns:
            str: Generated HTML
        """
        # Format month for display
        display_month = month.replace("_", " ")
        if display_month.startswith("20"):
            # Remove year prefix if present
            parts = display_month.split(" ")
            if len(parts) >= 2:
                display_month = parts[1]
        
        # Generate HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{client_name} - {display_month} Performance Report</title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>{client_name}</h1>
            <h2>{display_month} Performance Report</h2>
        </div>
    </header>
    
    <main class="container">
        <section class="key-takeaway">
            <h3>Key Takeaway</h3>
            <p>{insights.get('key_takeaway', 'No key takeaway available.')}</p>
        </section>
        
        <section class="metrics">
            <h3>Performance Metrics</h3>
            <div class="metrics-grid">"""
        
        # Add metrics
        for image_name, data in metrics_data.items():
            platform = data.get("platform", "unknown").capitalize()
            metrics = data.get("metrics", {})
            
            if metrics:
                html += f"""
                <div class="metric-card">
                    <h4>{platform}</h4>
                    <ul>"""
                
                for metric_name, value in metrics.items():
                    html += f"""
                        <li><strong>{metric_name.capitalize()}:</strong> {value}</li>"""
                
                html += """
                    </ul>
                </div>"""
        
        html += """
            </div>
        </section>
        
        <section class="insights">
            <h3>Insights</h3>
            <div class="insights-grid">"""
        
        # Add platform insights
        if insights.get("platform_insights"):
            html += """
                <div class="insight-card">
                    <h4>Platform Performance</h4>
                    <ul>"""
            
            for insight in insights.get("platform_insights", []):
                html += f"""
                        <li>{insight}</li>"""
            
            html += """
                    </ul>
                </div>"""
        
        # Add KPI insights
        if insights.get("kpi_insights"):
            html += """
                <div class="insight-card">
                    <h4>KPI Performance</h4>
                    <ul>"""
            
            for insight in insights.get("kpi_insights", []):
                html += f"""
                        <li>{insight}</li>"""
            
            html += """
                    </ul>
                </div>"""
        
        # Add content insights
        if insights.get("content_insights"):
            html += """
                <div class="insight-card">
                    <h4>Content Performance</h4>
                    <ul>"""
            
            for insight in insights.get("content_insights", []):
                html += f"""
                        <li>{insight}</li>"""
            
            html += """
                    </ul>
                </div>"""
        
        html += """
            </div>
        </section>
        
        <section class="highlights">
            <h3>Account Manager Highlights</h3>
            <div class="highlights-content">"""
        
        # Add highlights
        if highlights_text:
            # Split into paragraphs
            paragraphs = highlights_text.split("\n\n")
            for paragraph in paragraphs:
                if paragraph.strip():
                    html += f"""
                <p>{paragraph.strip()}</p>"""
        else:
            html += """
                <p>No highlights available.</p>"""
        
        html += """
            </div>
        </section>
        
        <section class="screenshots">
            <h3>Performance Screenshots</h3>
            <div class="screenshot-gallery">"""
        
        # Add screenshots
        for screenshot_path in screenshot_paths:
            html += f"""
                <div class="screenshot">
                    <img src="{screenshot_path}" alt="Performance Screenshot">
                </div>"""
        
        html += """
            </div>
        </section>
        
        <section class="archive">
            <h3>Report Archive</h3>
            <div class="archive-links">
                <p>This is a placeholder for the report archive. In a real implementation, this would list links to previous reports.</p>
            </div>
        </section>
    </main>
    
    <footer>
        <div class="container">
            <p>Generated on {datetime.now().strftime('%Y-%m-%d')} by Client Report Automation</p>
        </div>
    </footer>
    
    <script src="assets/script.js"></script>
</body>
</html>"""
        
        return html
    
    def _generate_css(self):
        """
        Generate CSS for the report.
        
        Returns:
            str: Generated CSS
        """
        css = """/* Reset and base styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f8f9fa;
}

.container {
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 15px;
}

/* Header styles */
header {
    background-color: #2c3e50;
    color: white;
    padding: 2rem 0;
    margin-bottom: 2rem;
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

header h2 {
    font-size: 1.5rem;
    font-weight: normal;
    opacity: 0.8;
}

/* Section styles */
section {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 2rem;
    margin-bottom: 2rem;
}

section h3 {
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    color: #2c3e50;
    border-bottom: 2px solid #ecf0f1;
    padding-bottom: 0.5rem;
}

/* Key takeaway styles */
.key-takeaway {
    background-color: #3498db;
    color: white;
}

.key-takeaway h3 {
    color: white;
    border-bottom-color: rgba(255, 255, 255, 0.2);
}

.key-takeaway p {
    font-size: 1.2rem;
    line-height: 1.8;
}

/* Metrics styles */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
}

.metric-card {
    background-color: #f8f9fa;
    border-radius: 6px;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.metric-card h4 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    color: #2c3e50;
}

.metric-card ul {
    list-style: none;
}

.metric-card li {
    margin-bottom: 0.5rem;
}

/* Insights styles */
.insights-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
}

.insight-card {
    background-color: #f8f9fa;
    border-radius: 6px;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.insight-card h4 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    color: #2c3e50;
}

.insight-card ul {
    list-style: none;
}

.insight-card li {
    margin-bottom: 0.8rem;
    position: relative;
    padding-left: 1.5rem;
}

.insight-card li:before {
    content: "•";
    position: absolute;
    left: 0;
    color: #3498db;
    font-weight: bold;
}

/* Highlights styles */
.highlights-content p {
    margin-bottom: 1rem;
    line-height: 1.8;
}

/* Screenshot gallery styles */
.screenshot-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
}

.screenshot {
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.screenshot img {
    width: 100%;
    height: auto;
    display: block;
}

/* Archive styles */
.archive-links {
    background-color: #f8f9fa;
    border-radius: 6px;
    padding: 1.5rem;
}

/* Footer styles */
footer {
    background-color: #2c3e50;
    color: white;
    padding: 1.5rem 0;
    text-align: center;
    margin-top: 2rem;
}

footer p {
    opacity: 0.8;
}

/* Responsive styles */
@media (max-width: 768px) {
    header h1 {
        font-size: 2rem;
    }
    
    header h2 {
        font-size: 1.2rem;
    }
    
    section {
        padding: 1.5rem;
    }
    
    .metrics-grid,
    .insights-grid,
    .screenshot-gallery {
        grid-template-columns: 1fr;
    }
}"""
        
        return css
    
    def _generate_js(self):
        """
        Generate JavaScript for the report.
        
        Returns:
            str: Generated JavaScript
        """
        js = """// Add interactivity to the report
document.addEventListener('DOMContentLoaded', function() {
    // Add lightbox functionality to screenshots
    const screenshots = document.querySelectorAll('.screenshot img');
    
    screenshots.forEach(function(screenshot) {
        screenshot.addEventListener('click', function() {
            // Create lightbox
            const lightbox = document.createElement('div');
            lightbox.className = 'lightbox';
            lightbox.style.position = 'fixed';
            lightbox.style.top = '0';
            lightbox.style.left = '0';
            lightbox.style.width = '100%';
            lightbox.style.height = '100%';
            lightbox.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
            lightbox.style.display = 'flex';
            lightbox.style.alignItems = 'center';
            lightbox.style.justifyContent = 'center';
            lightbox.style.zIndex = '1000';
            
            // Create image
            const img = document.createElement('img');
            img.src = this.src;
            img.style.maxWidth = '90%';
            img.style.maxHeight = '90%';
            img.style.border = '2px solid white';
            
            // Add close functionality
            lightbox.addEventListener('click', function() {
                document.body.removeChild(lightbox);
            });
            
            // Add to DOM
            lightbox.appendChild(img);
            document.body.appendChild(lightbox);
        });
    });
});"""
        
        return js

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 8:
        print("Usage: python report_generator.py [client_name] [month] [strategy_data.json] [metrics_data.json] [insights.json] [highlights.txt] [screenshots_dir] [output_dir]")
        sys.exit(1)
    
    client_name = sys.argv[1]
    month = sys.argv[2]
    strategy_path = sys.argv[3]
    metrics_path = sys.argv[4]
    insights_path = sys.argv[5]
    highlights_path = sys.argv[6]
    screenshots_dir = sys.argv[7]
    output_dir = sys.argv[8]
    
    # Load strategy data
    with open(strategy_path, "r") as f:
        strategy_data = json.load(f)
    
    # Load metrics data
    with open(metrics_path, "r") as f:
        metrics_data = json.load(f)
    
    # Load insights
    with open(insights_path, "r") as f:
        insights = json.load(f)
    
    # Load highlights text
    with open(highlights_path, "r") as f:
        highlights_text = f.read()
    
    # Get screenshots
    screenshots = [os.path.join(screenshots_dir, f) for f in os.listdir(screenshots_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    
    generator = ReportGenerator()
    report_url = generator.generate_report(client_name, month, strategy_data, metrics_data, insights, highlights_text, screenshots, output_dir)
    
    print(f"Report generated: {report_url}")
