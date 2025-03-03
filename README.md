# 🚀 Automation Framework

## 📌 Overview
This is a **Selenium-based automation framework** built with **Python & Pytest** to test web applications. The framework ensures stable, parallel, and efficient UI testing, supporting multiple browsers and CI/CD integration with GitHub Actions.

---

## 📂 Project Structure
```
AutomationFramework/
│── .github/                 # CI/CD GitHub Actions configuration
│
│── config/                  # WebDriver and settings configuration
│   ├── browser_setup.py     # WebDriver initialization
│   ├── settings.py          # General settings (timeouts, URLs, etc.)
│
│── pages/                   # Page Object Model (POM) files
│   ├── dashboard_page.py    # Interactions with Dashboard
│   ├── github_cli_page.py   # Interactions with GitHub CLI page
│   ├── login_page.py        # Interactions with Login page
│
│── reports/                 # Test reports and logs
│   ├── test_report.html     # Latest HTML test report
│   ├── test_report_.html    # Backup report
│
│── tests/                   # Automated test cases
│   ├── reports/             # Test-specific reports
│   ├── test_github_cli.py   # Test cases for GitHub CLI page
│   ├── test_login.py        # Test cases for Login page
│
│── utils/                   # Helper functions (screenshots, logs, etc.)
│   ├── helpers.py           # Utility functions
│
│── .env                     # Environment variables (ignored)
│── .gitignore               # Ignored files and directories
│── conftest.py              # Pytest fixtures (WebDriver setup)
│── Dockerfile               # Docker configuration
│── pytest.ini               # Pytest configuration
│── README.md                # Documentation
│── requirements.txt         # Python dependencies
```

---

## 🛠️ Setup & Installation
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-username/AutomationFramework.git
cd AutomationFramework
```

### **2️⃣ Create a Virtual Environment**
```sh
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate    # Windows
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

---

## 🚀 Running Tests
### **Run All Tests**
```sh
pytest --browser=chrome -v
```

### **Run Tests in Parallel**
```sh
pytest -n auto
```

### **Generate an HTML Report**
```sh
pytest --html=reports/test_report.html --self-contained-html
```

---

## 🔧 Configuration
### **Modify `config/browser_setup.py` to change browser settings**
- Supports **Chrome, Firefox, and Edge**
- Enables **headless mode** for CI/CD execution

Example:
```python
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
```

---

## 🌍 CI/CD Integration (GitHub Actions)
This framework includes **GitHub Actions** to run tests automatically on every **push** or **pull request**.

### **Manually Trigger CI/CD**
1. Go to **GitHub → Actions Tab**
2. Select **CI - Run Automation Tests**
3. Click **Run Workflow**

---

## 📌 Test Cases Overview
✅ **`test_github_cli.py`** verifies:
- **GitHub CLI page loads correctly**
- **Main header is visible**
- **Download button is present**

✅ **`test_login.py`** verifies:
- **Login form elements are present**
- **Valid and invalid login cases**

---

## 💡 Useful Commands
### **Update Dependencies Automatically**
```sh
pip freeze > requirements.txt
```

### **Check Configured Git Aliases**
```sh
git config --global --list | grep alias
```

---

## 📜 License
This project is **open-source** under the **MIT License**.

---

## 📞 Contact
- **GitHub:** AngHelll (https://github.com/AngHell)
