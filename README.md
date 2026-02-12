# 🌾 CropGuard AI - Crop Disease Detection System

An advanced AI-powered web application for detecting crop diseases using deep learning. Built with Flask, MobileNetV2, and modern web technologies.

## 🎯 Features

- **AI Disease Detection**: Upload crop images to detect 38+ diseases with 95% accuracy
- **Treatment Recommendations**: Get both chemical and organic treatment options
- **Crop Monitoring Dashboard**: Track your crops' health over time
- **Disease Database**: Browse comprehensive information about crop diseases
- **Expert Consultation**: Connect with agricultural experts
- **Detection History**: Save and review past detections
- **Analytics & Charts**: Visualize disease distribution and trends
- **Mobile Responsive**: Works on all devices

## 🚀 Technologies Used

### Backend
- Flask (Python web framework)
- SQLAlchemy (Database ORM)
- Transformers (Hugging Face)
- PyTorch (Deep learning)
- MobileNetV2 (Pre-trained model)

### Frontend
- HTML5, CSS3, JavaScript
- Chart.js (Data visualization)
- Font Awesome (Icons)
- Responsive Design

### Machine Learning
- Model: MobileNetV2 (Transfer Learning)
- Dataset: PlantVillage (54,000+ images)
- Accuracy: ~95%
- Classes: 38 crop diseases

## 📁 Project Structure

```
crop-disease-website/
├── backend/
│   └── app.py              # Main Flask application
├── frontend/
│   ├── static/
│   │   ├── css/           # Stylesheets
│   │   ├── js/            # JavaScript files
│   │   ├── images/        # Images and icons
│   │   └── uploads/       # User uploaded images
│   └── templates/         # HTML templates
│       ├── index.html     # Homepage
│       ├── detect.html    # Detection page
│       ├── dashboard.html # User dashboard
│       ├── disease_database.html
│       ├── consultation.html
│       ├── login.html
│       └── register.html
├── database/
│   └── crops.db           # SQLite database (auto-created)
├── models/                # ML models cache
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- 4GB+ RAM (for ML model)

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd crop-disease-website
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
cd backend
python app.py
```

The application will start on `http://localhost:5000`

## 📱 Usage

### 1. Disease Detection
- Navigate to "Detect Disease" page
- Upload a clear image of affected crop/leaf
- Click "Detect Disease"
- View results with treatment recommendations

### 2. Create Account
- Click "Login" → "Register"
- Fill in your details
- Access personalized dashboard

### 3. Monitor Crops
- Add your crops in the dashboard
- Track detections over time
- View analytics and trends

### 4. Get Expert Help
- Go to "Expert Consultation"
- Fill the form with your query
- Receive expert guidance

## 🎓 Academic Project Information

**Developed by:** [Your Name]  
**Guide:** [Professor Name]  
**Institution:** [Your College/University]  
**Course:** [Your Course]  
**Year:** 2024

### Project Objectives
1. Implement machine learning for agriculture
2. Create user-friendly web interface
3. Provide actionable disease management solutions
4. Enable crop health monitoring

### Model Details
- **Architecture:** MobileNetV2 (Transfer Learning)
- **Framework:** PyTorch + Transformers
- **Training Data:** PlantVillage Dataset
- **Image Count:** 54,000+ images
- **Disease Classes:** 38
- **Accuracy:** ~95%
- **Inference Time:** <2 seconds

## 🌱 Supported Crops & Diseases

### Crops
- Tomato (14 classes)
- Potato (3 classes)
- Corn (4 classes)
- Apple (4 classes)
- Grape (4 classes)
- Cherry (2 classes)
- Peach (2 classes)
- Pepper (2 classes)
- And more...

### Sample Diseases
- Late Blight
- Early Blight
- Septoria Leaf Spot
- Bacterial Spot
- Target Spot
- Mosaic Virus
- Yellow Leaf Curl Virus

## 🔒 Security Features
- Password hashing
- Session management
- File upload validation
- XSS protection
- SQL injection prevention

## 📊 Database Schema

### Users Table
- id, username, email, password_hash, location, created_at

### Detection Table
- id, user_id, crop_id, image_path, disease_name, confidence, detected_at

### Crops Table
- id, user_id, crop_type, location, planted_date, status

### Treatment Table
- id, crop_id, disease_name, treatment_type, applied_date, effectiveness

## 🚀 Deployment Options

### Local Deployment
Already covered in Installation section

### Cloud Deployment

#### Heroku
```bash
# Install Heroku CLI
# Create Procfile
web: gunicorn backend.app:app

# Deploy
heroku create your-app-name
git push heroku main
```

#### PythonAnywhere
1. Upload code
2. Set up virtual environment
3. Configure WSGI file
4. Add static files mapping

#### AWS/Azure/GCP
Use Docker container or VM deployment

## 🔧 Configuration

### Environment Variables
Create `.env` file in backend folder:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///database/crops.db
UPLOAD_FOLDER=frontend/static/uploads
```

### Model Configuration
The model is loaded from Hugging Face:
- Model ID: `linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification`
- Auto-downloaded on first run
- Cached in `~/.cache/huggingface/`

## 📝 API Endpoints

### Detection
- `POST /api/detect` - Upload image and get disease prediction

### User Management
- `POST /api/register` - Register new user
- `POST /api/login` - Login user
- `POST /api/logout` - Logout user

### Crops
- `POST /api/add-crop` - Add new crop
- `GET /api/crops` - Get user's crops

### History
- `GET /api/detections/history` - Get detection history
- `GET /api/stats` - Get user statistics

## 🤝 Contributing
This is an academic project. For suggestions:
1. Fork the repository
2. Create feature branch
3. Submit pull request

## 📄 License
This project is for educational purposes.

## 📞 Contact
- **Email:** [your-email@example.com]
- **GitHub:** [your-github]
- **LinkedIn:** [your-linkedin]

## 🙏 Acknowledgments
- Hugging Face for model hosting
- PlantVillage Dataset creators
- Flask framework developers
- Academic supervisor/guide

## 📚 Future Enhancements
- [ ] Mobile app (React Native)
- [ ] Real-time camera detection
- [ ] Weather API integration
- [ ] Multilingual support
- [ ] SMS/Email alerts
- [ ] Community forum
- [ ] Offline mode
- [ ] Advanced analytics
- [ ] Treatment effectiveness tracking
- [ ] Integration with IoT sensors

## ⚠️ Disclaimer
This is an AI-based preliminary diagnosis tool. Always consult agricultural experts for confirmation and detailed treatment plans. Results are based on training data and may not be 100% accurate in all conditions.

---

**Made with ❤️ for sustainable agriculture**
