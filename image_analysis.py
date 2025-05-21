#!/usr/bin/env python3
"""
Image Analysis Module for Client Report Automation

This module analyzes screenshots to extract performance metrics.
"""

import os
import logging
import json
import cv2
import numpy as np
import pytesseract
from PIL import Image

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("image_analysis.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ImageAnalyzer:
    """
    Analyzes images to extract performance metrics.
    """
    
    def analyze_image(self, image_path):
        """
        Analyze an image to extract performance metrics.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: Extracted metrics
        """
        logger.info(f"Analyzing image: {image_path}")
        
        try:
            # Open the image
            image = cv2.imread(image_path)
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
            
            # Extract text using pytesseract
            text = pytesseract.image_to_string(thresh)
            
            # Extract metrics from text
            metrics = self._extract_metrics(text)
            
            # Add image metadata
            metrics["image_path"] = image_path
            metrics["image_name"] = os.path.basename(image_path)
            
            return metrics
        
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return {
                "image_path": image_path,
                "image_name": os.path.basename(image_path),
                "error": str(e)
            }
    
    def _extract_metrics(self, text):
        """
        Extract metrics from text.
        
        Args:
            text (str): Text to extract metrics from
            
        Returns:
            dict: Extracted metrics
        """
        # This is a simplified implementation
        # In a real implementation, this would use more sophisticated techniques
        
        metrics = {
            "platform": self._detect_platform(text),
            "metrics": {}
        }
        
        # Look for common metrics
        metric_patterns = {
            "impressions": ["impressions", "views", "reach"],
            "engagement": ["engagement", "interactions", "likes", "comments", "shares"],
            "clicks": ["clicks", "link clicks", "website clicks"],
            "followers": ["followers", "new followers", "audience growth"],
            "conversion": ["conversion", "leads", "sign-ups", "purchases"]
        }
        
        for metric_name, patterns in metric_patterns.items():
            for pattern in patterns:
                if pattern.lower() in text.lower():
                    # Find the line containing the pattern
                    for line in text.split("\n"):
                        if pattern.lower() in line.lower():
                            # Extract the value
                            parts = line.split(":")
                            if len(parts) > 1:
                                value = parts[1].strip()
                                metrics["metrics"][metric_name] = value
                                break
                            
                            # Try extracting numeric value
                            words = line.split()
                            for i, word in enumerate(words):
                                if pattern.lower() in word.lower() and i < len(words) - 1:
                                    try:
                                        value = words[i + 1].strip()
                                        # Remove non-numeric characters
                                        value = ''.join(c for c in value if c.isdigit() or c == '.' or c == '%')
                                        metrics["metrics"][metric_name] = value
                                        break
                                    except:
                                        pass
        
        return metrics
    
    def _detect_platform(self, text):
        """
        Detect the platform from text.
        
        Args:
            text (str): Text to detect platform from
            
        Returns:
            str: Detected platform
        """
        platforms = {
            "facebook": ["facebook", "fb", "meta"],
            "instagram": ["instagram", "ig", "insta"],
            "twitter": ["twitter", "tweet", "x"],
            "linkedin": ["linkedin", "li", "linked in"],
            "tiktok": ["tiktok", "tt", "tik tok"],
            "youtube": ["youtube", "yt", "you tube"],
            "pinterest": ["pinterest", "pin"]
        }
        
        for platform, patterns in platforms.items():
            for pattern in patterns:
                if pattern.lower() in text.lower():
                    return platform
        
        return "unknown"

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python image_analysis.py [image_file]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    analyzer = ImageAnalyzer()
    metrics = analyzer.analyze_image(image_path)
    
    print(json.dumps(metrics, indent=2))
