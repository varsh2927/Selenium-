# Selenium Python Web Automation Suite

This repository contains comprehensive Python scripts for web automation, web scraping, bot creation, and web testing using Selenium WebDriver.

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Scripts Overview](#scripts-overview)
- [Usage Examples](#usage-examples)
- [Requirements](#requirements)
- [Troubleshooting](#troubleshooting)

## 🚀 Features

### 1. Web Automation (`web_automation.py`)
- **Form filling and submission**
- **Navigation and clicking**
- **Data extraction**
- **Screenshot capture**
- **Dynamic content handling**
- **Google search automation**
- **Website interaction**

### 2. Web Scraping (`web_scraping.py`)
- **Data extraction from websites**
- **Dynamic content handling**
- **Multiple output formats (JSON, CSV, Excel)**
- **Respectful scraping with delays**
- **Error handling and retry mechanisms**
- **News article scraping**
- **E-commerce product scraping**
- **Table data extraction**

### 3. Bot Creation (`bot_creation.py`)
- **Social media automation bots**
- **Interactive chatbots**
- **Task automation bots**
- **Data collection bots**
- **Notification bots**
- **Form automation**
- **File downloading**
- **Website monitoring**

### 4. Web Testing (`web_testing.py`)
- **Functional testing**
- **UI/UX testing**
- **Performance testing**
- **Cross-browser testing**
- **Automated test reporting**
- **Screenshot capture on failures**
- **HTML and JSON test reports**

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- Chrome browser (for Selenium)
- Git

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Selenium
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python -c "import selenium; print('Selenium installed successfully')"
   ```

## 🚀 Quick Start

### Easy Launcher (Recommended)
The easiest way to run any script is using the script launcher:

```bash
python run_scripts.py
```

This will show you a menu where you can select which script to run:
- Web Automation
- Web Scraping  
- Bot Creation
- Web Testing
- Simple Web Tools (no Chrome driver needed)

## 📁 Scripts Overview

### 0. Script Launcher (`run_scripts.py`)

**Purpose:** Easy menu-driven interface to run any script.

**Usage:**
```bash
python run_scripts.py
```

### 1. Web Automation Script (`web_automation.py`)

**Purpose:** Automate web interactions like form filling, navigation, and data extraction.

**Key Features:**
- Google search automation
- Form filling and submission
- Website navigation
- Screenshot capture
- Data extraction

**Usage:**
```bash
python web_automation.py
```

**Example Output:**
```
=== Google Search Automation ===
Successfully navigated to: https://www.google.com
Element found: q
Clicked element: Accept all
Extracted first_result: Python Selenium automation - Google Search
Screenshot saved as: google_search_results.png
```

### 2. Web Scraping Script (`web_scraping.py`)

**Purpose:** Extract data from websites using both requests/BeautifulSoup and Selenium.

**Key Features:**
- News article scraping
- E-commerce product scraping
- Table data extraction
- Multiple output formats
- Respectful scraping practices

**Usage:**
```bash
python web_scraping.py
```

**Example Output:**
```
=== Web Scraping with Requests + BeautifulSoup ===
Scraping news articles from: https://www.python.org/blogs/
Found 5 articles using selector: article
Scraped article 1: Python 3.12.0 is now available
Data saved to python_news.json
```

### 3. Bot Creation Script (`bot_creation.py`)

**Purpose:** Create various types of bots for automation and interaction.

**Key Features:**
- Social media bots (Twitter automation)
- Interactive chatbots
- Task automation bots
- Notification systems
- Form automation

**Usage:**
```bash
python bot_creation.py
```

**Example Output:**
```
=== Bot Creation Examples ===

1. ChatBot Example
--------------------

2. Task Automation Bot Example
------------------------------
2024-01-15 10:30:15 - INFO - Driver initialized for chrome
2024-01-15 10:30:17 - INFO - Filling form 1/1
2024-01-15 10:30:18 - INFO - Filled custname: John Doe
2024-01-15 10:30:19 - INFO - Form submitted
```

### 4. Web Testing Script (`web_testing.py`)

**Purpose:** Comprehensive web testing with automated reporting.

**Key Features:**
- Functional testing
- UI/UX testing
- Performance testing
- Cross-browser support
- Automated reporting

**Usage:**
```bash
python web_testing.py
```

**Example Output:**
```
Running Functional Tests...
Running UI Tests...
Running Performance Tests...
All tests completed. Check test_report.html and test_report.json for results.
```

## 🔧 Usage Examples

### Basic Web Automation
```python
from web_automation import WebAutomation

# Initialize automation
automation = WebAutomation(headless=False)

# Navigate to website
automation.navigate_to_website("https://www.google.com")

# Fill form
form_data = {
    "username": "testuser",
    "password": "testpass"
}
automation.fill_form(form_data)

# Take screenshot
automation.take_screenshot("test_screenshot.png")

# Close browser
automation.close()
```

### Web Scraping
```python
from web_scraping import WebScraper

# Initialize scraper
scraper = WebScraper(use_selenium=False)

# Scrape news articles
articles = scraper.scrape_news_articles("https://example.com/news", max_articles=10)

# Save data
scraper.save_data(articles, "news_data", "json")
```

### Bot Creation
```python
from bot_creation import ChatBot, TaskAutomationBot

# Create chatbot
chatbot = ChatBot()
response = chatbot.get_response("Hello")

# Create task automation bot
task_bot = TaskAutomationBot()
task_bot.fill_forms_automatically(form_data_list)
```

### Web Testing
```python
from web_testing import FunctionalTestSuite, TestReporter

# Run functional tests
tests = FunctionalTestSuite()
tests.setup_driver()
tests.test_google_search()
tests.teardown_driver()

# Generate report
reporter = TestReporter()
reporter.add_results(tests.test_results)
reporter.generate_html_report()
```

## 📋 Requirements

### Core Dependencies
- `selenium==4.15.2` - Web automation framework
- `webdriver-manager==4.0.1` - Automatic driver management
- `beautifulsoup4==4.12.2` - HTML parsing
- `requests==2.31.0` - HTTP library
- `pytest==7.4.3` - Testing framework

### Additional Dependencies
- `fake-useragent==1.4.0` - Random user agents
- `pandas==2.1.3` - Data manipulation
- `openpyxl==3.1.2` - Excel file support
- `lxml==4.9.3` - XML/HTML processing

## 🛠️ Troubleshooting

### Quick Diagnostic Tools

If you encounter any issues, use these diagnostic tools:

1. **Run Diagnostics:**
   ```bash
   python diagnostic.py
   ```
   This will check your environment and identify issues.

2. **Auto-Fix Common Issues:**
   ```bash
   python fix_environment.py
   ```
   This will attempt to fix common setup problems.

3. **Test Your Setup:**
   ```bash
   python test_setup.py
   ```
   This will verify everything is working.

### Common Windows Issues

The most common error on Windows is: `[WinError 193] %1 is not a valid Win32 application`

**Quick Solutions:**

1. **Use Simple Web Tools (Recommended):**
   ```bash
   python simple_web_tools.py
   ```
   This works without Chrome driver issues.

2. **Use the Script Launcher:**
   ```bash
   python run_scripts.py
   ```
   Select "Simple Web Tools" from the menu.

3. **Use Windows-Specific Script:**
   ```bash
   python web_automation_windows.py
   ```

### Detailed Troubleshooting

For comprehensive troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Common Issues

1. **ChromeDriver not found:**
   ```bash
   # The webdriver-manager will automatically download the correct version
   pip install webdriver-manager
   ```

2. **Permission errors on Windows:**
   ```bash
   # Run PowerShell as Administrator
   Set-ExecutionPolicy RemoteSigned
   ```

3. **Headless mode issues:**
   ```python
   # Try running without headless mode first
   automation = WebAutomation(headless=False)
   ```

4. **Element not found errors:**
   - Check if the website structure has changed
   - Increase wait time: `WebDriverWait(driver, 20)`
   - Use different selectors (ID, class, XPath)

### Performance Tips

1. **Use headless mode for faster execution:**
   ```python
   automation = WebAutomation(headless=True)
   ```

2. **Implement delays for respectful scraping:**
   ```python
   import time
   time.sleep(2)  # Wait 2 seconds between requests
   ```

3. **Use explicit waits instead of time.sleep():**
   ```python
   from selenium.webdriver.support.ui import WebDriverWait
   from selenium.webdriver.support import expected_conditions as EC
   
   element = WebDriverWait(driver, 10).until(
       EC.presence_of_element_located((By.ID, "my-element"))
   )
   ```

## 📊 Output Files

The scripts generate various output files:

- **Screenshots:** `screenshots/` directory
- **Test Reports:** `test_report.html`, `test_report.json`
- **Scraped Data:** `*.json`, `*.csv`, `*.xlsx` files
- **Logs:** Console output with timestamps

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

- Use these scripts responsibly and in accordance with website terms of service
- Respect robots.txt files and implement appropriate delays
- Some websites may have anti-bot measures
- Always test on non-production environments first

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue in the repository

---

**Happy Automating! 🚀**