#!/usr/bin/env python3
"""
Selenium Automation Hub Server Startup Script
This script starts the Flask API server and provides setup instructions.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask',
        'flask-cors',
        'selenium',
        'webdriver-manager'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing missing packages...")
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run:")
            print(f"   pip install {' '.join(missing_packages)}")
            return False
    
    return True

def check_chrome_driver():
    """Check if Chrome driver is available"""
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        ChromeDriverManager().install()
        print("✅ Chrome driver is ready")
        return True
    except Exception as e:
        print(f"⚠️  Chrome driver issue: {e}")
        print("   Make sure Chrome browser is installed")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'screenshots', 'results']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directories created")

def start_server():
    """Start the Flask server"""
    print("\n🚀 Starting Selenium Automation Hub...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check Chrome driver
    check_chrome_driver()
    
    # Create directories
    create_directories()
    
    print("\n🌐 Starting Flask server...")
    print("📱 Frontend will be available at: http://localhost:5000")
    print("🔧 API endpoints available at: http://localhost:5000/api/")
    print("\n⏳ Opening browser in 3 seconds...")
    
    # Wait a moment then open browser
    time.sleep(3)
    try:
        webbrowser.open('http://localhost:5000')
    except:
        print("⚠️  Could not open browser automatically")
        print("   Please manually open: http://localhost:5000")
    
    print("\n🔄 Server is running... Press Ctrl+C to stop")
    print("=" * 50)
    
    # Start the Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🤖 Selenium Automation Hub")
    print("=" * 30)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ app.py not found in current directory")
        print("   Please run this script from the project root directory")
        return
    
    # Start the server
    start_server()

if __name__ == '__main__':
    main() 