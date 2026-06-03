# 🛡️ Anti-Bot Scraping Implementation 

<div align="center">

# 🤖 Anti-Bot Web Scraping & Detection Evasion

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-HTTP_Client-green?style=for-the-badge)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-Web_Parsing-orange?style=for-the-badge)
![Selenium](https://img.shields.io/badge/Selenium-Browser_Automation-43B02A?style=for-the-badge\&logo=selenium)
![Linux](https://img.shields.io/badge/Linux-Ubuntu_20.04+-FCC624?style=for-the-badge\&logo=linux\&logoColor=black)

### 🔄 User-Agent Rotation • CAPTCHA Detection • Retry Logic • Human-Like Browsing

</div>

---

# 📖 Overview

Modern websites use sophisticated anti-bot protection mechanisms to detect and block automated scraping tools.

This lab demonstrates how to build a resilient scraper that can:

* 🔄 Rotate User Agents
* 🤖 Detect CAPTCHA Challenges
* ⏳ Implement Human-Like Delays
* 🔁 Retry Failed Requests
* 🛡️ Mimic Legitimate Browser Behavior

---

# 🎯 Learning Objectives

By completing this lab, you will:

✅ Implement User-Agent Rotation

✅ Build Retry Mechanisms

✅ Detect CAPTCHA Challenges

✅ Simulate Human Browsing Patterns

✅ Apply Rate Limiting Strategies

✅ Create Resilient Web Scrapers

---

# 📋 Prerequisites

| Requirement | Description               |
| ----------- | ------------------------- |
| 🐍 Python   | Basic Python Programming  |
| 🌐 HTTP     | Requests & Responses      |
| 📄 HTML     | Basic DOM Structure       |
| 🎯 CSS      | CSS Selectors             |
| 🖥 Linux    | Command-Line Navigation   |
| 🔍 Scraping | Web Scraping Fundamentals |

---

# 🏗️ Architecture

```text
                 ┌─────────────────┐
                 │ Target Website  │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ User-Agent Pool │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Anti-Bot Logic  │
                 │ Retry + Delay   │
                 └────────┬────────┘
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
 ┌─────────────────┐           ┌─────────────────┐
 │ Normal Response │           │ CAPTCHA Page    │
 └─────────────────┘           └─────────────────┘
```

---

# 🛠️ Environment Setup

## 🔄 Step 1: Update System

```bash
sudo apt update

sudo apt install -y python3 python3-pip python3-venv
```

---

## 📁 Step 2: Create Project Directory

```bash
mkdir ~/anti-bot-scraper

cd ~/anti-bot-scraper
```

Create virtual environment:

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

## 📦 Step 3: Install Dependencies

```bash
pip install requests beautifulsoup4 fake-useragent selenium
```

---

## 🌐 Step 4: Install Chromium & Driver

```bash
sudo apt install -y chromium-browser chromium-chromedriver
```

---

# 🚀 Task 1: Implement User-Agent Rotation

---

# 🏗️ Step 1: Create Base Scraper

Create:

```bash
nano scraper.py
```

---

## 🐍 scraper.py

```python
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import random

class AntiDetectionScraper:

    def __init__(self):

        self.ua = UserAgent()

        self.session = requests.Session()

    def get_random_headers(self):

        headers = {

            'User-Agent': self.ua.random,

            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',

            'Accept-Language':
            'en-US,en;q=0.5',

            'Accept-Encoding':
            'gzip, deflate',

            'Connection':
            'keep-alive',

            'Upgrade-Insecure-Requests':
            '1'
        }

        return headers
```

---

# 🔄 Step 2: Implement User-Agent Rotation

Every request should use a different browser fingerprint.

```python
headers = {
    "User-Agent": self.ua.random
}
```

Benefits:

✅ Reduces Detection

✅ Mimics Multiple Browsers

✅ Avoids Fingerprinting

---

# 🔁 Step 3: Implement Retry Logic

Add:

```python
def fetch_with_retry(self, url, max_retries=3):

    for attempt in range(max_retries):

        try:

            response = self.session.get(
                url,
                headers=self.get_random_headers(),
                timeout=10
            )

            if response.status_code == 200:

                return response

        except requests.exceptions.RequestException:

            pass

        delay = 2 ** attempt + random.uniform(0, 1)

        time.sleep(delay)

    return None
```

---

# 📄 Step 4: Implement Page Scraping

```python
def scrape_page(self, url):

    response = self.fetch_with_retry(url)

    if not response:

        return {"error": "Failed"}

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    return {

        "title": soup.title.text
        if soup.title else "No Title",

        "paragraphs":
        [p.text for p in soup.find_all("p")]

    }
```

---

# 🧪 Step 5: Test User-Agent Rotation

Create:

```bash
nano test_rotation.py
```

```python
from scraper import AntiDetectionScraper

def test_user_agents():

    scraper = AntiDetectionScraper()

    for i in range(5):

        headers = scraper.get_random_headers()

        print(
            f"{i+1}: "
            f"{headers['User-Agent']}"
        )

if __name__ == "__main__":

    test_user_agents()
```

Run:

```bash
python test_rotation.py
```

Expected:

```text
5 Different User-Agent Strings
```

---

# 🚀 Task 2: Handle CAPTCHA Simulation

---

# 🖥️ Step 1: Create Mock CAPTCHA Server

Create:

```bash
nano mock_server.py
```

```python
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

import random

class CAPTCHAHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if random.random() < 0.3:

            self.send_response(403)

            self.end_headers()

            self.wfile.write(
                b"CAPTCHA detected"
            )

        else:

            self.send_response(200)

            self.end_headers()

            self.wfile.write(
                b"Welcome! Content here."
            )

    def log_message(self, format, *args):
        pass

def run_server(port=8080):

    server = HTTPServer(
        ("localhost", port),
        CAPTCHAHandler
    )

    print(
        f"Server running on {port}"
    )

    server.serve_forever()

if __name__ == "__main__":

    run_server()
```

---

# 🔍 Step 2: CAPTCHA Detection

Add to scraper:

```python
def detect_captcha(self, response):

    indicators = [

        "captcha",

        "challenge",

        "verify"

    ]

    if response.status_code == 403:

        return True

    text = response.text.lower()

    return any(
        word in text
        for word in indicators
    )
```

---

# 🛡️ Step 3: CAPTCHA Handling

```python
def handle_captcha(self, url):

    print(
        "CAPTCHA encountered..."
    )

    wait_time = random.randint(10, 15)

    time.sleep(wait_time)

    return self.fetch_with_retry(url)
```

---

# 🔄 Step 4: Integrate CAPTCHA Logic

Update scraper:

```python
def scrape_page(self, url):

    response = self.fetch_with_retry(url)

    if response is None:

        return {
            "error":
            "Failed to fetch"
        }

    if self.detect_captcha(response):

        response = self.handle_captcha(url)

    if response is None:

        return {
            "error":
            "CAPTCHA unresolved"
        }

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    return {
        "content":
        soup.get_text()
    }
```

---

# 🧪 Step 5: Integration Test

Create:

```bash
nano test_captcha.py
```

```python
from scraper import AntiDetectionScraper

import time

def test_captcha_handling():

    scraper = AntiDetectionScraper()

    url = "http://localhost:8080"

    success = 0

    failed = 0

    for i in range(10):

        result = scraper.scrape_page(url)

        if "error" in result:

            failed += 1

        else:

            success += 1

    print(f"Success: {success}")

    print(f"Failed: {failed}")

if __name__ == "__main__":

    print(
        "Start mock_server.py first"
    )

    time.sleep(2)

    test_captcha_handling()
```

---

# ▶️ Run Complete Test

### Terminal 1

```bash
python mock_server.py
```

### Terminal 2

```bash
python test_captcha.py
```

---

# ✅ Verification

---

## 🔄 Verify User-Agent Rotation

```bash
python -c "
from scraper import AntiDetectionScraper

scraper = AntiDetectionScraper()

agents = [
scraper.get_random_headers()['User-Agent']
for _ in range(5)
]

print('Unique:', len(set(agents)))
"
```

Expected:

```text
Unique: 3+
```

---

## 🤖 Verify CAPTCHA Detection

```bash
python -c "
from scraper import AntiDetectionScraper
import requests

scraper = AntiDetectionScraper()

response = requests.get(
'http://localhost:8080'
)

print(
scraper.detect_captcha(response)
)
"
```

Expected:

```text
True or False
```

---

# 🎯 Comprehensive Test

Create:

```bash
nano final_test.py
```

```python
from scraper import AntiDetectionScraper

import time

def comprehensive_test():

    scraper = AntiDetectionScraper()

    print(
        'Testing httpbin'
    )

    for i in range(3):

        response = scraper.fetch_with_retry(
            'http://httpbin.org/user-agent'
        )

        if response:

            print(
                f'Request {i+1}: OK'
            )

        time.sleep(1)

    response = scraper.fetch_with_retry(
        'http://httpbin.org/headers'
    )

    if response:

        print(
            'Headers OK'
        )

    start = time.time()

    for _ in range(3):

        scraper.fetch_with_retry(
            'http://httpbin.org/delay/1'
        )

    elapsed = time.time() - start

    print(
        f'Time: {elapsed:.2f}s'
    )

if __name__ == "__main__":

    comprehensive_test()
```

Run:

```bash
python final_test.py
```

---

# 🛠️ Troubleshooting

---

## ❌ fake-useragent Missing

```bash
source venv/bin/activate

pip install fake-useragent
```

---

## ❌ Mock Server Not Running

Check:

```bash
sudo netstat -tlnp | grep 8080
```

Kill process:

```bash
sudo kill -9 <PID>
```

Restart:

```bash
python mock_server.py
```

---

## ❌ Connection Errors

Verify internet:

```bash
ping -c 3 google.com
```

Check firewall:

```bash
sudo ufw status
```

Test URL:

```bash
http://httpbin.org/get
```

---

## ❌ User Agents Not Rotating

Clear cache:

```bash
rm -rf ~/.fake_useragent/
```

Upgrade package:

```bash
pip install --upgrade fake-useragent
```

---

# 🎯 Key Accomplishments

✅ Implemented User-Agent Rotation

✅ Built Retry Mechanism

✅ Added CAPTCHA Detection

✅ Simulated Human Delays

✅ Implemented Browser-Like Headers

✅ Created Resilient Scraper Framework

---

# 🌍 Real-World Applications

### 🛒 Price Monitoring

Monitor competitor pricing.

### 📊 Market Research

Aggregate public information.

### 🔍 SEO Intelligence

Analyze websites and rankings.

### 📈 Data Collection

Gather publicly available datasets.

---

# 🚀 Next Steps

### 🌐 Proxy Rotation

Rotate IP addresses.

### 🍪 Cookie Management

Persist sessions.

### 🤖 Selenium Automation

Render JavaScript content.

### 🧩 CAPTCHA Services

Integrate commercial CAPTCHA providers.

### 📊 Distributed Crawling

Scale scraping infrastructure.

---

# ⚖️ Ethical Scraping Guidelines

✅ Respect robots.txt

✅ Implement rate limiting

✅ Scrape only public information

✅ Follow website Terms of Service

✅ Avoid excessive request rates

---

# 🎉 Lab Completed Successfully

You have successfully built an anti-bot scraping framework with:

🔄 User-Agent Rotation

🤖 CAPTCHA Detection

🔁 Retry Logic

⏳ Human-Like Delays

🛡️ Browser Fingerprinting Mitigation

This foundation can be extended into production-grade data collection systems while maintaining responsible and ethical scraping practices.

🚀 Happy Learning!
