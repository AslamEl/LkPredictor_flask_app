# 🎯 LkPredictor - AI-Powered Prediction Platform

A comprehensive machine learning web application that provides intelligent predictions for various domains. Currently featuring house price predictions and diabetes risk assessment for Sri Lanka, with more predictors coming soon!

🌐 **Live Demo**: [https://your-app-name.herokuapp.com](https://your-app-name.herokuapp.com)  
📦 **Repository**: [https://github.com/AslamEl/LkPredictor_flask_app.git](https://github.com/AslamEl/LkPredictor_flask_app.git)

---

## 📋 Table of Contents

- [Features](#features)
- [Current Predictors](#current-predictors)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Future Predictors](#future-predictors)
- [Contributing](#contributing)

---

## ✨ Features

- 🤖 **Multiple AI Predictors** - House prices, diabetes risk, and more coming soon
- 🔐 **Secure Authentication** - JWT-based user authentication system
- 📊 **Prediction History** - Track all your predictions with timestamps
- 📱 **Responsive Design** - Beautiful UI works on all devices
- 📸 **Share Results** - Download predictions as images or share via text
- 🎨 **Modern Interface** - Built with Tailwind CSS and smooth animations
- 💾 **Data Persistence** - MongoDB database for user data and predictions

---

## 🚀 Current Predictors

### 1. 🏠 House Price Predictor
Predicts residential property prices in Sri Lanka based on:
- Square footage
- Number of bedrooms
- Location (Urban, Suburb, Rural)

**Model**: Random Forest Regressor  
**Accuracy**: R² > 0.90  
**Dataset**: Kaggle - Sri Lanka House Prices Dataset

### 2. 🩺 Diabetes Risk Predictor
Assesses diabetes risk using 21 CDC BRFSS health indicators:
- Blood pressure and cholesterol levels
- BMI and lifestyle factors
- Medical history
- Demographics

**Model**: Random Forest Classifier  
**Dataset**: Kaggle - CDC BRFSS 2015 (21 health indicators)

### 3. 🚗 Car Price Predictor
**Status**: Coming Soon  
Vehicle price predictions based on make, model, year, and condition.

---

## 🛠️ Tech Stack

**Backend**
- Python 3.11
- Flask 3.0.0
- scikit-learn 1.3.2
- joblib for model serialization

**Frontend**
- HTML5, CSS3, JavaScript
- Tailwind CSS
- Font Awesome icons
- html2canvas for image generation

**Database**
- MongoDB (local/Atlas)
- PyMongo 4.6.1

**Authentication**
- JWT (PyJWT 2.8.0)
- Secure token-based sessions

**Deployment**
- Heroku (Platform as a Service)
- Gunicorn WSGI server

---

## 📦 Installation

### Prerequisites
- Python 3.11+
- MongoDB (local or Atlas)
- Git

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/AslamEl/LkPredictor_flask_app.git
cd LkPredictor_flask_app
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
MONGO_URI=mongodb://localhost:27017/lkpredictor
MODEL_PATH=sri_lanka_model.pkl
MODEL_COLUMNS_PATH=model_columns.json
DIABETES_MODEL_PATH=diabetes_model.pkl
DIABETES_SCALER_PATH=diabetes_scaler.pkl
DIABETES_COLUMNS_PATH=diabetes_model_columns.json
```

To generate secure keys:
```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32)); print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
```

5. **Run the application**
```bash
python app.py
```

6. **Open browser**
```
http://localhost:5000
```

---

## 💻 Usage

### For Users

1. **Sign Up**: Create an account with email and password
2. **Login**: Access your dashboard
3. **Make Predictions**: 
   - Choose a predictor (House Price or Diabetes Risk)
   - Fill in the required information
   - Get instant AI-powered predictions
4. **View History**: Check all your past predictions
5. **Share Results**: Download prediction results as images

### For Developers

**Training New Models**: See Jupyter notebooks in project root
- `srilanka_house_predictor.ipynb` - House price model training
- `diabets_predictor.ipynb` - Diabetes model training

**Adding New Predictors**:
1. Train your model (use scikit-learn or similar)
2. Save model as `.pkl` file using joblib
3. Add model paths to `.env` and `config.py`
4. Create prediction route in `app.py`
5. Design frontend template in `templates/`
6. Update dashboard with new predictor card

---

## 📁 Project Structure

```
srilanka house predictor/
│
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── database.py                     # MongoDB connection
├── auth.py                         # JWT authentication
│
├── models/                         # Data models
│   ├── user.py                     # User model
│   └── prediction.py               # Prediction model
│
├── templates/                      # HTML templates
│   ├── landing.html                # Landing page
│   ├── dashboard.html              # User dashboard
│   ├── house_predictor.html        # House price predictor
│   ├── diabetes_predictor.html     # Diabetes risk predictor
│   ├── history.html                # Prediction history
│   └── settings.html               # User settings
│
├── *.pkl                           # Trained ML models
├── *.json                          # Model metadata
├── requirements.txt                # Python dependencies
├── Procfile                        # Heroku process file
├── runtime.txt                     # Python version for Heroku
├── .env                            # Environment variables (not in git)
├── .gitignore                      # Git ignore rules
│
└── notebooks/
    ├── srilanka_house_predictor.ipynb
    └── diabets_predictor.ipynb
```

---

## 🚀 Deployment

### Heroku Deployment

This application is deployed on Heroku. To deploy your own instance:

**Prerequisites**
- Heroku account
- Heroku CLI installed
- MongoDB Atlas account (free tier)

**Quick Deploy**

```bash
# 1. Login to Heroku
heroku login

# 2. Create new Heroku app
heroku create your-app-name

# 3. Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set JWT_SECRET_KEY="your-jwt-key"
heroku config:set MONGO_URI="your-mongodb-atlas-uri"
heroku config:set MODEL_PATH="sri_lanka_model.pkl"
heroku config:set MODEL_COLUMNS_PATH="model_columns.json"
heroku config:set DIABETES_MODEL_PATH="diabetes_model.pkl"
heroku config:set DIABETES_SCALER_PATH="diabetes_scaler.pkl"
heroku config:set DIABETES_COLUMNS_PATH="diabetes_model_columns.json"

# 4. Deploy
git push heroku main

# 5. Open your app
heroku open
```

**MongoDB Atlas Setup**
1. Create free cluster at https://www.mongodb.com/cloud/atlas
2. Create database user
3. Whitelist IP: 0.0.0.0/0 (allow from anywhere)
4. Get connection string
5. Add to Heroku config vars

---

## 🔮 Future Predictors

We're constantly expanding our prediction capabilities. Coming soon:

- 🚗 **Car Price Predictor** - Vehicle valuation based on make, model, year, and condition
- 🏢 **Commercial Property Predictor** - Business property price estimates
- 💰 **Loan Approval Predictor** - Credit risk assessment
- 📈 **Stock Price Predictor** - Market trend analysis
- 🌾 **Crop Yield Predictor** - Agricultural predictions
- ⚕️ **Disease Risk Predictor** - Additional health assessments

*Have a suggestion? [Open an issue](https://github.com/AslamEl/AWS-Projects-Challenge-01/issues)*

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/new-predictor
   ```
3. **Commit your changes**
   ```bash
   git commit -m "Add new predictor for XYZ"
   ```
4. **Push to branch**
   ```bash
   git push origin feature/new-predictor
   ```
5. **Open a Pull Request**

### Adding New Predictors

If you want to contribute a new predictor:

1. Train your model using scikit-learn or similar framework
2. Achieve good accuracy (R² > 0.85 for regression, Accuracy > 80% for classification)
3. Save model as `.pkl` file with joblib
4. Create clean, user-friendly interface
5. Write clear documentation
6. Test thoroughly before submitting PR

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Mohamed Aslam**
- GitHub: [@AslamEl](https://github.com/AslamEl)
- Project: [LkPredictor Flask App](https://github.com/AslamEl/LkPredictor_flask_app)

---

## 🙏 Acknowledgments

- **Kaggle** for providing datasets:
  - CDC BRFSS 2015 Diabetes Health Indicators Dataset
  - Sri Lanka House Prices Dataset
- scikit-learn community for machine learning tools
- Flask framework developers
- MongoDB Atlas for database hosting
- Heroku for deployment platform
- Tailwind CSS for beautiful UI components

---

## 📞 Support

For issues, questions, or suggestions:

1. Check existing [Issues](https://github.com/AslamEl/LkPredictor_flask_app/issues)
2. Open a new issue with detailed description
3. Star ⭐ the repository if you find it useful!

## 📊 Datasets

This project uses publicly available datasets from Kaggle:

1. **Sri Lanka House Prices Dataset**
   - Used for training the house price prediction model
   - Features: Square footage, bedrooms, location
   
2. **CDC BRFSS 2015 - Diabetes Health Indicators**
   - Used for diabetes risk assessment model
   - 21 health indicators from CDC Behavioral Risk Factor Surveillance System

*Note: Datasets are not included in this repository. Download from Kaggle if you want to retrain models.*

---

## 🌟 Show Your Support

Give a ⭐️ if this project helped you or you find it interesting!

---

**Built with ❤️ for Sri Lanka**

*Last Updated: October 28, 2025*
