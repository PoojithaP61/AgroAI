# 🚀 EXACT COMMANDS TO RUN - COPY & PASTE

## 📍 **IMPORTANT: You MUST be in this directory:**
```
C:\Users\pooji\OneDrive\Desktop\AgroAI_FinalYear_Project
```

---

## ✅ **STEP 1: Open PowerShell/Terminal**

Open PowerShell or Command Prompt.

---

## ✅ **STEP 2: Navigate to Project Directory**

**Copy and paste this EXACT command:**

```powershell
cd C:\Users\pooji\OneDrive\Desktop\AgroAI_FinalYear_Project
```

---

## ✅ **STEP 3: Activate Virtual Environment**

**Copy and paste this EXACT command:**

```powershell
.\finalenv\Scripts\Activate.ps1
```

**OR if that doesn't work, try:**

```powershell
finalenv\Scripts\activate
```

**You should see `(finalenv)` at the start of your prompt.**

---

## ✅ **STEP 4: Install Dependencies**

**Copy and paste this EXACT command:**

```powershell
pip install -r requirements.txt
```

**Wait for installation to complete (may take 2-5 minutes).**

---

## ✅ **STEP 5: Start the Backend Server**

**Copy and paste this EXACT command:**

```powershell
python backend\start.py
```

**OR use this alternative:**

```powershell
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

---

## 🎯 **Expected Output**

You should see:
```
🚀 Starting AgroAI Backend...
📦 Initializing database...
✅ Database initialized
🤖 Initializing ML models...
✅ ML models loaded successfully
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 🌐 **Access the API**

Once running, open your browser and go to:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## ⚠️ **If You Get Errors**

### Error: "ModuleNotFoundError: No module named 'fastapi'"
**Solution:** Make sure you activated the virtual environment (Step 3)

### Error: "No module named 'backend'"
**Solution:** Make sure you're in the project root directory (Step 2)

### Error: "Cannot activate virtual environment"
**Solution:** Try running PowerShell as Administrator, or use:
```powershell
python -m venv finalenv
.\finalenv\Scripts\Activate.ps1
```

### Error: "Port 8000 already in use"
**Solution:** Change the port in `backend/start.py` or kill the process using port 8000

---

## 📝 **Quick Reference - All Commands in Order**

```powershell
# 1. Navigate to project
cd C:\Users\pooji\OneDrive\Desktop\AgroAI_FinalYear_Project

# 2. Activate virtual environment
.\finalenv\Scripts\Activate.ps1

# 3. Install dependencies (only needed once)
pip install -r requirements.txt

# 4. Start server
python backend\start.py
```

---

## 🎉 **That's it! Your backend should now be running!**
