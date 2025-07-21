# 🤖 Selenium Automation Hub

A modern web interface for managing and running Selenium web automation tasks. This project combines a beautiful frontend dashboard with a powerful Python backend API.

## ✨ Features

### 🎨 **Frontend Dashboard**
- **Modern UI/UX**: Beautiful gradient design with glassmorphism effects
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Real-time Updates**: Live statistics and test results
- **Interactive Elements**: Smooth animations and hover effects
- **Notification System**: Real-time feedback for all actions

### 🔧 **Backend API**
- **Flask REST API**: Full RESTful API for automation control
- **Selenium Integration**: Direct connection to your existing Selenium scripts
- **Instance Management**: Multiple automation instances support
- **File Management**: Screenshot capture and result export
- **Real-time Status**: Live monitoring of automation processes

### 🚀 **Automation Features**
- **Website Navigation**: Navigate to any URL with headless mode support
- **Search Automation**: Google, Bing, and DuckDuckGo search automation
- **Form Filling**: Automated form submission with JSON data
- **Data Extraction**: Extract data using CSS selectors
- **Screenshot Capture**: Take screenshots of web pages
- **Test Suites**: Run basic, advanced, and custom test suites

## 📋 Prerequisites

- Python 3.7 or higher
- Google Chrome browser
- Internet connection

## 🛠️ Installation

### 1. Clone or Download the Project
Make sure you have all the project files in your directory.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Quick Start
```bash
python start_server.py
```

This script will:
- ✅ Check and install missing dependencies
- ✅ Verify Chrome driver availability
- ✅ Create necessary directories
- ✅ Start the Flask server
- ✅ Open your browser automatically

## 🚀 Usage

### Starting the Application

1. **Run the startup script:**
   ```bash
   python start_server.py
   ```

2. **Or start manually:**
   ```bash
   python app.py
   ```

3. **Access the application:**
   - Frontend: http://localhost:5000
   - API: http://localhost:5000/api/

### Using the Dashboard

#### 📊 **Dashboard Section**
- View real-time statistics
- Use quick action buttons for common tasks
- Monitor automation status

#### 🤖 **Automation Tools**
1. **Website Navigation**
   - Enter target URL
   - Choose headless mode (optional)
   - Click "Navigate"

2. **Search Automation**
   - Select search engine (Google, Bing, DuckDuckGo)
   - Enter search query
   - Click "Search"

3. **Form Automation**
   - Enter form URL
   - Provide JSON form data
   - Click "Fill Form"

4. **Data Extraction**
   - Provide CSS selectors in JSON format
   - Click "Extract Data"

#### 🧪 **Testing Suite**
1. Select test suite type (Basic, Advanced, Custom)
2. Click "Run Test Suite"
3. Monitor real-time test progress
4. View results and generate reports

#### 📈 **Results & Analytics**
- View performance charts
- See recent test results
- Export data in JSON, CSV, or HTML format

## 🔌 API Endpoints

### Status & Management
- `GET /api/status` - Get current automation status
- `POST /api/automation/create` - Create new automation instance
- `DELETE /api/automation/close/<instance_id>` - Close automation instance

### Automation Actions
- `POST /api/navigate` - Navigate to website
- `POST /api/search` - Perform search
- `POST /api/form/fill` - Fill form
- `POST /api/extract` - Extract data
- `POST /api/screenshot` - Take screenshot

### Testing
- `POST /api/tests/run` - Run test suite
- `POST /api/tests/stop` - Stop running tests

### Results & Export
- `GET /api/results` - Get all test results
- `GET /api/results/export/<format>` - Export results (json/csv/html)
- `GET /api/stats` - Get automation statistics

## 📁 Project Structure

```
Selenium/
├── app.py                 # Flask API server
├── start_server.py        # Startup script
├── index.html            # Frontend HTML
├── styles.css            # Frontend CSS
├── script.js             # Frontend JavaScript
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── web_automation.py    # Your Selenium automation
├── web_testing.py       # Your test scripts
├── web_scraping.py      # Your scraping scripts
├── uploads/             # Upload directory
├── screenshots/         # Screenshot storage
└── results/             # Export results
```

## 🔧 Configuration

### Environment Variables
You can set these environment variables for customization:

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
export CHROME_HEADLESS=false
```

### API Configuration
The API base URL is configured in `script.js`:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

## 🐛 Troubleshooting

### Common Issues

1. **Chrome Driver Issues**
   ```bash
   # Reinstall Chrome driver
   pip install --upgrade webdriver-manager
   ```

2. **Port Already in Use**
   ```bash
   # Kill process on port 5000
   lsof -ti:5000 | xargs kill -9
   ```

3. **CORS Issues**
   - Make sure Flask-CORS is installed
   - Check browser console for CORS errors

4. **Module Import Errors**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

### Debug Mode
Run the server in debug mode for detailed error messages:
```bash
export FLASK_DEBUG=1
python app.py
```

## 🔒 Security Notes

- The server runs on `0.0.0.0` by default (accessible from any IP)
- For production use, consider:
  - Adding authentication
  - Using HTTPS
  - Restricting access to localhost only
  - Implementing rate limiting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section
2. Review the browser console for errors
3. Check the Flask server logs
4. Ensure all dependencies are installed correctly

## 🎯 Next Steps

- [ ] Add user authentication
- [ ] Implement database storage
- [ ] Add more automation features
- [ ] Create mobile app
- [ ] Add CI/CD pipeline

---

**Happy Automating! 🚀** 