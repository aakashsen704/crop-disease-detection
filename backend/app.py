from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import os
import time
from datetime import datetime
import json

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:/crop-disease-website/database/crops.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'frontend/static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

CORS(app)
db = SQLAlchemy(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load ML Model
print("🔄 Loading model... Please wait...")
MODEL_NAME = "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
print("✅ Model loaded successfully!")

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    detections = db.relationship('Detection', backref='user', lazy=True)
    crops = db.relationship('Crop', backref='user', lazy=True)

class Detection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id'))
    image_path = db.Column(db.String(200), nullable=False)
    disease_name = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crop_type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))
    planted_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='healthy')  # healthy, infected, treated
    detections = db.relationship('Detection', backref='crop', lazy=True)
    treatments = db.relationship('Treatment', backref='crop', lazy=True)

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id'), nullable=False)
    disease_name = db.Column(db.String(100))
    treatment_type = db.Column(db.String(50))  # chemical, organic
    treatment_details = db.Column(db.Text)
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    effectiveness = db.Column(db.String(20))  # effective, partially_effective, not_effective
    notes = db.Column(db.Text)

class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    crop_type = db.Column(db.String(50))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, replied, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Disease Information Database
DISEASE_INFO = {
    "Tomato___Late_blight": {
        "description": "Late blight is a devastating disease caused by the fungus-like organism Phytophthora infestans.",
        "symptoms": "Dark brown to black lesions on leaves, stems, and fruits. White fungal growth on undersides of leaves in humid conditions.",
        "treatment": [
            "Remove and destroy infected plants immediately",
            "Apply copper-based fungicides (Copper oxychloride 50% WP @ 3g/liter)",
            "Use resistant varieties like Pusa Ruby, Pusa Rohini",
            "Ensure proper spacing for air circulation"
        ],
        "prevention": [
            "Avoid overhead irrigation",
            "Plant in well-drained soil",
            "Remove volunteer potato plants nearby",
            "Apply preventive fungicide sprays during monsoon"
        ],
        "organic_solution": "Neem oil spray (5ml/liter) + Bordeaux mixture (1%)",
        "severity": "High - Can destroy entire crop within 2 weeks"
    },
    "Tomato___Early_blight": {
        "description": "Early blight is caused by fungus Alternaria solani, affecting older leaves first.",
        "symptoms": "Circular spots with concentric rings (target-like pattern) on older leaves. Yellowing around spots.",
        "treatment": [
            "Apply Mancozeb 75% WP @ 2.5g/liter water",
            "Remove infected lower leaves",
            "Spray Chlorothalonil 75% WP @ 2g/liter",
            "Maintain adequate potassium levels in soil"
        ],
        "prevention": [
            "Crop rotation with non-solanaceous crops",
            "Mulching to prevent soil splash",
            "Adequate spacing between plants",
            "Balanced fertilization (avoid excess nitrogen)"
        ],
        "organic_solution": "Baking soda spray (1 tablespoon/liter water) + liquid soap (few drops)",
        "severity": "Medium - Progressive disease, manageable if caught early"
    },
    "Potato___Late_blight": {
        "description": "Same pathogen as tomato late blight. Historically caused Irish Potato Famine.",
        "symptoms": "Water-soaked lesions on leaves turning dark brown/black. White mold on leaf undersides in moist conditions.",
        "treatment": [
            "Metalaxyl + Mancozeb combination @ 2.5g/liter",
            "Remove infected tubers immediately",
            "Spray Cymoxanil 8% + Mancozeb 64% WP",
            "Hill up soil around plants to protect tubers"
        ],
        "prevention": [
            "Use certified disease-free seed potatoes",
            "Plant resistant varieties (Kufri Giriraj, Kufri Jyoti)",
            "Avoid irrigation late in the day",
            "Proper storage of harvested potatoes"
        ],
        "organic_solution": "Copper sulfate solution (Bordeaux mixture 1%)",
        "severity": "Very High - Can cause total crop loss"
    },
    "Tomato___healthy": {
        "description": "Your crop appears healthy with no visible disease symptoms.",
        "symptoms": "No disease detected. Plant shows normal growth patterns.",
        "treatment": ["Continue regular care and monitoring"],
        "prevention": [
            "Maintain current good practices",
            "Regular monitoring for early disease detection",
            "Balanced fertilization",
            "Proper irrigation management"
        ],
        "organic_solution": "No treatment needed. Continue preventive care.",
        "severity": "None - Plant is healthy"
    }
}

DEFAULT_INFO = {
    "description": "Disease detected. Consult local agricultural extension officer for detailed information.",
    "symptoms": "Various symptoms may be present. Please observe your crop carefully.",
    "treatment": [
        "Consult Krishi Vigyan Kendra (KVK)",
        "Contact agricultural extension officer",
        "Take sample to nearest agricultural university"
    ],
    "prevention": ["Regular monitoring", "Proper crop management", "Maintain field hygiene"],
    "organic_solution": "Consult organic farming experts in your area",
    "severity": "Unknown - Professional diagnosis recommended"
}

def predict_disease(image_path):
    """Predict disease from image"""
    start_time = time.time()
    
    # Load and preprocess image
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt")
    
    # Make prediction
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
    
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    confidence, predicted_idx = torch.max(probabilities, 1)
    
    predicted_class = model.config.id2label[predicted_idx.item()]
    confidence_score = confidence.item() * 100
    
    end_time = time.time()
    prediction_time = end_time - start_time
    
    disease_data = DISEASE_INFO.get(predicted_class, DEFAULT_INFO)
    
    return {
        'disease_name': predicted_class,
        'confidence': confidence_score,
        'prediction_time': prediction_time,
        'disease_info': disease_data
    }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect')
def detect_page():
    return render_template('detect.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    detections = Detection.query.filter_by(user_id=user.id).order_by(Detection.detected_at.desc()).limit(10).all()
    crops = Crop.query.filter_by(user_id=user.id).all()
    
    return render_template('dashboard.html', user=user, detections=detections, crops=crops)

@app.route('/disease-database')
def disease_database():
    return render_template('disease_database.html', diseases=DISEASE_INFO)

@app.route('/consultation')
def consultation():
    return render_template('consultation.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

# API Routes
@app.route('/api/detect', methods=['POST'])
def api_detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save uploaded file
    filename = secure_filename(f"{int(time.time())}_{file.filename}")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Predict disease
    result = predict_disease(filepath)
    
    # Save detection to database if user is logged in
    if 'user_id' in session:
        detection = Detection(
            user_id=session['user_id'],
            image_path=filepath,
            disease_name=result['disease_name'],
            confidence=result['confidence']
        )
        db.session.add(detection)
        db.session.commit()
        result['detection_id'] = detection.id
    
    result['image_url'] = f"/static/uploads/{filename}"
    return jsonify(result)

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        location=data.get('location', '')
    )
    db.session.add(user)
    db.session.commit()
    
    session['user_id'] = user.id
    return jsonify({'success': True, 'message': 'Registration successful'})

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        session['user_id'] = user.id
        return jsonify({'success': True, 'message': 'Login successful'})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.pop('user_id', None)
    return jsonify({'success': True})

@app.route('/api/consultation', methods=['POST'])
def api_consultation():
    data = request.json
    
    consultation = Consultation(
        user_id=session.get('user_id'),
        name=data['name'],
        email=data['email'],
        phone=data.get('phone', ''),
        crop_type=data.get('crop_type', ''),
        message=data['message']
    )
    db.session.add(consultation)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Consultation request submitted'})

@app.route('/api/add-crop', methods=['POST'])
def api_add_crop():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    crop = Crop(
        user_id=session['user_id'],
        crop_type=data['crop_type'],
        location=data.get('location', ''),
        planted_date=datetime.strptime(data['planted_date'], '%Y-%m-%d').date() if data.get('planted_date') else None
    )
    db.session.add(crop)
    db.session.commit()
    
    return jsonify({'success': True, 'crop_id': crop.id})

@app.route('/api/detections/history')
def api_detection_history():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    detections = Detection.query.filter_by(user_id=session['user_id']).order_by(Detection.detected_at.desc()).all()
    
    return jsonify([{
        'id': d.id,
        'disease_name': d.disease_name,
        'confidence': d.confidence,
        'detected_at': d.detected_at.isoformat(),
        'image_url': d.image_path.replace('frontend/static', '/static')
    } for d in detections])

@app.route('/api/stats')
def api_stats():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    total_detections = Detection.query.filter_by(user_id=session['user_id']).count()
    total_crops = Crop.query.filter_by(user_id=session['user_id']).count()
    
    # Get disease distribution
    detections = Detection.query.filter_by(user_id=session['user_id']).all()
    disease_counts = {}
    for d in detections:
        disease_counts[d.disease_name] = disease_counts.get(d.disease_name, 0) + 1
    
    return jsonify({
        'total_detections': total_detections,
        'total_crops': total_crops,
        'disease_distribution': disease_counts
    })

if __name__ == '__main__':
    # Database will be created automatically on first request
    app.run(debug=True, host='0.0.0.0', port=5000)