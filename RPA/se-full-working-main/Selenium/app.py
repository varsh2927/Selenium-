from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import sys
import traceback
from datetime import datetime
import threading
import time
from werkzeug.utils import secure_filename

# Import your existing Selenium modules
try:
    from web_automation import WebAutomation
    from web_testing import FunctionalTestSuite, UITestSuite, PerformanceTestSuite, run_all_tests
    from web_scraping import WebScraper
except ImportError as e:
    print(f"Warning: Could not import some modules: {e}")

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Global variables for managing automation state
automation_instances = {}
test_results = []
is_running = False

# Configuration
UPLOAD_FOLDER = 'uploads'
SCREENSHOT_FOLDER = 'screenshots'
RESULTS_FOLDER = 'results'

# Create necessary directories
for folder in [UPLOAD_FOLDER, SCREENSHOT_FOLDER, RESULTS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SCREENSHOT_FOLDER'] = SCREENSHOT_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER

class AutomationManager:
    def __init__(self):
        self.instances = {}
        self.results = []
        self.is_running = False
    
    def create_instance(self, instance_id, headless=False):
        """Create a new automation instance"""
        try:
            automation = WebAutomation(headless=headless)
            self.instances[instance_id] = automation
            return {"success": True, "message": f"Automation instance {instance_id} created successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def close_instance(self, instance_id):
        """Close an automation instance"""
        if instance_id in self.instances:
            try:
                self.instances[instance_id].close()
                del self.instances[instance_id]
                return {"success": True, "message": f"Instance {instance_id} closed successfully"}
            except Exception as e:
                return {"success": False, "error": str(e)}
        return {"success": False, "error": "Instance not found"}
    
    def get_instance(self, instance_id):
        """Get an automation instance"""
        return self.instances.get(instance_id)

# Initialize automation manager
automation_manager = AutomationManager()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS)"""
    return send_file(filename)

@app.route('/api/status')
def get_status():
    """Get current automation status"""
    return jsonify({
        "is_running": automation_manager.is_running,
        "active_instances": len(automation_manager.instances),
        "total_results": len(automation_manager.results),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/automation/create', methods=['POST'])
def create_automation():
    """Create a new automation instance"""
    try:
        data = request.get_json()
        instance_id = data.get('instance_id', f"instance_{int(time.time())}")
        headless = data.get('headless', False)
        
        result = automation_manager.create_instance(instance_id, headless)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/automation/close/<instance_id>', methods=['DELETE'])
def close_automation(instance_id):
    """Close an automation instance"""
    result = automation_manager.close_instance(instance_id)
    return jsonify(result)

@app.route('/api/navigate', methods=['POST'])
def navigate_to_website():
    """Navigate to a website"""
    try:
        data = request.get_json()
        instance_id = data.get('instance_id')
        url = data.get('url')
        
        if not instance_id or not url:
            return jsonify({"success": False, "error": "Missing instance_id or url"}), 400
        
        automation = automation_manager.get_instance(instance_id)
        if not automation:
            return jsonify({"success": False, "error": "Automation instance not found"}), 404
        
        success = automation.navigate_to_website(url)
        if success:
            automation_manager.results.append({
                "type": "navigation",
                "url": url,
                "status": "success",
                "timestamp": datetime.now().isoformat()
            })
            return jsonify({"success": True, "message": f"Successfully navigated to {url}"})
        else:
            return jsonify({"success": False, "error": f"Failed to navigate to {url}"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/search', methods=['POST'])
def perform_search():
    """Perform a search on a search engine"""
    try:
        data = request.get_json()
        instance_id = data.get('instance_id')
        search_engine = data.get('search_engine', 'google')
        query = data.get('query')
        
        if not instance_id or not query:
            return jsonify({"success": False, "error": "Missing instance_id or query"}), 400
        
        automation = automation_manager.get_instance(instance_id)
        if not automation:
            return jsonify({"success": False, "error": "Automation instance not found"}), 404
        
        # Navigate to search engine
        search_urls = {
            'google': 'https://www.google.com',
            'bing': 'https://www.bing.com',
            'duckduckgo': 'https://duckduckgo.com'
        }
        
        url = search_urls.get(search_engine, 'https://www.google.com')
        automation.navigate_to_website(url)
        
        # Perform search (this would need to be implemented based on your existing code)
        # For now, we'll simulate the search
        time.sleep(2)  # Simulate search time
        
        automation_manager.results.append({
            "type": "search",
            "engine": search_engine,
            "query": query,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        })
        
        return jsonify({"success": True, "message": f"Search completed on {search_engine}"})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/form/fill', methods=['POST'])
def fill_form():
    """Fill out a form with provided data"""
    try:
        data = request.get_json()
        instance_id = data.get('instance_id')
        form_url = data.get('form_url')
        form_data = data.get('form_data')
        
        if not instance_id or not form_url or not form_data:
            return jsonify({"success": False, "error": "Missing required parameters"}), 400
        
        automation = automation_manager.get_instance(instance_id)
        if not automation:
            return jsonify({"success": False, "error": "Automation instance not found"}), 404
        
        # Navigate to form
        automation.navigate_to_website(form_url)
        
        # Fill form using your existing method
        success = automation.fill_form(form_data)
        
        if success:
            automation_manager.results.append({
                "type": "form_fill",
                "url": form_url,
                "data": form_data,
                "status": "success",
                "timestamp": datetime.now().isoformat()
            })
            return jsonify({"success": True, "message": "Form filled successfully"})
        else:
            return jsonify({"success": False, "error": "Failed to fill form"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/extract', methods=['POST'])
def extract_data():
    """Extract data from a webpage"""
    try:
        data = request.get_json()
        instance_id = data.get('instance_id')
        selectors = data.get('selectors')
        
        if not instance_id or not selectors:
            return jsonify({"success": False, "error": "Missing instance_id or selectors"}), 400
        
        automation = automation_manager.get_instance(instance_id)
        if not automation:
            return jsonify({"success": False, "error": "Automation instance not found"}), 404
        
        # Extract data using your existing method
        extracted_data = automation.extract_data(selectors)
        
        automation_manager.results.append({
            "type": "data_extraction",
            "selectors": selectors,
            "data": extracted_data,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        })
        
        return jsonify({
            "success": True,
            "data": extracted_data,
            "message": "Data extracted successfully"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/screenshot', methods=['POST'])
def take_screenshot():
    """Take a screenshot of the current page"""
    try:
        data = request.get_json()
        instance_id = data.get('instance_id')
        filename = data.get('filename')
        
        if not instance_id:
            return jsonify({"success": False, "error": "Missing instance_id"}), 400
        
        automation = automation_manager.get_instance(instance_id)
        if not automation:
            return jsonify({"success": False, "error": "Automation instance not found"}), 404
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        filepath = os.path.join(app.config['SCREENSHOT_FOLDER'], filename)
        screenshot_path = automation.take_screenshot(filepath)
        
        if screenshot_path:
            automation_manager.results.append({
                "type": "screenshot",
                "filename": filename,
                "path": screenshot_path,
                "status": "success",
                "timestamp": datetime.now().isoformat()
            })
            
            return jsonify({
                "success": True,
                "filename": filename,
                "path": screenshot_path,
                "message": "Screenshot taken successfully"
            })
        else:
            return jsonify({"success": False, "error": "Failed to take screenshot"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/tests/run', methods=['POST'])
def run_tests():
    """Run a test suite"""
    try:
        data = request.get_json()
        test_suite = data.get('test_suite', 'basic')
        
        automation_manager.is_running = True
        
        # Run tests in a separate thread to avoid blocking
        def run_test_suite():
            try:
                if test_suite == 'basic':
                    # Run functional tests
                    test_suite_instance = FunctionalTestSuite(headless=True)
                    test_suite_instance.setup_driver()
                    test_suite_instance.test_google_search()
                    test_suite_instance.test_form_submission()
                    test_suite_instance.test_navigation()
                    test_suite_instance.teardown_driver()
                    
                    results = []
                    for result in test_suite_instance.test_results:
                        results.append({
                            "type": "test",
                            "name": result.test_name,
                            "status": "success" if result.status == "PASS" else "error",
                            "duration": result.duration,
                            "error": result.error_message,
                            "timestamp": result.timestamp.isoformat()
                        })
                    
                elif test_suite == 'advanced':
                    # Run UI and performance tests
                    ui_suite = UITestSuite(headless=True)
                    ui_suite.setup_driver()
                    ui_suite.test_responsive_design()
                    ui_suite.test_element_visibility()
                    ui_suite.test_page_load_time()
                    ui_suite.teardown_driver()
                    
                    perf_suite = PerformanceTestSuite(headless=True)
                    perf_suite.setup_driver()
                    perf_suite.test_api_response_time()
                    perf_suite.teardown_driver()
                    
                    results = []
                    for suite in [ui_suite, perf_suite]:
                        for result in suite.test_results:
                            results.append({
                                "type": "test",
                                "name": result.test_name,
                                "status": "success" if result.status == "PASS" else "error",
                                "duration": result.duration,
                                "error": result.error_message,
                                "timestamp": result.timestamp.isoformat()
                            })
                else:
                    # Run all tests
                    results = run_all_tests()
                
                automation_manager.results.extend(results)
                automation_manager.is_running = False
                
            except Exception as e:
                automation_manager.results.append({
                    "type": "test_suite",
                    "suite": test_suite,
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
                automation_manager.is_running = False
        
        thread = threading.Thread(target=run_test_suite)
        thread.start()
        
        return jsonify({
            "success": True,
            "message": f"Started {test_suite} test suite",
            "test_suite": test_suite
        })
        
    except Exception as e:
        automation_manager.is_running = False
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/tests/stop', methods=['POST'])
def stop_tests():
    """Stop running tests"""
    automation_manager.is_running = False
    return jsonify({
        "success": True,
        "message": "Tests stopped"
    })

@app.route('/api/results')
def get_results():
    """Get all test results"""
    return jsonify({
        "results": automation_manager.results,
        "total": len(automation_manager.results)
    })

@app.route('/api/results/export/<format>')
def export_results(format):
    """Export results in specified format"""
    try:
        if format not in ['json', 'csv', 'html']:
            return jsonify({"success": False, "error": "Unsupported format"}), 400
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results_{timestamp}.{format}"
        filepath = os.path.join(app.config['RESULTS_FOLDER'], filename)
        
        if format == 'json':
            with open(filepath, 'w') as f:
                json.dump(automation_manager.results, f, indent=2)
        elif format == 'csv':
            import csv
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Type', 'Status', 'Timestamp', 'Details'])
                for result in automation_manager.results:
                    writer.writerow([
                        result.get('type', ''),
                        result.get('status', ''),
                        result.get('timestamp', ''),
                        json.dumps(result)
                    ])
        elif format == 'html':
            html_content = generate_html_report(automation_manager.results)
            with open(filepath, 'w') as f:
                f.write(html_content)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def generate_html_report(results):
    """Generate HTML report from results"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Selenium Test Results</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .success {{ color: green; }}
            .error {{ color: red; }}
        </style>
    </head>
    <body>
        <h1>Selenium Test Results</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Total Results: {len(results)}</p>
        <table>
            <tr>
                <th>Type</th>
                <th>Status</th>
                <th>Timestamp</th>
                <th>Details</th>
            </tr>
    """
    
    for result in results:
        html += f"""
            <tr>
                <td>{result.get('type', '')}</td>
                <td class="{result.get('status', '')}">{result.get('status', '')}</td>
                <td>{result.get('timestamp', '')}</td>
                <td>{json.dumps(result, indent=2)}</td>
            </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    
    return html

@app.route('/api/stats')
def get_stats():
    """Get automation statistics"""
    total_results = len(automation_manager.results)
    successful_results = len([r for r in automation_manager.results if r.get('status') == 'success'])
    success_rate = (successful_results / total_results * 100) if total_results > 0 else 0
    
    return jsonify({
        "total_results": total_results,
        "successful_results": successful_results,
        "success_rate": round(success_rate, 2),
        "active_instances": len(automation_manager.instances),
        "is_running": automation_manager.is_running
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🚀 Starting Selenium Automation Hub API Server...")
    print("📱 Frontend will be available at: http://localhost:5000")
    print("🔧 API endpoints available at: http://localhost:5000/api/")
    app.run(debug=True, host='0.0.0.0', port=5000) 