# 🐳 Docker Guide for Automation Framework

**Complete guide on using Docker with the test automation framework.**

---

## What is Docker?

Docker packages your framework and all dependencies into a **container** - a lightweight, isolated environment that runs identically everywhere.

**Think of it as:** A shipping container for your tests that works the same on any machine.

---

## When to Use Docker ✅

### **1. Continuous Integration/Continuous Deployment (CI/CD)**

**Use Docker when:**
- Running tests in GitHub Actions, GitLab CI, Jenkins, etc.
- Need consistent test environment across pipeline stages
- Multiple projects share the same CI/CD infrastructure

**Why:**
- ✅ No "works on my machine" problems
- ✅ Clean environment for every test run
- ✅ Fast parallel execution
- ✅ No dependency conflicts

**Example: GitHub Actions**
```yaml
# .github/workflows/tests.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: docker build -t automation-framework .
      - run: docker run automation-framework pytest -v
```

---

### **2. Team Environments**

**Use Docker when:**
- Team members use different operating systems (Windows, Mac, Linux)
- Onboarding new team members
- Want to avoid "it works for me but not for you" issues

**Why:**
- ✅ Everyone tests on identical environment
- ✅ New developers productive in minutes
- ✅ No manual setup of Python, browsers, drivers
- ✅ Version consistency guaranteed

---

### **3. Production-Like Testing**

**Use Docker when:**
- Production application runs in containers
- Testing against specific OS versions
- Need to match production environment exactly

**Why:**
- ✅ Test in environment identical to production
- ✅ Catch environment-specific bugs early
- ✅ Validate deployment configurations

---

### **4. Parallel Execution at Scale**

**Use Docker when:**
- Running hundreds/thousands of tests
- Need horizontal scaling
- Using orchestration tools (Kubernetes, Docker Swarm)

**Why:**
- ✅ Spin up multiple containers instantly
- ✅ Each container isolated (no interference)
- ✅ Auto-scaling based on load
- ✅ Efficient resource usage

---

### **5. Cloud Testing Services**

**Use Docker when:**
- Using cloud platforms (AWS, Azure, GCP)
- Running tests on-demand
- Need auto-scaling test execution

**Why:**
- ✅ Cloud platforms have native Docker support
- ✅ Pay only for test execution time
- ✅ Scale from 1 to 1000 containers instantly

---

## When NOT to Use Docker ❌

### **1. Local Development**

**Don't use Docker when:**
- Developing and debugging tests locally
- Need to see browser visually (non-headless)
- Iterating quickly on test code

**Why:**
- ❌ Slower iteration (rebuild container each time)
- ❌ Can't see browser UI easily
- ❌ Debugging is more complex
- ❌ Extra complexity without benefit

**Instead:** Run tests directly on your machine
```bash
pytest -v                    # Direct execution
HEADLESS=false pytest       # See browser
```

---

### **2. Visual Testing**

**Don't use Docker when:**
- Need to watch tests execute visually
- Debugging complex UI interactions
- Recording test execution videos

**Why:**
- ❌ Containers run headless by default
- ❌ No display output
- ❌ Harder to capture/view videos

**Instead:** Use local execution or CI tools with video recording

---

### **3. Simple Projects**

**Don't use Docker when:**
- Solo developer, single machine
- Small test suite (< 50 tests)
- No deployment/CI/CD pipeline

**Why:**
- ❌ Overkill for simple scenarios
- ❌ Added complexity without benefits
- ❌ Learning curve not justified

---

## How to Use Docker with This Framework

### **Setup (One Time)**

#### **1. Install Docker**
```bash
# Windows/Mac: Download Docker Desktop
# https://www.docker.com/products/docker-desktop

# Linux:
sudo apt-get install docker.io
```

#### **2. Verify Installation**
```bash
docker --version
# Should show: Docker version 20.x.x or higher
```

---

### **Basic Usage**

#### **1. Build Docker Image**
```bash
# From framework root directory
docker build -t automation-framework .

# Output:
# [+] Building 45.2s (10/10) FINISHED
# Successfully tagged automation-framework:latest
```

**What this does:**
- Creates image from `Dockerfile`
- Installs Python 3.9
- Installs all dependencies from `requirements.txt`
- Copies framework code
- Tags as `automation-framework`

#### **2. Run Tests in Container**
```bash
# Run all tests
docker run automation-framework

# Run specific tests
docker run automation-framework pytest tests/test_login.py

# Run with verbose output
docker run automation-framework pytest -v

# Run BDD tests
docker run automation-framework behave
```

#### **3. Run with Custom Configuration**
```bash
# Pass environment variables
docker run -e BROWSER=firefox -e HEADLESS=true automation-framework

# Mount local .env file
docker run -v $(pwd)/.env:/app/.env automation-framework

# Run with different test markers
docker run automation-framework pytest -m smoke
```

---

### **Advanced Usage**

#### **1. Keep Logs and Reports**
```bash
# Mount reports directory to see results locally
docker run -v $(pwd)/reports:/app/reports automation-framework

# After run, check:
# - reports/test_report.html
# - logs/test_execution_*.log
```

#### **2. Parallel Execution**
```bash
# Run 4 containers in parallel
docker run automation-framework pytest -n 4

# Or use docker-compose for multiple services
```

#### **3. Interactive Mode (Debugging)**
```bash
# Enter container shell
docker run -it automation-framework /bin/bash

# Inside container:
root@container:/app# pytest -v
root@container:/app# python -m pytest --collect-only
root@container:/app# exit
```

#### **4. Different Browser Versions**
```dockerfile
# Create custom Dockerfile for specific browser
FROM python:3.9

# Install specific Chrome version
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get install -y google-chrome-stable=98.0.4758.102-1

# Continue with framework setup
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["pytest"]
```

---

## CI/CD Integration Examples

### **GitHub Actions**

```yaml
# .github/workflows/tests.yml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t automation-framework .
      
      - name: Run smoke tests
        run: docker run automation-framework pytest -m smoke
      
      - name: Run all tests
        run: docker run automation-framework pytest -v
      
      - name: Upload reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-reports
          path: reports/
```

---

### **GitLab CI**

```yaml
# .gitlab-ci.yml
image: docker:latest

services:
  - docker:dind

stages:
  - test

test_job:
  stage: test
  script:
    - docker build -t automation-framework .
    - docker run automation-framework pytest -v
  artifacts:
    paths:
      - reports/
    when: always
```

---

### **Jenkins**

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t automation-framework .'
            }
        }
        
        stage('Test') {
            steps {
                sh 'docker run automation-framework pytest -v'
            }
        }
    }
    
    post {
        always {
            publishHTML([
                reportDir: 'reports',
                reportFiles: 'test_report.html',
                reportName: 'Test Report'
            ])
        }
    }
}
```

---

## Docker Compose (Multi-Container)

### **When to Use docker-compose**

Use when you need:
- Multiple services (e.g., tests + database + API)
- Complex networking between containers
- Consistent multi-container setup

### **Example: docker-compose.yml**

```yaml
version: '3.8'

services:
  tests:
    build: .
    environment:
      - BROWSER=chrome
      - HEADLESS=true
      - BASE_URL=http://web:8000
    volumes:
      - ./reports:/app/reports
    depends_on:
      - web
  
  web:
    image: nginx:alpine
    ports:
      - "8000:80"
    volumes:
      - ./test-app:/usr/share/nginx/html
```

```bash
# Run all services
docker-compose up

# Run tests only
docker-compose run tests pytest -v

# Clean up
docker-compose down
```

---

## Performance Optimization

### **1. Use Build Cache**

```dockerfile
# Dockerfile optimized for caching
FROM python:3.9

WORKDIR /app

# Copy only requirements first (cached if unchanged)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy code later (changes frequently)
COPY . .

CMD ["pytest"]
```

**Benefit:** Rebuilds only take seconds instead of minutes

---

### **2. Multi-Stage Builds**

```dockerfile
# Stage 1: Build dependencies
FROM python:3.9 as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["pytest"]
```

**Benefit:** Smaller final image (faster pull/push)

---

### **3. Layer Optimization**

```dockerfile
# Group RUN commands to reduce layers
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/cache/apt/* && \
    rm -rf /tmp/*
COPY . .
CMD ["pytest"]
```

**Benefit:** Smaller image size, faster builds

---

## Troubleshooting Docker Issues

### **Issue: Tests fail in Docker but pass locally**

**Cause:** Different environment (browser version, dependencies, timing)

**Solution:**
```bash
# 1. Check exact versions
docker run automation-framework pip freeze

# 2. Run interactively to debug
docker run -it automation-framework /bin/bash

# 3. Check logs
docker run -v $(pwd)/logs:/app/logs automation-framework
```

---

### **Issue: Container exits immediately**

**Cause:** Command fails or completes too fast

**Solution:**
```bash
# Check container logs
docker logs <container-id>

# Keep container alive
docker run -it automation-framework /bin/bash
```

---

### **Issue: Can't see screenshots**

**Cause:** Screenshots saved inside container

**Solution:**
```bash
# Mount screenshots directory
docker run -v $(pwd)/screenshots:/app/screenshots automation-framework
```

---

### **Issue: Slow build times**

**Cause:** Not using build cache

**Solution:**
```bash
# Use BuildKit (faster builds)
DOCKER_BUILDKIT=1 docker build -t automation-framework .

# Remove unused images
docker system prune -a
```

---

## Decision Matrix: Docker vs Local

| Scenario | Use Docker? | Reason |
|----------|-------------|---------|
| Local development | ❌ No | Slower iteration, harder debugging |
| CI/CD pipeline | ✅ Yes | Consistency, reproducibility |
| Team collaboration | ✅ Yes | Same environment for everyone |
| Visual debugging | ❌ No | Need to see browser |
| Production-like tests | ✅ Yes | Match prod environment |
| Quick smoke test | ❌ No | Overhead not worth it |
| Parallel scaling | ✅ Yes | Easy horizontal scaling |
| Solo project | ❌ Maybe | Only if deploying to containers |

---

## Best Practices Summary

### **DO:**
✅ Use Docker for CI/CD pipelines  
✅ Use Docker for team consistency  
✅ Use Docker for production-like testing  
✅ Version your Docker images (tags)  
✅ Keep Dockerfile simple and cached  
✅ Mount volumes for reports/logs  

### **DON'T:**
❌ Use Docker for local development (unless necessary)  
❌ Put sensitive data in Docker images  
❌ Create huge images (optimize layers)  
❌ Run without mounting results directories  
❌ Forget to clean up old containers/images  

---

## Quick Commands Reference

```bash
# Build
docker build -t automation-framework .

# Run
docker run automation-framework                    # All tests
docker run automation-framework pytest -v          # Verbose
docker run automation-framework behave            # BDD tests

# With environment
docker run -e HEADLESS=true automation-framework

# With volumes
docker run -v $(pwd)/reports:/app/reports automation-framework

# Interactive
docker run -it automation-framework /bin/bash

# Cleanup
docker system prune                                # Remove unused
docker rmi automation-framework                    # Remove image
```

---

## Conclusion

**Use Docker when:**
- 🔄 Running in CI/CD
- 👥 Working in teams
- 🚀 Deploying to production
- 📈 Scaling horizontally

**Skip Docker when:**
- 💻 Developing locally
- 🐛 Debugging visually
- 🏃 Quick iterations
- 👤 Solo, simple project

**The framework supports both approaches - choose based on your needs!** 🎯

---

**Ready to containerize your tests? Start with: `docker build -t automation-framework .`** 🐳

