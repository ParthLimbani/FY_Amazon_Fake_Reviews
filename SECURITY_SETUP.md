# 🔒 Security & Setup Guide

## ⚠️ IMPORTANT: Before Pushing to GitHub

### 1. Verify .env is NOT Committed
The `.env` file contains your **sensitive API keys** and should **NEVER** be committed to git.

**Check:**
```bash
git status
```

If you see `.env` in the output, **DO NOT COMMIT IT!**

The `.gitignore` file already excludes it, but double-check:
```bash
cat .gitignore | grep .env
```

Should show:
```
.env
.env.local
.env.*.local
```

### 2. Use .env.example as Template
The repository includes `.env.example` with placeholder values. This is safe to commit.

**Setup for new users:**
```bash
# Copy the example file
cp backend/.env.example backend/.env

# Edit .env and add your actual API credentials
# NEVER commit backend/.env to git!
```

### 3. API Keys Location

✅ **CORRECT:**
- `backend/.env` - Your actual keys (git ignored)
- `backend/.env.example` - Template with placeholders (committed to git)

❌ **WRONG:**
- Hardcoded in `backend/config.py`
- Hardcoded in any `.py` files
- In documentation files
- In README files

### 4. What's Protected

All sensitive data is now only in `.env`:
- `BRIGHT_DATA_API_TOKEN` - Your Bright Data API token
- Any future API keys or credentials

### 5. Before Each Git Push

Run this checklist:
```bash
# 1. Check no .env files are staged
git status

# 2. Search for accidental API key commits
git grep -i "api_token\|bearer" -- '*.py' '*.md'

# 3. Verify .gitignore includes .env
cat .gitignore | grep .env

# 4. Review what you're about to commit
git diff --cached
```

### 6. If You Accidentally Committed API Keys

**Immediate Actions:**
1. **Rotate your API keys** on Bright Data dashboard
2. Remove keys from git history:
```bash
# Remove from last commit
git reset HEAD~1
git add .
git commit -m "Remove sensitive data"

# If already pushed, you may need to force push (use with caution)
git push --force
```

## 🚀 Setup Instructions for Team Members

### Initial Setup
```bash
# 1. Clone the repository
git clone <your-repo-url>
cd fake_review_v2

# 2. Set up backend
cd backend
cp .env.example .env
# Edit .env and add your Bright Data API token

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Set up frontend
cd ../frontend
npm install

# 5. Run the application
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Getting Your API Token
1. Sign up at https://brightdata.com
2. Navigate to Dashboard → API Access
3. Create a new API token
4. Copy token to `backend/.env`

## 📋 Environment Variables Reference

### Required Variables
```bash
BRIGHT_DATA_API_TOKEN=your_actual_token_here  # Get from Bright Data dashboard
BRIGHT_DATA_DATASET_ID=gd_le8e811kzy4ggddlq # Amazon Reviews dataset
```

### Optional Variables
```bash
API_HOST=0.0.0.0                    # API host
API_PORT=8000                       # API port
DEBUG=True                          # Debug mode
MODEL_CONFIDENCE_THRESHOLD=0.5      # ML confidence threshold
MAX_REVIEWS_PER_REQUEST=500         # Rate limiting
```

## 🔐 Security Best Practices

### What We've Implemented:
✅ All API keys in environment variables
✅ `.env` excluded from git via `.gitignore`
✅ `.env.example` template for team members
✅ No hardcoded credentials in source code
✅ Clear separation of config and secrets

### Additional Recommendations:
- **Never share** your `.env` file
- **Rotate API keys** regularly
- **Use different keys** for dev/staging/production
- **Monitor API usage** on Bright Data dashboard
- **Set up alerts** for unusual API activity

## 🆘 Troubleshooting

### "API token not found"
1. Verify `.env` file exists in `backend/` folder
2. Check `.env` has `BRIGHT_DATA_API_TOKEN=your_token`
3. Restart the backend server after editing `.env`

### "Customer is not active" error
1. Your Bright Data account needs activation
2. Log in to https://brightdata.com
3. Complete account verification
4. Check your dataset access

### Demo data showing instead of real data
1. Verify API token is correctly set in `.env`
2. Check backend logs for API errors
3. Ensure Bright Data account is active
4. The app automatically falls back to demo data if API fails

## 📝 Git Workflow

### Safe Commit Process
```bash
# 1. Check status
git status

# 2. Add only necessary files (NEVER git add .)
git add backend/services/
git add frontend/src/
git add README.md

# 3. Verify what's staged
git diff --cached

# 4. Commit
git commit -m "Your message"

# 5. Push
git push
```

### Files to NEVER Commit
- `backend/.env`
- `backend/__pycache__/`
- `backend/*.pyc`
- `node_modules/`
- `venv/`
- Any files with API keys

### Files SAFE to Commit
- `backend/.env.example`
- All `.py` source files
- All `.jsx` frontend files
- `requirements.txt`
- `package.json`
- Documentation (`.md` files)
- `.gitignore`

---

**Remember:** When in doubt, don't commit! Review carefully before pushing to GitHub.
