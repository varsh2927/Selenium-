#!/usr/bin/env python3
"""
Selenium Script Launcher
Interactive menu to run web automation, scraping, bot creation, and testing scripts.
"""

import os
import sys
import subprocess
from typing import List, Dict

class ScriptLauncher:
    """Interactive launcher for Selenium scripts"""
    
    def __init__(self):
        self.scripts = {
            "1": {
                "name": "Simple Web Tools (Recommended)",
                "file": "simple_web_tools.py",
                "description": "Web scraping and testing without Chrome driver - most reliable"
            },
            "2": {
                "name": "Test Setup",
                "file": "test_setup.py",
                "description": "Test your Selenium setup and identify issues"
            },
            "3": {
                "name": "Windows Web Automation",
                "file": "web_automation_windows.py",
                "description": "Windows-specific web automation with better error handling"
            },
            "4": {
                "name": "Web Automation (Full)",
                "file": "web_automation.py",
                "description": "Full web automation with Chrome driver (may have issues on Windows)"
            },
            "5": {
                "name": "Web Scraping (Full)",
                "file": "web_scraping.py",
                "description": "Advanced web scraping with Selenium (may have issues on Windows)"
            },
            "6": {
                "name": "Bot Creation",
                "file": "bot_creation.py",
                "description": "Create various types of bots for automation and interaction"
            },
            "7": {
                "name": "Web Testing",
                "file": "web_testing.py",
                "description": "Comprehensive web testing with automated reporting"
            },
            "8": {
                "name": "Install Dependencies",
                "file": None,
                "description": "Install required packages from requirements.txt"
            },
            "9": {
                "name": "Exit",
                "file": None,
                "description": "Exit the launcher"
            }
        }
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*60)
        print("🚀 Selenium Python Web Automation Suite")
        print("="*60)
        print("Choose a script to run:\n")
        
        for key, script in self.scripts.items():
            print(f"{key}. {script['name']}")
            print(f"   {script['description']}")
            print()
    
    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed"""
        required_packages = [
            "selenium",
            "webdriver_manager",
            "bs4",  # beautifulsoup4 imports as bs4
            "requests",
            "pandas"
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                if package == "bs4":
                    __import__("bs4")  # beautifulsoup4
                else:
                    __import__(package.replace("-", "_"))
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Missing packages: {', '.join(missing_packages)}")
            print("Please run option 5 to install dependencies first.")
            return False
        
        print("✅ All required packages are installed!")
        return True
    
    def install_dependencies(self):
        """Install dependencies from requirements.txt"""
        print("📦 Installing dependencies...")
        
        try:
            if os.path.exists("requirements.txt"):
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
                print("✅ Dependencies installed successfully!")
            else:
                print("❌ requirements.txt not found!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing dependencies: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    def run_script(self, script_file: str):
        """Run a Python script"""
        if not os.path.exists(script_file):
            print(f"❌ Script file '{script_file}' not found!")
            return
        
        print(f"🚀 Running {script_file}...")
        print("-" * 40)
        
        try:
            # Run the script
            result = subprocess.run([sys.executable, script_file], 
                                  capture_output=False, 
                                  text=True)
            
            if result.returncode == 0:
                print(f"\n✅ {script_file} completed successfully!")
            else:
                print(f"\n❌ {script_file} failed with return code {result.returncode}")
                
        except KeyboardInterrupt:
            print(f"\n⏹️  {script_file} interrupted by user")
        except Exception as e:
            print(f"\n❌ Error running {script_file}: {e}")
    
    def show_script_info(self, script_key: str):
        """Show detailed information about a script"""
        script = self.scripts.get(script_key)
        if not script:
            print("❌ Invalid script selection!")
            return
        
        print(f"\n📋 {script['name']} Information")
        print("-" * 40)
        print(f"Description: {script['description']}")
        
        if script['file']:
            if os.path.exists(script['file']):
                file_size = os.path.getsize(script['file'])
                print(f"File: {script['file']} ({file_size} bytes)")
                
                # Show first few lines of the script
                try:
                    with open(script['file'], 'r', encoding='utf-8') as f:
                        lines = f.readlines()[:10]
                        print("\nFirst 10 lines:")
                        for i, line in enumerate(lines, 1):
                            print(f"{i:2d}: {line.rstrip()}")
                        if len(lines) == 10:
                            print("   ...")
                except Exception as e:
                    print(f"Error reading file: {e}")
            else:
                print(f"File: {script['file']} (not found)")
    
    def run(self):
        """Main launcher loop"""
        print("Welcome to the Selenium Python Web Automation Suite!")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("Enter your choice (1-9): ").strip()
                
                if choice not in self.scripts:
                    print("❌ Invalid choice! Please enter a number between 1-9.")
                    continue
                
                script = self.scripts[choice]
                
                if choice == "9":  # Exit
                    print("👋 Goodbye!")
                    break
                
                elif choice == "8":  # Install dependencies
                    self.install_dependencies()
                
                else:  # Run a script
                    if not self.check_dependencies():
                        continue
                    
                    # Show script info first
                    self.show_script_info(choice)
                    
                    # Ask for confirmation
                    confirm = input(f"\nDo you want to run {script['name']}? (y/n): ").strip().lower()
                    if confirm in ['y', 'yes']:
                        self.run_script(script['file'])
                    
                    # Ask if user wants to continue
                    continue_choice = input("\nPress Enter to continue or 'q' to quit: ").strip().lower()
                    if continue_choice == 'q':
                        print("👋 Goodbye!")
                        break
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")

def main():
    """Main function"""
    launcher = ScriptLauncher()
    launcher.run()

if __name__ == "__main__":
    main() 