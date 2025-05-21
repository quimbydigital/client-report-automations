#!/usr/bin/env python3
"""
Insight Generation Module for Client Report Automation

This module generates insights based on extracted data.
"""

import os
import logging
import json
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("insight_generation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class InsightGenerator:
    """
    Generates insights based on extracted data.
    """
    
    def generate_insights(self, strategy_data, metrics_data, highlights_text):
        """
        Generate insights based on extracted data.
        
        Args:
            strategy_data (dict): Strategy data extracted from PDF
            metrics_data (dict): Metrics data extracted from images
            highlights_text (str): Highlights text
            
        Returns:
            dict: Generated insights
        """
        logger.info("Generating insights")
        
        try:
            # Generate platform insights
            platform_insights = self._generate_platform_insights(metrics_data)
            
            # Generate KPI insights
            kpi_insights = self._generate_kpi_insights(strategy_data, metrics_data)
            
            # Generate content insights
            content_insights = self._generate_content_insights(strategy_data, metrics_data, highlights_text)
            
            # Generate key takeaway
            key_takeaway = self._generate_key_takeaway(platform_insights, kpi_insights, content_insights, highlights_text)
            
            # Return insights
            return {
                "platform_insights": platform_insights,
                "kpi_insights": kpi_insights,
                "content_insights": content_insights,
                "key_takeaway": key_takeaway
            }
        
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            return {
                "platform_insights": [],
                "kpi_insights": [],
                "content_insights": [],
                "key_takeaway": "Unable to generate insights due to an error."
            }
    
    def _generate_platform_insights(self, metrics_data):
        """
        Generate platform insights based on metrics data.
        
        Args:
            metrics_data (dict): Metrics data extracted from images
            
        Returns:
            list: Platform insights
        """
        insights = []
        
        # Group metrics by platform
        platforms = {}
        for image_name, data in metrics_data.items():
            platform = data.get("platform", "unknown")
            if platform not in platforms:
                platforms[platform] = []
            platforms[platform].append(data)
        
        # Generate insights for each platform
        for platform, data_list in platforms.items():
            if platform == "unknown":
                continue
            
            # Combine metrics from all images for this platform
            combined_metrics = {}
            for data in data_list:
                metrics = data.get("metrics", {})
                for metric_name, value in metrics.items():
                    if metric_name not in combined_metrics:
                        combined_metrics[metric_name] = []
                    combined_metrics[metric_name].append(value)
            
            # Generate insights based on combined metrics
            for metric_name, values in combined_metrics.items():
                if not values:
                    continue
                
                # Generate insight based on metric
                if metric_name == "impressions":
                    insights.append(f"{platform.capitalize()} content reached a significant audience with {values[0]} impressions.")
                elif metric_name == "engagement":
                    insights.append(f"{platform.capitalize()} engagement was strong with {values[0]} interactions.")
                elif metric_name == "clicks":
                    insights.append(f"{platform.capitalize()} drove {values[0]} clicks to the website.")
                elif metric_name == "followers":
                    insights.append(f"{platform.capitalize()} audience grew by {values[0]} new followers.")
                elif metric_name == "conversion":
                    insights.append(f"{platform.capitalize()} generated {values[0]} conversions.")
        
        return insights
    
    def _generate_kpi_insights(self, strategy_data, metrics_data):
        """
        Generate KPI insights based on strategy data and metrics data.
        
        Args:
            strategy_data (dict): Strategy data extracted from PDF
            metrics_data (dict): Metrics data extracted from images
            
        Returns:
            list: KPI insights
        """
        insights = []
        
        # Extract KPIs from strategy data
        kpis = strategy_data.get("kpis", [])
        
        # Extract all metrics
        all_metrics = {}
        for image_name, data in metrics_data.items():
            metrics = data.get("metrics", {})
            for metric_name, value in metrics.items():
                if metric_name not in all_metrics:
                    all_metrics[metric_name] = []
                all_metrics[metric_name].append(value)
        
        # Compare KPIs to metrics
        for kpi in kpis:
            kpi_name = kpi.get("name", "").lower()
            kpi_value = kpi.get("value", "")
            
            # Find matching metric
            for metric_name, values in all_metrics.items():
                if metric_name.lower() in kpi_name or kpi_name in metric_name.lower():
                    if not values:
                        continue
                    
                    # Compare metric value to KPI value
                    metric_value = values[0]
                    
                    # Try to convert to numbers for comparison
                    try:
                        kpi_num = float(''.join(c for c in kpi_value if c.isdigit() or c == '.'))
                        metric_num = float(''.join(c for c in metric_value if c.isdigit() or c == '.'))
                        
                        if metric_num >= kpi_num:
                            insights.append(f"Exceeded KPI for {kpi_name}: Target was {kpi_value}, achieved {metric_value}.")
                        else:
                            insights.append(f"Below KPI for {kpi_name}: Target was {kpi_value}, achieved {metric_value}.")
                    except:
                        insights.append(f"KPI for {kpi_name}: Target was {kpi_value}, achieved {metric_value}.")
        
        return insights
    
    def _generate_content_insights(self, strategy_data, metrics_data, highlights_text):
        """
        Generate content insights based on strategy data, metrics data, and highlights text.
        
        Args:
            strategy_data (dict): Strategy data extracted from PDF
            metrics_data (dict): Metrics data extracted from images
            highlights_text (str): Highlights text
            
        Returns:
            list: Content insights
        """
        insights = []
        
        # Extract content pillars from strategy data
        content_pillars = strategy_data.get("content_pillars", [])
        
        # Generate insights based on content pillars and highlights
        if content_pillars and highlights_text:
            # Check if any content pillars are mentioned in highlights
            for pillar in content_pillars:
                if pillar.lower() in highlights_text.lower():
                    insights.append(f"Content aligned with the '{pillar}' pillar performed well this month.")
        
        # Generate insights based on highlights text
        if highlights_text:
            # Extract key phrases from highlights
            phrases = [
                "performed well",
                "high engagement",
                "popular",
                "successful",
                "resonated",
                "positive feedback",
                "strong performance"
            ]
            
            for phrase in phrases:
                if phrase in highlights_text.lower():
                    # Find the sentence containing the phrase
                    sentences = highlights_text.split(".")
                    for sentence in sentences:
                        if phrase in sentence.lower():
                            insights.append(sentence.strip() + ".")
                            break
        
        return insights
    
    def _generate_key_takeaway(self, platform_insights, kpi_insights, content_insights, highlights_text):
        """
        Generate a key takeaway based on all insights.
        
        Args:
            platform_insights (list): Platform insights
            kpi_insights (list): KPI insights
            content_insights (list): Content insights
            highlights_text (str): Highlights text
            
        Returns:
            str: Key takeaway
        """
        # Combine all insights
        all_insights = platform_insights + kpi_insights + content_insights
        
        # If we have insights, generate a takeaway based on them
        if all_insights:
            # Count positive and negative insights
            positive_count = sum(1 for insight in all_insights if any(pos in insight.lower() for pos in ["exceeded", "strong", "significant", "grew", "performed well"]))
            negative_count = sum(1 for insight in all_insights if any(neg in insight.lower() for neg in ["below", "declined", "decreased", "underperformed"]))
            
            # Generate takeaway based on positive/negative ratio
            if positive_count > negative_count:
                return "Overall performance was strong this month, with multiple KPIs exceeding targets. Continue to focus on content that resonates with the audience."
            elif negative_count > positive_count:
                return "Performance was below targets in several areas this month. Consider adjusting the content strategy to better align with audience interests."
            else:
                return "Performance was mixed this month, with some areas exceeding targets and others falling short. Focus on replicating successful content strategies."
        
        # If we don't have insights but have highlights, generate a takeaway based on highlights
        elif highlights_text:
            return "Based on the account manager's highlights, focus on continuing to create content that resonates with the audience and drives engagement."
        
        # Default takeaway
        else:
            return "Insufficient data to generate a meaningful takeaway. Ensure all required data is provided for future reports."

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python insight_generation.py [strategy_data.json] [metrics_data.json] [highlights.txt]")
        sys.exit(1)
    
    strategy_path = sys.argv[1]
    metrics_path = sys.argv[2]
    highlights_path = sys.argv[3]
    
    # Load strategy data
    with open(strategy_path, "r") as f:
        strategy_data = json.load(f)
    
    # Load metrics data
    with open(metrics_path, "r") as f:
        metrics_data = json.load(f)
    
    # Load highlights text
    with open(highlights_path, "r") as f:
        highlights_text = f.read()
    
    generator = InsightGenerator()
    insights = generator.generate_insights(strategy_data, metrics_data, highlights_text)
    
    print(json.dumps(insights, indent=2))
