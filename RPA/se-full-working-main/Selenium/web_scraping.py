"""
Web Scraping Script using Selenium and BeautifulSoup
This script demonstrates various web scraping techniques including:
- Data extraction from websites
- Handling dynamic content
- Saving data to different formats
- Respectful scraping with delays
- Error handling and retry mechanisms
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json
import time
import random
from datetime import datetime
import os
from fake_useragent import UserAgent

class WebScraper:
    def __init__(self, use_selenium=False, headless=True):
        """Initialize the web scraper"""
        self.use_selenium = use_selenium
        self.ua = UserAgent()
        
        if use_selenium:
            self.chrome_options = Options()
            if headless:
                self.chrome_options.add_argument("--headless")
            self.chrome_options.add_argument("--no-sandbox")
            self.chrome_options.add_argument("--disable-dev-shm-usage")
            self.chrome_options.add_argument("--disable-gpu")
            self.chrome_options.add_argument("--window-size=1920,1080")
            self.chrome_options.add_argument(f"--user-agent={self.ua.random}")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
    
    def get_page_content(self, url, delay=1):
        """Get page content using requests or Selenium"""
        try:
            if self.use_selenium:
                self.driver.get(url)
                time.sleep(delay)
                return self.driver.page_source
            else:
                headers = {
                    'User-Agent': self.ua.random,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                }
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                return response.text
        except Exception as e:
            print(f"Error getting content from {url}: {e}")
            return None
    
    def scrape_news_articles(self, url, max_articles=10):
        """Scrape news articles from a news website"""
        print(f"Scraping news articles from: {url}")
        
        content = self.get_page_content(url)
        if not content:
            return []
        
        soup = BeautifulSoup(content, 'html.parser')
        articles = []
        
        # Example selectors for news articles (adjust based on target website)
        article_selectors = [
            'article',
            '.article',
            '.news-item',
            '.post',
            'div[class*="article"]',
            'div[class*="news"]'
        ]
        
        for selector in article_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"Found {len(elements)} articles using selector: {selector}")
                break
        
        for i, element in enumerate(elements[:max_articles]):
            try:
                article_data = {}
                
                # Extract title
                title_elem = element.find(['h1', 'h2', 'h3', 'h4']) or element.find(class_=lambda x: x and 'title' in x.lower())
                if title_elem:
                    article_data['title'] = title_elem.get_text(strip=True)
                
                # Extract link
                link_elem = element.find('a')
                if link_elem and link_elem.get('href'):
                    article_data['link'] = link_elem.get('href')
                    if not article_data['link'].startswith('http'):
                        article_data['link'] = url + article_data['link']
                
                # Extract summary/description
                summary_elem = element.find(['p', 'div'], class_=lambda x: x and ('summary' in x.lower() or 'description' in x.lower()))
                if summary_elem:
                    article_data['summary'] = summary_elem.get_text(strip=True)
                
                # Extract date
                date_elem = element.find(['time', 'span'], class_=lambda x: x and ('date' in x.lower() or 'time' in x.lower()))
                if date_elem:
                    article_data['date'] = date_elem.get_text(strip=True)
                
                if article_data:
                    articles.append(article_data)
                    print(f"Scraped article {i+1}: {article_data.get('title', 'No title')}")
                
            except Exception as e:
                print(f"Error scraping article {i+1}: {e}")
                continue
        
        return articles
    
    def scrape_ecommerce_products(self, url, max_products=20):
        """Scrape product information from e-commerce websites"""
        print(f"Scraping products from: {url}")
        
        content = self.get_page_content(url)
        if not content:
            return []
        
        soup = BeautifulSoup(content, 'html.parser')
        products = []
        
        # Common product selectors
        product_selectors = [
            '.product',
            '.item',
            '[data-product]',
            '.card',
            '.product-item'
        ]
        
        for selector in product_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"Found {len(elements)} products using selector: {selector}")
                break
        
        for i, element in enumerate(elements[:max_products]):
            try:
                product_data = {}
                
                # Extract product name
                name_elem = element.find(['h1', 'h2', 'h3', 'h4']) or element.find(class_=lambda x: x and 'name' in x.lower())
                if name_elem:
                    product_data['name'] = name_elem.get_text(strip=True)
                
                # Extract price
                price_elem = element.find(class_=lambda x: x and 'price' in x.lower())
                if price_elem:
                    product_data['price'] = price_elem.get_text(strip=True)
                
                # Extract image
                img_elem = element.find('img')
                if img_elem and img_elem.get('src'):
                    product_data['image'] = img_elem.get('src')
                
                # Extract rating
                rating_elem = element.find(class_=lambda x: x and 'rating' in x.lower())
                if rating_elem:
                    product_data['rating'] = rating_elem.get_text(strip=True)
                
                if product_data:
                    products.append(product_data)
                    print(f"Scraped product {i+1}: {product_data.get('name', 'No name')}")
                
            except Exception as e:
                print(f"Error scraping product {i+1}: {e}")
                continue
        
        return products
    
    def scrape_table_data(self, url, table_selector='table'):
        """Scrape data from HTML tables"""
        print(f"Scraping table data from: {url}")
        
        content = self.get_page_content(url)
        if not content:
            return []
        
        soup = BeautifulSoup(content, 'html.parser')
        tables = soup.select(table_selector)
        
        all_data = []
        
        for table in tables:
            try:
                # Extract headers
                headers = []
                header_row = table.find('thead')
                if header_row:
                    headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
                else:
                    # Try to get headers from first row
                    first_row = table.find('tr')
                    if first_row:
                        headers = [th.get_text(strip=True) for th in first_row.find_all(['th', 'td'])]
                
                # Extract data rows
                rows = table.find_all('tr')[1:] if header_row else table.find_all('tr')
                
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if cells:
                        row_data = {}
                        for i, cell in enumerate(cells):
                            if i < len(headers):
                                row_data[headers[i]] = cell.get_text(strip=True)
                            else:
                                row_data[f'column_{i}'] = cell.get_text(strip=True)
                        all_data.append(row_data)
                
            except Exception as e:
                print(f"Error scraping table: {e}")
                continue
        
        return all_data
    
    def save_data(self, data, filename=None, format='json'):
        """Save scraped data to file"""
        if not data:
            print("No data to save")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraped_data_{timestamp}"
        
        try:
            if format.lower() == 'json':
                with open(f"{filename}.json", 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"Data saved to {filename}.json")
            
            elif format.lower() == 'csv':
                df = pd.DataFrame(data)
                df.to_csv(f"{filename}.csv", index=False, encoding='utf-8')
                print(f"Data saved to {filename}.csv")
            
            elif format.lower() == 'excel':
                df = pd.DataFrame(data)
                df.to_excel(f"{filename}.xlsx", index=False)
                print(f"Data saved to {filename}.xlsx")
            
            else:
                print(f"Unsupported format: {format}")
                
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def close(self):
        """Close the browser if using Selenium"""
        if self.use_selenium and hasattr(self, 'driver'):
            self.driver.quit()
            print("Browser closed")

def main():
    """Main function demonstrating web scraping"""
    
    # Example 1: Scraping with requests and BeautifulSoup
    print("=== Web Scraping with Requests + BeautifulSoup ===")
    scraper = WebScraper(use_selenium=False)
    
    try:
        # Scrape Python.org news
        news_url = "https://www.python.org/blogs/"
        news_articles = scraper.scrape_news_articles(news_url, max_articles=5)
        scraper.save_data(news_articles, "python_news", "json")
        
        # Scrape table data from a sample website
        table_url = "https://en.wikipedia.org/wiki/List_of_countries_by_population"
        table_data = scraper.scrape_table_data(table_url, 'table.wikitable')
        scraper.save_data(table_data[:10], "population_data", "csv")
        
    except Exception as e:
        print(f"Error in requests scraping: {e}")
    
    # Example 2: Scraping with Selenium for dynamic content
    print("\n=== Web Scraping with Selenium ===")
    selenium_scraper = WebScraper(use_selenium=True, headless=True)
    
    try:
        # Scrape a dynamic website (example: GitHub trending)
        github_url = "https://github.com/trending"
        trending_repos = selenium_scraper.scrape_news_articles(github_url, max_articles=10)
        selenium_scraper.save_data(trending_repos, "github_trending", "excel")
        
    except Exception as e:
        print(f"Error in Selenium scraping: {e}")
    
    finally:
        selenium_scraper.close()

if __name__ == "__main__":
    main() 