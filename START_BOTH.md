# 🚀 Starting Both Backend and Frontend

## ⚠️ Important: Both Servers Must Be Running!

The frontend needs the backend API to be running. Here's how to start both:

---

## 📋 Step-by-Step Instructions

### Terminal 1: Start Backend

```powershell
# Navigate to project root
cd C:\Users\pooji\OneDrive\Desktop\AgroAI_FinalYear_Project

# Activate virtual environment
.\finalenv\Scripts\Activate.ps1

# Start backend server
python backend\start.py
```

**Expected output:**
```
🚀 Starting AgroAI Backend...
📦 Initializing database...
✅ Database initialized
🤖 Initializing ML models...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open!**

---

### Terminal 2: Start Frontend

Open a **NEW** PowerShell window:

```powershell
# Navigate to project root
cd C:\Users\pooji\OneDrive\Desktop\AgroAI_FinalYear_Project

# Start frontend (from root)
.\start_frontend.bat

# OR navigate to frontend and run:
cd frontend
npm run dev
```

**Expected output:**
```
VITE v5.4.21  ready in 288 ms
➜  Local:   http://localhost:3000/
```

**Keep this terminal open too!**

---

## ✅ Verify Both Are Running

1. **Backend**: http://localhost:8000/docs (should show Swagger UI)
2. **Frontend**: http://localhost:3000 (should show login page)

---

## 🔧 Quick Fix for Current Error

If you see `ECONNREFUSED`:

1. **Check if backend is running:**
   - Open http://localhost:8000/docs in browser
   - If it doesn't load, backend is not running

2. **Start the backend:**
   ```powershell
   cd C:\Users\pooji\OneDrive\Desktop\AgroAI_FinalYear_Project
   .\finalenv\Scripts\Activate.ps1
   python backend\start.py
   ```

3. **Wait for backend to fully start** (you'll see "Uvicorn running")

4. **Refresh the frontend** (http://localhost:3000)

---

## 🎯 Quick Start Scripts

### Option 1: Manual (Two Terminals)

**Terminal 1:**
```powershell
cd C:\Users\pooji\OneDrive\Desktop\AgroAI_FinalYear_Project
.\finalenv\Scripts\Activate.ps1
python backend\start.py
```

**Terminal 2:**
```powershell
cd C:\Users\pooji\OneDrive\Desktop\AgroAI_FinalYear_Project
cd frontend
npm run dev
```

### Option 2: Use Batch Files

**Terminal 1:**
```powershell
.\start_backend.bat
```

**Terminal 2:**
```powershell
.\start_frontend.bat
```

---

## ⚠️ Common Issues

### Backend won't start
- Make sure virtual environment is activated
- Check if port 8000 is already in use
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Frontend can't connect
- **Backend must be running first!**
- Check backend is on http://localhost:8000
- Verify CORS is configured in backend/config.py

### Port already in use
- Backend: Change port in `backend/start.py` (line 89)
- Frontend: Change port in `frontend/vite.config.js` (line 7)

---

## 🎉 Once Both Are Running

1. Open http://localhost:3000
2. Register a new account
3. Login
4. Upload a plant image
5. View disease detection results!

---

## 📝 Summary

**You need TWO terminals:**
- **Terminal 1**: Backend (Python/FastAPI) on port 8000
- **Terminal 2**: Frontend (React/Vite) on port 3000

**Both must be running simultaneously!**
