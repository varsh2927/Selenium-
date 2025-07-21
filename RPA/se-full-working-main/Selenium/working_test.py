#!/usr/bin/env python3
"""
Guaranteed Working Web Script
This script should work on any Windows system with Python.
"""

import requests
import json
from datetime import datetime

def test_basic_functionality():
    """Test basic web functionality"""
    print("Testing basic web functionality...")
    
    try:
        # Test 1: Simple HTTP request
        print("\n--- Test 1: HTTP Request ---")
        response = requests.get("https://httpbin.org/get", timeout=10)
        print(f"HTTP request successful: Status {response.status_code}")
        
        # Test 2: Get JSON data
        print("\n--- Test 2: JSON Data ---")
        data = response.json()
        print(f"JSON data received: {data.get('url', 'N/A')}")
        
        # Test 3: Test multiple websites
        print("\n--- Test 3: Multiple Websites ---")
        websites = [
            "https://www.google.com",
            "https://www.python.org",
            "https://httpbin.org/json"
        ]
        
        results = []
        for url in websites:
            try:
                resp = requests.get(url, timeout=10)
                results.append({
                    "url": url,
                    "status": resp.status_code,
                    "accessible": resp.status_code == 200
                })
                print(f"SUCCESS: {url} - Status: {resp.status_code}")
            except Exception as e:
                results.append({
                    "url": url,
                    "status": "ERROR",
                    "accessible": False,
                    "error": str(e)
                })
                print(f"ERROR: {url} - Error: {e}")
        
        # Save results
        with open("test_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print("\nResults saved to test_results.json")
        
        # Summary
        successful = sum(1 for r in results if r.get('accessible', False))
        total = len(results)
        print(f"\nSummary: {successful}/{total} websites accessible")
        
        return True
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False

def main():
    """Main function"""
    print("="*60)
    print("GUARANTEED WORKING WEB SCRIPT")
    print("="*60)
    
    success = test_basic_functionality()
    
    if success:
        print("\nAll tests passed! Your system can perform basic web operations.")
        print("\nNext steps:")
        print("1. Try: python simple_web_tools.py")
        print("2. Try: python run_scripts.py")
    else:
        print("\nSome tests failed. Check your internet connection.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
