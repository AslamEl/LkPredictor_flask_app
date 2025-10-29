import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)

import pandas as pd
import joblib
import json
import jwt
from datetime import datetime, timedelta
from flask import Flask, request, render_template, jsonify, redirect, url_for, make_response
from config import Config
from database import Database
from models.user import User
from models.prediction import Prediction
from auth import token_required

# Initialize the app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
try:
    Database.initialize()
    print("✓ Database connected successfully")
except Exception as e:
    print(f"⚠ Warning: Could not connect to MongoDB: {e}")
    print("  Make sure MongoDB is running on localhost:27017")
    print("  The app will start but database features won't work.")

# Load the trained model
try:
    model = joblib.load(Config.MODEL_PATH)
    print("✓ House price model loaded successfully")
except Exception as e:
    print(f"✗ Error loading house price model: {e}")
    model = None

# Load the column list
with open(Config.MODEL_COLUMNS_PATH, 'r') as f:
    MODEL_COLUMNS = json.load(f)

# Load diabetes model and scaler
try:
    diabetes_model = joblib.load(Config.DIABETES_MODEL_PATH)
    diabetes_scaler = joblib.load(Config.DIABETES_SCALER_PATH)
    print("✓ Diabetes model loaded successfully")
except Exception as e:
    print(f"✗ Error loading diabetes model: {e}")
    diabetes_model = None
    diabetes_scaler = None

# Load diabetes model columns
try:
    with open('diabetes_model_columns.json', 'r') as f:
        DIABETES_COLUMNS = json.load(f)
except Exception as e:
    print(f"✗ Error loading diabetes columns: {e}")
    DIABETES_COLUMNS = None


# ==================== PUBLIC ROUTES ====================

@app.route('/')
def landing():
    """Landing page"""
    return render_template('landing.html')


@app.route('/login')
def login_page():
    """Login page"""
    return render_template('login.html')


@app.route('/signup')
def signup_page():
    """Signup page"""
    return render_template('signup.html')


# ==================== AUTH API ROUTES ====================

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """Handle user registration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('email') or not data.get('password') or not data.get('name'):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        email = data['email'].lower().strip()
        name = data['name'].strip()
        password = data['password']
        
        # Check if user already exists
        if User.find_by_email(email):
            return jsonify({'success': False, 'message': 'User already exists'}), 400
        
        # Create new user
        user = User.create_user(email=email, name=name, password=password)
        
        # Generate JWT token
        token = jwt.encode(
            {
                'email': user.email,
                'name': user.name,
                'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
            },
            Config.JWT_SECRET_KEY,
            algorithm='HS256'
        )
        
        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'token': token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Handle user login"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'success': False, 'message': 'Missing email or password'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # Verify credentials
        user = User.verify_password(email, password)
        
        if not user:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        # Generate JWT token
        token = jwt.encode(
            {
                'email': user.email,
                'name': user.name,
                'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
            },
            Config.JWT_SECRET_KEY,
            algorithm='HS256'
        )
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Handle user logout"""
    response = make_response(jsonify({'success': True, 'message': 'Logged out successfully'}))
    response.set_cookie('token', '', expires=0)
    return response


# ==================== PROTECTED ROUTES ====================

@app.route('/dashboard')
@token_required
def dashboard(current_user):
    """Dashboard page - requires authentication"""
    return render_template('dashboard.html', user=current_user.to_dict())


@app.route('/house-predictor')
@token_required
def house_predictor_page(current_user):
    """House predictor page - requires authentication"""
    return render_template('house_predictor.html', user=current_user.to_dict())


@app.route('/diabetes-predictor')
@token_required
def diabetes_predictor_page(current_user):
    """Diabetes predictor page - requires authentication"""
    return render_template('diabetes_predictor.html', user=current_user.to_dict())


@app.route('/history')
@token_required
def history_page(current_user):
    """History page - requires authentication"""
    return render_template('history.html', user=current_user.to_dict())


@app.route('/settings')
@token_required
def settings_page(current_user):
    """Settings page - requires authentication"""
    return render_template('settings.html', user=current_user.to_dict())


# ==================== PREDICTION API ====================

@app.route('/api/predict/house', methods=['POST'])
@token_required
def predict_house(current_user):
    """Handle house price prediction"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'SquareFootage' not in data or 'Bedrooms' not in data or 'Location' not in data:
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Create input data dictionary
        input_data = {col: 0 for col in MODEL_COLUMNS}
        
        # Update with form data
        input_data['SquareFootage'] = float(data['SquareFootage'])
        input_data['Bedrooms'] = int(data['Bedrooms'])
        
        # Handle location (One-Hot Encoding)
        selected_location = data['Location']
        location_column = f"Location_{selected_location}"
        
        if location_column in input_data:
            input_data[location_column] = 1
        
        # Convert to DataFrame
        df_to_predict = pd.DataFrame([input_data], columns=MODEL_COLUMNS)
        
        # Make prediction
        prediction = model.predict(df_to_predict)
        output_price = float(prediction[0])
        
        # Save prediction to database
        prediction_record = Prediction.create_prediction(
            user_id=str(current_user._id),
            prediction_type='house',
            input_data={
                'SquareFootage': data['SquareFootage'],
                'Bedrooms': data['Bedrooms'],
                'Location': data['Location']
            },
            predicted_value=output_price
        )
        
        return jsonify({
            'success': True,
            'prediction': output_price,
            'formatted_price': f'LKR {output_price:,.2f}',
            'prediction_id': str(prediction_record._id)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/predict/diabetes', methods=['POST'])
@token_required
def predict_diabetes(current_user):
    """Handle diabetes prediction"""
    try:
        data = request.get_json()
        
        if not data or not diabetes_model or not diabetes_scaler:
            return jsonify({'success': False, 'message': 'Model not available'}), 400
        
        # Create input data in the correct order
        input_values = []
        for col in DIABETES_COLUMNS:
            if col not in data:
                return jsonify({'success': False, 'message': f'Missing field: {col}'}), 400
            input_values.append(float(data[col]))
        
        # Create DataFrame
        df_to_predict = pd.DataFrame([input_values], columns=DIABETES_COLUMNS)
        
        # Scale the data
        scaled_data = diabetes_scaler.transform(df_to_predict)
        
        # Make prediction
        prediction = diabetes_model.predict(scaled_data)
        prediction_proba = diabetes_model.predict_proba(scaled_data)
        
        result_value = int(prediction[0])
        
        # Map prediction to readable result
        result_map = {
            0: 'No Diabetes',
            1: 'Prediabetes',
            2: 'Diabetes'
        }
        result_text = result_map.get(result_value, 'Unknown')
        
        # Get probability for the predicted class
        confidence = float(prediction_proba[0][result_value]) * 100
        
        # Save prediction to database
        prediction_record = Prediction.create_prediction(
            user_id=str(current_user._id),
            prediction_type='diabetes',
            input_data=data,
            predicted_value=result_value,
            metadata={
                'result_text': result_text,
                'confidence': confidence,
                'probabilities': {
                    'no_diabetes': float(prediction_proba[0][0]) * 100,
                    'prediabetes': float(prediction_proba[0][1]) * 100,
                    'diabetes': float(prediction_proba[0][2]) * 100
                }
            }
        )
        
        return jsonify({
            'success': True,
            'prediction': result_value,
            'result': result_text,
            'confidence': confidence,
            'probabilities': {
                'no_diabetes': float(prediction_proba[0][0]) * 100,
                'prediabetes': float(prediction_proba[0][1]) * 100,
                'diabetes': float(prediction_proba[0][2]) * 100
            },
            'prediction_id': str(prediction_record._id)
        }), 200
        
    except Exception as e:
        print(f"Error in diabetes prediction: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== USER API ROUTES ====================

@app.route('/api/user/predictions', methods=['GET'])
@token_required
def get_predictions(current_user):
    """Get user's prediction history"""
    try:
        limit = request.args.get('limit', type=int)
        skip = request.args.get('skip', 0, type=int)
        
        predictions = Prediction.get_user_predictions(str(current_user._id), limit=limit, skip=skip)
        total_count = Prediction.get_user_prediction_count(str(current_user._id))
        
        return jsonify({
            'success': True,
            'predictions': [pred.to_dict() for pred in predictions],
            'total_count': total_count
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/user/stats', methods=['GET'])
@token_required
def get_user_stats(current_user):
    """Get user statistics"""
    try:
        total_predictions = Prediction.get_user_prediction_count(str(current_user._id))
        
        # Get this month's predictions
        db = Database.get_db()
        from datetime import datetime
        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_count = db.predictions.count_documents({
            'user_id': str(current_user._id),
            'created_at': {'$gte': start_of_month}
        })
        
        return jsonify({
            'success': True,
            'stats': {
                'total_predictions': total_predictions,
                'month_predictions': month_count
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/user/update', methods=['PUT'])
@token_required
def update_user(current_user):
    """Update user profile"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({'success': False, 'message': 'Name is required'}), 400
        
        new_name = data['name'].strip()
        
        if not new_name:
            return jsonify({'success': False, 'message': 'Name cannot be empty'}), 400
        
        current_user.update_name(new_name)
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': current_user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/user/delete', methods=['DELETE'])
@token_required
def delete_user_account(current_user):
    """Delete user account and all associated data"""
    try:
        # Delete all user predictions
        Prediction.delete_user_predictions(str(current_user._id))
        
        # Delete user account
        User.delete_user(current_user._id)
        
        response = make_response(jsonify({
            'success': True,
            'message': 'Account deleted successfully'
        }))
        
        # Clear cookie
        response.set_cookie('token', '', expires=0)
        
        return response, 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


@app.route('/favicon.ico')
def favicon():
    """Handle favicon requests"""
    return '', 204  # No content


# ==================== APP RUNNER ====================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)