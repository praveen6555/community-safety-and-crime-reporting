# CrimeGuard AI - Crime Analysis & Predictive Risk Modeling Platform

An advanced **Django & Scikit-Learn** web application designed for law enforcement intelligence, citizen safety, and spatial crime risk forecasting.

---

## 🌟 Key Features

1. **AI Crime Risk Prediction Engine**:
   - Uses Scikit-Learn `RandomForestClassifier` pipeline.
   - Evaluates district, offense category, day of week, hour, area type, and armed threat factors.
   - Generates real-time threat index scores (0–100%), confidence metrics, citizen advisories, and police patrol directives.

2. **Interactive Crime Analytics Dashboard**:
   - Built with **Chart.js**.
   - Category breakdown doughnut charts, district activity rankings, incident severity distributions, and case status lifecycles.

3. **Geospatial Crime Hotspots & Risk Radar**:
   - Built with **Leaflet.js** and dark CartoDB tiles.
   - Color-coded risk clusters (Critical, High, Medium, Low), incident pins, and police station directories.

4. **Citizen Incident Filing & Tracking**:
   - Public complaint submission generating unique encrypted tracking IDs (`CR-XXXXXXXX`).
   - Interactive 4-stage investigation timeline tracker (Reported → Under Investigation → Patrol Dispatched → Solved).
   - Officer status and notes update console.

5. **Emergency Safety & SOS Directory**:
   - National helplines (112, 100, 1930, 1091) and district station contacts.
   - Prevention advisories for cyber fraud, night transit, and home security.

---

## 🚀 Commands to Execute

### 1. Run Migrations
```bash
python manage.py makemigrations application
python manage.py migrate
```

### 2. Seed Database & Train ML Model
```bash
python seed_data.py
```
*(This loads 9 categories, 8 districts, sample crime cases, and trains `crime_model.joblib`)*

### 3. Start the Development Server
```bash
python manage.py runserver
```

### 4. Access the Application
- **Main Web Portal**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Analytics Dashboard**: [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)
- **AI Risk Predictor**: [http://127.0.0.1:8000/predict/](http://127.0.0.1:8000/predict/)
- **Hotspot Map**: [http://127.0.0.1:8000/map/](http://127.0.0.1:8000/map/)
- **File Incident**: [http://127.0.0.1:8000/report/](http://127.0.0.1:8000/report/)
- **Track Case**: [http://127.0.0.1:8000/track/](http://127.0.0.1:8000/track/)
- **Django Admin Portal**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
  - **Username**: `admin`
  - **Password**: `admin123`

---

## 🧪 Run Automated Tests
```bash
python manage.py test application
```
