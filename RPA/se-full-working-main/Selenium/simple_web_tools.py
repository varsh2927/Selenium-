#!/usr/bin/env python3
"""
Simple Web Tools - No Chrome Driver Required
This script provides web automation, scraping, and testing capabilities
without requiring Chrome driver, making it more reliable on Windows.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os
from datetime import datetime
from fake_useragent import UserAgent
import pandas as pd

class SimpleWebTools:
    """Simple web tools that don't require browser automation"""
    
    def __init__(self):
        """Initialize the web tools"""
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def get_page_content(self, url, delay=1):
        """Get page content with error handling"""
        try:
            print(f"Fetching: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Add delay to be respectful
            time.sleep(delay)
            
            print(f"✅ Successfully fetched {url} (Status: {response.status_code})")
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching {url}: {e}")
            return None
    
    def scrape_news_articles(self, url, max_articles=5):
        """Scrape news articles from a website"""
        print(f"Scraping news from: {url}")
        
        content = self.get_page_content(url)
        if not content:
            return []
        
        soup = BeautifulSoup(content, 'html.parser')
        articles = []
        
        # Common selectors for news articles
        selectors = [
            'article',
            '.article',
            '.news-item',
            '.post',
            'div[class*="article"]',
            'div[class*="news"]',
            '.entry',
            '.story'
        ]
        
        for selector in selectors:
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
                    href = link_elem.get('href')
                    if not href.startswith('http'):
                        href = url + href
                    article_data['link'] = href
                
                # Extract summary
                summary_elem = element.find(['p', 'div'], class_=lambda x: x and ('summary' in x.lower() or 'description' in x.lower()))
                if summary_elem:
                    article_data['summary'] = summary_elem.get_text(strip=True)
                
                if article_data:
                    articles.append(article_data)
                    print(f"Scraped article {i+1}: {article_data.get('title', 'No title')}")
                
            except Exception as e:
                print(f"Error scraping article {i+1}: {e}")
                continue
        
        return articles
    
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
    
    def test_website_connectivity(self, url):
        """Test if a website is accessible"""
        print(f"Testing connectivity to: {url}")
        
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=10)
            response_time = time.time() - start_time
            
            result = {
                'url': url,
                'status_code': response.status_code,
                'response_time': round(response_time, 2),
                'accessible': response.status_code == 200,
                'content_length': len(response.content)
            }
            
            print(f"✅ {url} - Status: {response.status_code}, Time: {response_time:.2f}s")
            return result
            
        except requests.exceptions.RequestException as e:
            result = {
                'url': url,
                'status_code': None,
                'response_time': None,
                'accessible': False,
                'error': str(e)
            }
            print(f"❌ {url} - Error: {e}")
            return result
    
    def save_data(self, data, filename=None, format='json'):
        """Save data to file"""
        if not data:
            print("No data to save")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_{timestamp}"
        
        try:
            if format.lower() == 'json':
                with open(f"{filename}.json", 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"✅ Data saved to {filename}.json")
            
            elif format.lower() == 'csv':
                df = pd.DataFrame(data)
                df.to_csv(f"{filename}.csv", index=False, encoding='utf-8')
                print(f"✅ Data saved to {filename}.csv")
            
            elif format.lower() == 'excel':
                df = pd.DataFrame(data)
                df.to_excel(f"{filename}.xlsx", index=False)
                print(f"✅ Data saved to {filename}.xlsx")
            
            else:
                print(f"❌ Unsupported format: {format}")
                
        except Exception as e:
            print(f"❌ Error saving data: {e}")

def demo_web_scraping():
    """Demonstrate web scraping capabilities"""
    print("=" * 60)
    print("Web Scraping Demo")
    print("=" * 60)
    
    tools = SimpleWebTools()
    
    # Test 1: Scrape news from Python.org
    print("\n--- Test 1: Scraping Python.org News ---")
    news_url = "https://www.python.org/blogs/"
    articles = tools.scrape_news_articles(news_url, max_articles=3)
    if articles:
        tools.save_data(articles, "python_news", "json")
    
    # Test 2: Test website connectivity
    print("\n--- Test 2: Website Connectivity Test ---")
    test_urls = [
        "https://www.google.com",
        "https://www.python.org",
        "https://httpbin.org/get",
        "https://www.github.com"
    ]
    
    connectivity_results = []
    for url in test_urls:
        result = tools.test_website_connectivity(url)
        connectivity_results.append(result)
    
    tools.save_data(connectivity_results, "connectivity_test", "json")
    
    # Test 3: Scrape table data (example with Wikipedia)
    print("\n--- Test 3: Table Data Scraping ---")
    table_url = "https://en.wikipedia.org/wiki/List_of_countries_by_population"
    table_data = tools.scrape_table_data(table_url, 'table.wikitable')
    if table_data:
        tools.save_data(table_data[:10], "population_data", "csv")  # Save first 10 rows
    
    print("\n✅ Web scraping demo completed!")

def demo_web_testing():
    """Demonstrate web testing capabilities"""
    print("=" * 60)
    print("Web Testing Demo")
    print("=" * 60)
    
    tools = SimpleWebTools()
    
    # Test multiple websites
    test_urls = [
        "https://www.google.com",
        "https://www.python.org",
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404",
        "https://httpbin.org/delay/2"
    ]
    
    print("Testing website connectivity and performance...")
    results = []
    
    for url in test_urls:
        result = tools.test_website_connectivity(url)
        results.append(result)
    
    # Generate test report
    total_tests = len(results)
    passed_tests = len([r for r in results if r['accessible']])
    failed_tests = total_tests - passed_tests
    
    print(f"\n📊 Test Results Summary:")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success rate: {(passed_tests/total_tests*100):.1f}%")
    
    # Save detailed results
    tools.save_data(results, "web_test_results", "json")
    
    print("\n✅ Web testing demo completed!")

def main():
    """Main function"""
    print("🚀 Simple Web Tools Demo")
    print("This script demonstrates web scraping and testing without browser automation.")
    
    try:
        # Run web scraping demo
        demo_web_scraping()
        
        # Run web testing demo
        demo_web_testing()
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("This might be due to network connectivity issues.")
    
    print("\n" + "=" * 60)
    print("All demos completed!")
    print("=" * 60)

if __name__ == "__main__":
    main() 