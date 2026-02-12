# 🌾 CropGuard AI - Complete Website Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Installation Guide](#installation-guide)
5. [Usage Guide](#usage-guide)
6. [API Documentation](#api-documentation)
7. [Database Schema](#database-schema)
8. [Deployment Guide](#deployment-guide)
9. [Future Enhancements](#future-enhancements)

---

## 🎯 Project Overview

CropGuard AI is a comprehensive web-based crop disease detection and monitoring system that uses artificial intelligence to help farmers identify and manage crop diseases effectively.

### Key Objectives
- Provide instant disease detection using AI
- Offer treatment recommendations (chemical & organic)
- Enable crop health monitoring over time
- Connect farmers with agricultural experts
- Maintain comprehensive disease database

---

## ✨ Features

### 1. **AI Disease Detection**
- Upload crop/leaf images
- Get instant disease identification
- 95% accuracy rate
- Support for 38+ diseases
- Confidence score display

### 2. **Treatment Recommendations**
- Chemical treatment options
- Organic alternatives
- Prevention measures
- Severity assessment

### 3. **User Dashboard**
- Personal account system
- Detection history
- Crop monitoring
- Analytics & charts
- Export capabilities

### 4. **Disease Database**
- Browse all diseases
- Detailed information
- Search functionality
- Symptoms & treatments

### 5. **Expert Consultation**
- Contact form
- Direct expert connection
- Query tracking

### 6. **Crop Monitoring**
- Add multiple crops
- Track health status
- Treatment history
- Location tracking

---

## 🛠️ Technology Stack

### Backend
```
Flask           3.0.0    - Web framework
SQLAlchemy      3.1.1    - ORM
Transformers    4.36.0   - ML models
PyTorch         2.1.0    - Deep learning
Pillow          10.1.0   - Image processing
```

### Frontend
```
HTML5/CSS3               - Structure & styling
JavaScript (ES6+)        - Interactivity
Chart.js                 - Data visualization
Font Awesome 6.4.0       - Icons
```

### Machine Learning
```
Model: MobileNetV2 (Transfer Learning)
Dataset: PlantVillage
Images: 54,000+
Classes: 38
Framework: PyTorch
```

---

## 🚀 Installation Guide

### Prerequisites
- Python 3.8+
- pip package manager
- 4GB+ RAM
- Modern web browser

### Step-by-Step Installation

#### 1. Clone/Download Project
```bash
git clone <repository-url>
cd crop-disease-website
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Setup Database
```bash
cd backend
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

#### 5. Run Application
```bash
python app.py
```

#### 6. Access Application
Open browser: `http://localhost:5000`

---

## 📖 Usage Guide

### For First-Time Users

#### 1. **Registration**
- Click "Login" → "Register"
- Fill in: Username, Email, Password, Location
- Submit to create account

#### 2. **Disease Detection**
- Go to "Detect Disease"
- Upload clear crop/leaf image
- Click "Detect Disease"
- View results and recommendations

#### 3. **Dashboard Access**
- Navigate to "Dashboard"
- View statistics
- See detection history
- Add crops for monitoring

#### 4. **Expert Consultation**
- Go to "Expert Consultation"
- Fill consultation form
- Submit query
- Track status

---

## 📡 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/register
Content-Type: application/json

{
  "username": "farmerjohn",
  "email": "john@example.com",
  "password": "secure123",
  "location": "Maharashtra"
}

Response: 200 OK
{
  "success": true,
  "message": "Registration successful"
}
```

#### Login
```http
POST /api/login
Content-Type: application/json

{
  "username": "farmerjohn",
  "password": "secure123"
}

Response: 200 OK
{
  "success": true,
  "message": "Login successful"
}
```

#### Logout
```http
POST /api/logout

Response: 200 OK
{
  "success": true
}
```

### Detection Endpoints

#### Detect Disease
```http
POST /api/detect
Content-Type: multipart/form-data

Form Data:
- image: [file]

Response: 200 OK
{
  "disease_name": "Tomato___Late_blight",
  "confidence": 94.5,
  "prediction_time": 1.23,
  "disease_info": {
    "description": "...",
    "symptoms": "...",
    "treatment": [...],
    "prevention": [...],
    "organic_solution": "...",
    "severity": "High"
  },
  "image_url": "/static/uploads/1234567890_image.jpg"
}
```

#### Get Detection History
```http
GET /api/detections/history

Response: 200 OK
[
  {
    "id": 1,
    "disease_name": "Tomato___Late_blight",
    "confidence": 94.5,
    "detected_at": "2024-01-15T10:30:00",
    "image_url": "/static/uploads/..."
  }
]
```

### Crop Management

#### Add Crop
```http
POST /api/add-crop
Content-Type: application/json

{
  "crop_type": "Tomato",
  "location": "Field A",
  "planted_date": "2024-01-01"
}

Response: 200 OK
{
  "success": true,
  "crop_id": 1
}
```

### Statistics

#### Get User Stats
```http
GET /api/stats

Response: 200 OK
{
  "total_detections": 15,
  "total_crops": 5,
  "disease_distribution": {
    "Tomato___Late_blight": 3,
    "Tomato___healthy": 7,
    ...
  }
}
```

---

## 💾 Database Schema

### Users Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    location VARCHAR(100),
    created_at DATETIME
);
```

### Detections Table
```sql
CREATE TABLE detection (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    crop_id INTEGER,
    image_path VARCHAR(200) NOT NULL,
    disease_name VARCHAR(100) NOT NULL,
    confidence FLOAT NOT NULL,
    detected_at DATETIME,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (crop_id) REFERENCES crop(id)
);
```

### Crops Table
```sql
CREATE TABLE crop (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    crop_type VARCHAR(50) NOT NULL,
    location VARCHAR(100),
    planted_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

### Treatments Table
```sql
CREATE TABLE treatment (
    id INTEGER PRIMARY KEY,
    crop_id INTEGER NOT NULL,
    disease_name VARCHAR(100),
    treatment_type VARCHAR(50),
    treatment_details TEXT,
    applied_date DATETIME,
    effectiveness VARCHAR(20),
    notes TEXT,
    FOREIGN KEY (crop_id) REFERENCES crop(id)
);
```

### Consultations Table
```sql
CREATE TABLE consultation (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(20),
    crop_type VARCHAR(50),
    message TEXT NOT NULL,
    status VARCHAR(20),
    created_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

---

## 🌐 Deployment Guide

### Local Development
Already covered in Installation Guide above.

### Production Deployment

#### Option 1: Heroku
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create cropguard-ai

# Add buildpacks
heroku buildpacks:set heroku/python

# Create Procfile
echo "web: gunicorn backend.app:app" > Procfile

# Deploy
git push heroku main

# Open app
heroku open
```

#### Option 2: PythonAnywhere
1. Upload code via git or zip
2. Create virtual environment
3. Install dependencies
4. Configure WSGI file:
```python
import sys
path = '/home/yourusername/crop-disease-website'
if path not in sys.path:
    sys.path.append(path)

from backend.app import app as application
```
5. Set up static files mapping
6. Reload web app

#### Option 3: AWS EC2
```bash
# SSH into EC2 instance
ssh -i key.pem ubuntu@ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Clone code
git clone <repo>

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn --bind 0.0.0.0:5000 backend.app:app

# Configure nginx as reverse proxy
# Setup systemd service for auto-start
```

#### Option 4: Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "backend/app.py"]
```

```bash
# Build image
docker build -t cropguard-ai .

# Run container
docker run -p 5000:5000 cropguard-ai
```

---

## 🔐 Security Considerations

### Implemented
- Password hashing (Werkzeug)
- Session management
- File upload validation
- SQL injection prevention (SQLAlchemy)
- XSS protection

### Recommended for Production
- HTTPS/SSL certificate
- Rate limiting
- CSRF protection
- Input sanitization
- Environment variables for secrets
- Regular security updates

---

## 🎨 Customization Guide

### Branding
Update in:
- `frontend/static/css/style.css` (colors, fonts)
- `frontend/templates/*.html` (text, logos)

### Colors
Edit CSS variables in `style.css`:
```css
:root {
    --primary: #10b981;  /* Change main color */
    --secondary: #3b82f6; /* Change accent color */
}
```

### Adding New Crops
1. Add to disease info in `backend/app.py`
2. Update dropdown in templates
3. Add to supported crops list

---

## 🚀 Future Enhancements

### Planned Features
- [ ] Mobile app (React Native/Flutter)
- [ ] Real-time camera detection
- [ ] Weather API integration
- [ ] SMS/Email notifications
- [ ] Multilingual support (Hindi, Marathi, etc.)
- [ ] Community forum
- [ ] Crop yield prediction
- [ ] Market price integration
- [ ] Government scheme information
- [ ] Offline mode with PWA

### Advanced Features
- [ ] IoT sensor integration
- [ ] Drone image analysis
- [ ] Satellite imagery integration
- [ ] AR visualization
- [ ] Blockchain for supply chain
- [ ] Machine learning model retraining
- [ ] Custom model training for regional crops

---

## 👨‍💻 Development Guidelines

### Code Style
- Follow PEP 8 for Python
- Use ESLint for JavaScript
- Comment complex logic
- Write meaningful commit messages

### Testing
```bash
# Run tests (when implemented)
pytest tests/

# Test coverage
pytest --cov=backend tests/
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add: new feature description"

# Push and create PR
git push origin feature/new-feature
```

---

## 📞 Support & Contact

### Academic Queries
- **Student:** [Your Name]
- **Email:** [your-email@example.com]
- **Guide:** [Professor Name]

### Technical Support
- GitHub Issues: [repo-url]/issues
- Documentation: See README.md

---

## 📄 License
This is an academic project. For educational use only.

---

## 🙏 Acknowledgments
- Hugging Face for model hosting
- PlantVillage Dataset team
- Flask framework developers
- Academic supervisor/guide
- Open source community

---

**Last Updated:** 2024
**Version:** 1.0.0
**Status:** Academic Project - Active Development
