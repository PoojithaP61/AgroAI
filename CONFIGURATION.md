# ⚙️ Configuration Guide

## 🔑 API Keys & Environment Variables

### OpenAI API Key (Optional but Recommended)

The AI advisory feature uses OpenAI's API. You can set it in two ways:

**Option 1: Environment Variable (Recommended)**
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your-api-key-here"

# Windows CMD
set OPENAI_API_KEY=your-api-key-here

# Linux/Mac
export OPENAI_API_KEY=your-api-key-here
```

**Option 2: Edit `backend/config.py`**
```python
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "your-api-key-here")
```

**Note:** If you don't set the API key, the AI advisory feature will show a message instead of generating recommendations. The rest of the system will work fine.

### JWT Secret Key (For Production)

**Important:** Change the default secret key in production!

**Option 1: Environment Variable**
```bash
$env:SECRET_KEY="your-very-secure-secret-key-change-this"
```

**Option 2: Edit `backend/config.py`**
```python
SECRET_KEY: str = os.getenv("SECRET_KEY", "your-very-secure-secret-key-change-this")
```

---

## 🗄️ Database Configuration

### SQLite (Default - No Configuration Needed)

The system uses SQLite by default. The database file `agroai.db` will be created automatically in the project root.

**No configuration needed!** Just start the server.

### PostgreSQL (Optional - For Production)

If you want to use PostgreSQL instead:

1. **Install PostgreSQL** and create a database

2. **Set Environment Variable:**
```bash
$env:DATABASE_URL="postgresql://username:password@localhost:5432/agroai"
```

3. **Install PostgreSQL Driver:**
```bash
pip install psycopg2-binary
```

4. **Update `requirements.txt`** (add `psycopg2-binary`)

---

## 📁 File Paths Configuration

All paths are configured with sensible defaults. You can override them:

### ML Model Paths

```bash
# Encoder model path
$env:ENCODER_PATH="ml/encoder/encoder_supcon.pth"

# Training data directory
$env:TRAIN_DATA_DIR="data/fewshot/train"
```

### Upload Directories

```bash
# Where uploaded images are stored
$env:UPLOAD_DIR="data/processed"

# Where Grad-CAM images are saved
$env:GRADCAM_OUTPUT_DIR="data/processed/gradcam"
```

---

## 🖥️ Device Configuration

### CPU (Default)
```bash
$env:DEVICE="cpu"
```

### GPU (If you have CUDA)
```bash
$env:DEVICE="cuda"
```

---

## 🌐 CORS Configuration

CORS is already configured for:
- `http://localhost:3000` (React default)
- `http://localhost:5173` (Vite default)
- `http://localhost:8000` (Backend)

To add more origins, edit `backend/config.py`:
```python
CORS_ORIGINS: list = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://your-domain.com",  # Add your domain
]
```

---

## 📝 Quick Configuration Checklist

### Required (Works Out of the Box)
- ✅ Database: SQLite (automatic)
- ✅ File paths: Default paths (automatic)
- ✅ CORS: Already configured

### Optional (For Better Experience)
- 🔑 OpenAI API Key: For AI advisory feature
- 🔐 Secret Key: Change for production
- 🗄️ PostgreSQL: For production databases
- 🖥️ CUDA: For GPU acceleration

---

## 🚀 Default Configuration

The system works **out of the box** with these defaults:

- **Database**: SQLite (`agroai.db`)
- **Backend Port**: 8000
- **Frontend Port**: 3000 (or 5173 with Vite)
- **Device**: CPU
- **File Upload**: `data/processed/`
- **Grad-CAM**: `data/processed/gradcam/`

**You don't need to change anything to get started!**

---

## 🔒 Security Notes

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Change default secret key** in production
4. **Use HTTPS** in production
5. **Set strong passwords** for database (if using PostgreSQL)

---

## 📚 Environment Variables Summary

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `OPENAI_API_KEY` | (empty) | No | OpenAI API key for AI advisory |
| `SECRET_KEY` | "your-secret-key..." | Yes* | JWT secret key (*change in production) |
| `DATABASE_URL` | "sqlite:///./agroai.db" | No | Database connection string |
| `ENCODER_PATH` | "ml/encoder/encoder_supcon.pth" | No | Path to ML encoder model |
| `TRAIN_DATA_DIR` | "data/fewshot/train" | No | Training data directory |
| `UPLOAD_DIR` | "data/processed" | No | Upload directory |
| `GRADCAM_OUTPUT_DIR` | "data/processed/gradcam" | No | Grad-CAM output directory |
| `DEVICE` | "cpu" | No | "cpu" or "cuda" |

---

## ✅ Ready to Go!

The system is configured to work immediately with sensible defaults. You only need to configure:

1. **OpenAI API Key** (if you want AI advisory)
2. **Secret Key** (for production)

Everything else works out of the box! 🎉
