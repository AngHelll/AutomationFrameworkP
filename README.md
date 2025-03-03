# 🚀 Automation Framework

## 📌 Overview
This is a **Selenium-based automation framework** built with **Python & Pytest** to test the **Example Domain page** (`https://example.com/`). The framework ensures stable, parallel, and efficient UI testing, supporting multiple browsers and CI/CD integration with GitHub Actions.

---

## 📂 Project Structure
```
AutomationFramework/
│── config/                  # WebDriver and settings configuration
│   ├── webdriver_setup.py   # WebDriver initialization
│   ├── settings.py          # General settings (timeouts, URLs, etc.)
│
│── pages/                   # Page Object Model (POM) files
│   ├── example_page.py      # Interactions with Example Domain
│
│── tests/                   # Automated test cases
│   ├── test_example_page.py # Test cases for Example Domain
│
│── reports/                 # Test reports and logs
│── utils/                   # Helper functions (screenshots, logs, etc.)
│── .github/workflows/       # CI/CD GitHub Actions configuration
│── requirements.txt         # Python dependencies
│── conftest.py              # Pytest fixtures (WebDriver setup)
│── pytest.ini               # Pytest configuration
│── .gitignore               # Ignored files and directories
│── README.md                # Documentation
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
### **Modify `config/webdriver_setup.py` to change browser settings**
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
✅ **`test_example_page.py`** verifies:
- **Page title is correct**
- **Main header is visible**
- **Paragraph text is present**
- **More information link exists**

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
- **GitHub:** [your-username](https://github.com/your-username)
- **Email:** your-email@example.com

