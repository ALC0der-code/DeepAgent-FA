# 📦 All Project Files in One Place

Copy each section below and save with the filename shown.

---

## FILE 1: requirements.txt

**Copy everything between the lines:**

```
streamlit==1.29.0
anthropic==0.34.0
```

**Save as:** `requirements.txt`

---

## FILE 2: .gitignore

**Copy everything between the lines:**

```
# Streamlit secrets
.streamlit/secrets.toml

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment variables
.env
.env.local

# Generated files
*.log
```

**Save as:** `.gitignore`

---

## FILE 3: .streamlit/secrets.toml

**Create this file manually:**

1. Create a folder named `.streamlit`
2. Inside it, create a file named `secrets.toml`
3. Add this content:

```
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

4. Replace with your actual API key!

**Save as:** `.streamlit/secrets.toml`

⚠️ **Important:** This file should NOT be pushed to GitHub (it's in .gitignore)

---

## FILE 4: README.md

**Copy this:**

```markdown
# 🤖 Multi-Agent DeepAgent

AI-powered app builder with 5 specialized agents.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Add API Key

Create `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "your-key-here"
```

## Deploy

1. Push to GitHub
2. Go to https://share.streamlit.io
3. Deploy this repo
4. Add API key in Secrets

## Usage

1. Describe your app in plain English
2. Watch 5 AI agents collaborate
3. Download your working app
4. Open in browser

## Example Requests

- "Create a todo list with categories"
- "Build a calculator"
- "Make a habit tracker with streaks"

Built with Streamlit & Claude AI
```

**Save as:** `README.md`

---

## 📊 FILE CHECKLIST

After downloading, you should have:

```
deepagent-app/
├── app.py                    ✅ From artifact "app.py - Main Application"
├── requirements.txt          ✅ From above (2 lines)
├── .gitignore               ✅ From above
├── README.md                ✅ From above
└── .streamlit/
    └── secrets.toml         ✅ Create manually with your API key
```

---

## 🚀 NEXT STEPS

Once you have all files:

```bash
# 1. Test locally
pip install -r requirements.txt
streamlit run app.py

# 2. Push to GitHub
git init
git add .
git commit -m "Initial commit"
# Create repo on GitHub, then:
git remote add origin YOUR-GITHUB-URL
git push -u origin main

# 3. Deploy to Streamlit Cloud
# Go to https://share.streamlit.io
# Click "New app" → Select your repo → Deploy
# Add API key in Secrets
```

---

## ✅ VERIFICATION

Before deploying, check:

- [ ] `streamlit run app.py` works locally
- [ ] You see the web interface at localhost:8501
- [ ] All 5 files are in the right places
- [ ] `.gitignore` is working (secrets.toml not in git)
- [ ] GitHub repo created
- [ ] Code pushed successfully

---

Need help with any file? Just ask!