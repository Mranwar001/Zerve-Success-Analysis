# Zerve Success Analysis: Behavioral Intelligence Engine

This project was developed for the **Zerve Open Innovation Challenge**. It provides a comprehensive behavioral analytics engine to identify and predict long-term user success based on early event patterns.

## 🚀 Features
- **Success Score Framework**: Multi-dimensional scoring across Retention, Depth, Complexity, and Velocity.
- **Behavioral Archetypes**: Automatic user segmentation (Power Builders, Curious Explorers, etc.) using K-Means.
- **Predictive Driver Analysis**: Identifying 'Aha Moment' latency as the #1 leading indicator of retention.
- **Interactive Dashboard**: A Flask-based web interface to explore data and predict user outcomes.
- **Success Prediction Tool**: A CLI utility for rapid behavioral assessment.

## 🛠️ Tech Stack
- **Python 3.14**
- **Data**: Pandas, Numpy, Scikit-Learn
- **Web**: Flask, HTML5, CSS3 (Vanilla)
- **Deployment**: Gunicorn, Procfile

## 📂 Project Structure
- `data_generator.py`: Synthetic event engine (176k+ events).
- `preprocess.py`: Sessionization and Success Score calculation.
- `features.py`: Advanced behavioral feature engineering.
- `analysis.py`: Clustering and Random Forest modeling.
- `app.py`: Flask backend for the dashboard.
- `templates/`: Dashboard UI templates.
- `success_predict.py`: CLI-based prediction tool.

## 🚀 Getting Started

### Local Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the analysis pipeline:
   ```bash
   python data_generator.py
   python preprocess.py
   python features.py
   python analysis.py
   ```
3. Launch the dashboard:
   ```bash
   python app.py
   ```
   Access at `http://127.0.0.1:5000`

## 🌐 Deployment
This project is configured for deployment on **Render** or **Railway**. 
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

---
**Developed for the Zerve Open Innovation Challenge.**
