# AgroAI Backend API

FastAPI backend for the AgroAI Plant Disease Detection System.

## Features

- ✅ **Authentication System** - JWT-based user authentication
- ✅ **Disease Detection** - Full ML pipeline integration
- ✅ **Grad-CAM Visualization** - Explainable AI heatmaps
- ✅ **AI Advisory** - LLM-powered disease recommendations
- ✅ **User Management** - Admin endpoints for user control
- ✅ **Analytics** - Disease statistics and prediction history

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables (Optional)

Create a `.env` file or set environment variables:

```bash
# Database
DATABASE_URL=sqlite:///./agroai.db  # or PostgreSQL URL

# Security
SECRET_KEY=your-secret-key-here

# ML Model Paths
ENCODER_PATH=ml/encoder/encoder_supcon.pth
TRAIN_DATA_DIR=data/fewshot/train

# OpenAI API (for AI reasoning)
OPENAI_API_KEY=your-openai-api-key

# Device
DEVICE=cpu  # or cuda
```

### 3. Initialize Database

The database will be automatically initialized on first startup.

### 4. Start Server

```bash
# Option 1: Using the startup script
python backend/start.py

# Option 2: Using uvicorn directly
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication (`/api/v1/auth`)

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get access token
- `GET /api/v1/auth/me` - Get current user info

### Diagnosis (`/api/v1/diagnosis`)

- `POST /api/v1/diagnosis/predict` - Upload image and get disease prediction
- `GET /api/v1/diagnosis/history` - Get user's prediction history
- `GET /api/v1/diagnosis/history/{id}` - Get prediction details
- `GET /api/v1/diagnosis/gradcam/{id}` - Get Grad-CAM visualization

### Admin (`/api/v1/admin`)

- `GET /api/v1/admin/stats` - System statistics
- `GET /api/v1/admin/diseases` - Disease statistics
- `GET /api/v1/admin/users` - List all users
- `GET /api/v1/admin/users/{id}` - User details
- `PUT /api/v1/admin/users/{id}/activate` - Activate user
- `PUT /api/v1/admin/users/{id}/deactivate` - Deactivate user
- `PUT /api/v1/admin/users/{id}/make-admin` - Grant admin privileges

## Usage Example

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "farmer@example.com",
    "username": "farmer1",
    "password": "securepassword",
    "full_name": "John Farmer"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=farmer1&password=securepassword"
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {...}
}
```

### 3. Predict Disease

```bash
curl -X POST "http://localhost:8000/api/v1/diagnosis/predict" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@path/to/plant_image.jpg" \
  -F "crop_type=Tomato" \
  -F "location=Field A"
```

## Database Models

- **User** - User accounts (farmers and admins)
- **Prediction** - Disease prediction records
- **DiseaseHistory** - Aggregated disease statistics

## Notes

- The ML models are initialized on server startup
- First startup may take a few minutes to load models
- Ensure `ml/encoder/encoder_supcon.pth` exists
- Ensure `data/fewshot/train` directory exists with training data
