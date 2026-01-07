# 🌱 AgroAI: Intelligent Plant Disease Detection System

AgroAI is a final-year project designed to assist farmers and agronomists in early detection of plant diseases using Deep Learning. It combines a **FastAPI** backend with a modern **React** frontend to provide real-time diagnosis, disease intelligence, and AI-powered advisory.

![AgroAI Banner](https://via.placeholder.com/1200x400?text=AgroAI+Plant+Disease+Detection)

## 🚀 Features

-   **Disease Detection**: Upload plant leaf images to detect diseases with high accuracy using PyTorch models.
-   **Visual Explanations**: Grad-CAM heatmaps show exactly *where* the model is looking.
-   **AI Advisory**: Generative AI provides actionable treatment advice based on the diagnosis and crop type.
-   **History & Tracking**: Save your predictions and track disease spread over time.
-   **Stage Analysis**: Estimates disease severity (Early, Mid, Late).
-   **Multi-Crop Support**: Capable of handling various crop types.
-   **Admin Dashboard**: Monitor system stats and train new diseases dynamically.

## 🛠️ Tech Stack

-   **Frontend**: React, Vite, Tailwind CSS, Lucide Icons, Axios, Recharts.
-   **Backend**: FastAPI, SQLAlchemy, Pydantic, Uvicorn, Python-Jose (JWT).
-   **Database**: MySQL (Production) / SQLite (Dev).
-   **AI/ML**: PyTorch, Torchvision, OpenAI API (for advisory), Grad-CAM.

---

## 📦 Installation & Setup

### Prerequisites
-   **Python 3.9+**
-   **Node.js 18+**
-   **MySQL Server** (Optional, can use SQLite for testing)

### 1. Backend Setup
1.  Navigate to the project root.
2.  Create a virtual environment:
    ```bash
    python -m venv finalenv
    # Windows
    finalenv\Scripts\activate
    # Mac/Linux
    source finalenv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configuration**:
    -   Create a `.env` file in the root directory (copy from `.env.example`).
    -   Add your **Gmail credentials** (for email verification) and **OpenAI API Key**.
    ```env
    DB_USER=root
    DB_PASSWORD=your_password
    DB_NAME=agroai
    SECRET_KEY=your_secret_key
    OPENAI_API_KEY=your_openai_key
    # Email Settings
    EMAIL_SENDER=your_email@gmail.com
    EMAIL_PASSWORD=your_app_password
    ```
5.  Start the Backend:
    ```bash
    # Run from the root directory
    uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
    ```
    The API will be available at `http://localhost:8000/docs`.

### 2. Frontend Setup
1.  Open a new terminal and navigate to `frontend`:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the Development Server:
    ```bash
    npm run dev
    ```
    The app will run at `http://localhost:3000`.

## 📡 API Endpoints Summary

### Authentication
- `POST /api/v1/auth/register` - Register new user (Email verification required)
- `POST /api/v1/auth/login` - Login (returns JWT token)
- `POST /api/v1/auth/forgot-password` - Request password reset code
- `POST /api/v1/auth/reset-password` - Reset password with code
- `GET /api/v1/auth/me` - Get current user info

### Disease Detection
- `POST /api/v1/diagnosis/predict` - Upload image, get full diagnosis
- `GET /api/v1/diagnosis/history` - User's prediction history
- `GET /api/v1/diagnosis/history/{id}` - Prediction details
- `GET /api/v1/diagnosis/gradcam/{id}` - Grad-CAM image

### Admin (Requires admin token)
- `GET /api/v1/admin/stats` - System statistics
- `GET /api/v1/admin/diseases` - Disease statistics
- `POST /api/v1/admin/train` - Train new disease class dynamically

## 🗃️ Database Schema
The application automatically creates tables on startup:
-   **users**: Authentication and profiles.
-   **predictions**: Stores image paths, diagnosis results, and metadata.
-   **disease_history**: Aggregated stats for analysis.
-   **verification_codes**: Stores OTPs for email verification/password reset.

## 🤝 Contributing
1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit changes (`git commit -m 'Add AmazingFeature'`).
4.  Push to branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---
*Built with ❤️ for Agriculture*
