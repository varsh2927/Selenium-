"""
Bot Creation Script using Selenium
This script demonstrates various types of bots including:
- Social media automation bots
- Chat bots
- Task automation bots
- Data collection bots
- Notification bots
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import random
import requests
from datetime import datetime
import os
import threading
from queue import Queue
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SocialMediaBot:
    """Bot for social media automation"""
    
    def __init__(self, headless=True):
        """Initialize the social media bot"""
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def login_twitter(self, username, password):
        """Login to Twitter (example - requires actual credentials)"""
        try:
            self.driver.get("https://twitter.com/login")
            time.sleep(3)
            
            # Enter username
            username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "text")))
            username_field.send_keys(username)
            username_field.send_keys(Keys.RETURN)
            time.sleep(2)
            
            # Enter password
            password_field = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)
            time.sleep(5)
            
            logger.info("Successfully logged into Twitter")
            return True
            
        except Exception as e:
            logger.error(f"Error logging into Twitter: {e}")
            return False
    
    def post_tweet(self, message):
        """Post a tweet"""
        try:
            # Find tweet compose box
            tweet_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')))
            tweet_box.send_keys(message)
            time.sleep(1)
            
            # Click tweet button
            tweet_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetButton"]')))
            tweet_button.click()
            time.sleep(3)
            
            logger.info(f"Successfully posted tweet: {message[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return False
    
    def like_tweets(self, hashtag, count=5):
        """Like tweets with specific hashtag"""
        try:
            search_url = f"https://twitter.com/search?q=%23{hashtag}&src=typed_query&f=live"
            self.driver.get(search_url)
            time.sleep(3)
            
            # Find like buttons
            like_buttons = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="like"]')
            
            for i, button in enumerate(like_buttons[:count]):
                try:
                    button.click()
                    time.sleep(random.uniform(1, 3))
                    logger.info(f"Liked tweet {i+1}")
                except:
                    continue
            
            return True
            
        except Exception as e:
            logger.error(f"Error liking tweets: {e}")
            return False
    
    def follow_users(self, usernames):
        """Follow users by username"""
        for username in usernames:
            try:
                self.driver.get(f"https://twitter.com/{username}")
                time.sleep(3)
                
                follow_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="follow"]')))
                follow_button.click()
                time.sleep(2)
                
                logger.info(f"Followed user: {username}")
                
            except Exception as e:
                logger.error(f"Error following {username}: {e}")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")

class ChatBot:
    """Simple chatbot with predefined responses"""
    
    def __init__(self):
        """Initialize the chatbot with responses"""
        self.responses = {
            "hello": ["Hi there!", "Hello!", "Hey! How can I help you?"],
            "how are you": ["I'm doing great, thanks!", "I'm fine, how about you?"],
            "bye": ["Goodbye!", "See you later!", "Take care!"],
            "help": ["I can help you with basic questions. Just ask!"],
            "weather": ["I'm sorry, I don't have access to weather data yet."],
            "time": [f"The current time is {datetime.now().strftime('%H:%M:%S')}"],
            "date": [f"Today is {datetime.now().strftime('%Y-%m-%d')}"]
        }
        
        self.default_responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "That's interesting! Tell me more.",
            "I'm still learning. Could you ask something else?",
            "I don't have information about that yet."
        ]
    
    def get_response(self, user_input):
        """Get a response based on user input"""
        user_input = user_input.lower().strip()
        
        for key, responses in self.responses.items():
            if key in user_input:
                return random.choice(responses)
        
        return random.choice(self.default_responses)
    
    def start_chat(self):
        """Start an interactive chat session"""
        print("ChatBot: Hi! I'm your chatbot. Type 'bye' to exit.")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['bye', 'exit', 'quit']:
                print("ChatBot: Goodbye!")
                break
            
            response = self.get_response(user_input)
            print(f"ChatBot: {response}")

class TaskAutomationBot:
    """Bot for automating repetitive tasks"""
    
    def __init__(self, headless=True):
        """Initialize the task automation bot"""
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def fill_forms_automatically(self, form_data_list):
        """Automatically fill multiple forms"""
        for i, form_data in enumerate(form_data_list):
            try:
                logger.info(f"Filling form {i+1}/{len(form_data_list)}")
                
                # Navigate to form page
                self.driver.get(form_data.get('url', 'https://httpbin.org/forms/post'))
                time.sleep(2)
                
                # Fill form fields
                for field_name, value in form_data.get('fields', {}).items():
                    try:
                        field = self.wait.until(EC.presence_of_element_located((By.NAME, field_name)))
                        field.clear()
                        field.send_keys(value)
                        logger.info(f"Filled {field_name}: {value}")
                    except:
                        logger.warning(f"Could not fill field: {field_name}")
                
                # Submit form if submit button exists
                try:
                    submit_button = self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"], button[type="submit"]')
                    submit_button.click()
                    logger.info("Form submitted")
                except:
                    logger.info("No submit button found")
                
                time.sleep(3)
                
            except Exception as e:
                logger.error(f"Error filling form {i+1}: {e}")
    
    def download_files(self, file_urls, download_dir="downloads"):
        """Download files from URLs"""
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        for url in file_urls:
            try:
                filename = url.split('/')[-1]
                filepath = os.path.join(download_dir, filename)
                
                response = requests.get(url, stream=True)
                response.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                logger.info(f"Downloaded: {filename}")
                
            except Exception as e:
                logger.error(f"Error downloading {url}: {e}")
    
    def monitor_website_changes(self, url, check_interval=60):
        """Monitor website for changes"""
        logger.info(f"Starting to monitor: {url}")
        
        try:
            self.driver.get(url)
            initial_content = self.driver.page_source
            
            while True:
                time.sleep(check_interval)
                
                self.driver.refresh()
                current_content = self.driver.page_source
                
                if current_content != initial_content:
                    logger.info("Website content has changed!")
                    # You could add notification logic here
                    break
                    
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error monitoring website: {e}")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")

class NotificationBot:
    """Bot for sending notifications"""
    
    def __init__(self):
        """Initialize the notification bot"""
        self.notification_queue = Queue()
        
    def add_notification(self, message, priority="normal"):
        """Add a notification to the queue"""
        notification = {
            "message": message,
            "priority": priority,
            "timestamp": datetime.now()
        }
        self.notification_queue.put(notification)
        logger.info(f"Notification added: {message}")
    
    def send_notification(self, notification):
        """Send a notification (placeholder for actual implementation)"""
        print(f"[{notification['priority'].upper()}] {notification['message']}")
        logger.info(f"Notification sent: {notification['message']}")
    
    def start_notification_service(self):
        """Start the notification service"""
        logger.info("Starting notification service...")
        
        while True:
            try:
                if not self.notification_queue.empty():
                    notification = self.notification_queue.get()
                    self.send_notification(notification)
                else:
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                logger.info("Notification service stopped")
                break
            except Exception as e:
                logger.error(f"Error in notification service: {e}")

def main():
    """Main function demonstrating different types of bots"""
    
    print("=== Bot Creation Examples ===\n")
    
    # Example 1: ChatBot
    print("1. ChatBot Example")
    print("-" * 20)
    chatbot = ChatBot()
    # Uncomment to start interactive chat
    # chatbot.start_chat()
    
    # Example 2: Task Automation Bot
    print("\n2. Task Automation Bot Example")
    print("-" * 30)
    task_bot = TaskAutomationBot(headless=True)
    
    try:
        # Example form data
        form_data_list = [
            {
                "url": "https://httpbin.org/forms/post",
                "fields": {
                    "custname": "John Doe",
                    "custtel": "123-456-7890",
                    "custemail": "john@example.com",
                    "size": "large",
                    "topping": "bacon",
                    "delivery": "20:00",
                    "comments": "Automated form submission"
                }
            }
        ]
        
        task_bot.fill_forms_automatically(form_data_list)
        
        # Download example files
        file_urls = [
            "https://httpbin.org/robots.txt",
            "https://httpbin.org/json"
        ]
        task_bot.download_files(file_urls)
        
    except Exception as e:
        logger.error(f"Error in task automation: {e}")
    finally:
        task_bot.close()
    
    # Example 3: Notification Bot
    print("\n3. Notification Bot Example")
    print("-" * 30)
    notification_bot = NotificationBot()
    
    # Add some notifications
    notification_bot.add_notification("Task completed successfully", "high")
    notification_bot.add_notification("System check passed", "normal")
    notification_bot.add_notification("New data available", "low")
    
    # Start notification service in a separate thread
    notification_thread = threading.Thread(target=notification_bot.start_notification_service, daemon=True)
    notification_thread.start()
    
    # Let it run for a few seconds
    time.sleep(5)
    
    print("\n=== Bot Examples Completed ===")

if __name__ == "__main__":
    main() 