AutomationFramework/
│── config/                  
│   ├── __init__.py
│   ├── webdriver_setup.py    # WebDriver initialization
│   ├── settings.py           # General settings
│
│── pages/                    
│   ├── __init__.py
│   ├── login_page.py         # Login Page Object Model
│   ├── dashboard_page.py     # Dashboard Page Object Model
│
│── tests/                    
│   ├── __init__.py
│   ├── test_login.py         # Login test cases
│
│── utils/                    
│   ├── __init__.py
│   ├── helpers.py            # Utility functions
│
│── reports/                  # Stores test reports
│── .github/workflows/        # GitHub Actions (CI/CD)
│── requirements.txt          # Project dependencies
│── conftest.py               # Pytest configuration & WebDriver fixture
│── pytest.ini                # Pytest default configurations
│── README.md                 # Project documentation
