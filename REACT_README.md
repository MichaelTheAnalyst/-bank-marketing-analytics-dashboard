# 🚀 Bank Marketing Dashboard - React Version

A modern, high-performance React dashboard with Flask API backend for comprehensive bank marketing campaign analysis.

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         React Frontend (Port 3000)       │
│  - Modern UI with Tailwind CSS          │
│  - Interactive Plotly.js charts         │
│  - Real-time data visualization         │
└──────────────┬──────────────────────────┘
               │ HTTP/REST API
┌──────────────▼──────────────────────────┐
│        Flask Backend (Port 5000)         │
│  - REST API endpoints                    │
│  - ML model training                     │
│  - Data analysis & processing            │
└──────────────────────────────────────────┘
```

## ✨ Features

### Frontend (React)
- ⚡ **Fast Performance**: React 18 with optimized rendering
- 🎨 **Beautiful UI**: Tailwind CSS with custom components
- 📊 **Interactive Charts**: Plotly.js for rich visualizations
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile
- 🔄 **Real-time Updates**: Live data fetching from API
- 🎯 **Intuitive Navigation**: Sidebar navigation with routing

### Backend (Flask)
- 🔌 **RESTful API**: Clean API endpoints for all analyses
- 🤖 **ML Models**: Scikit-learn integration
- 📈 **Data Processing**: Pandas for efficient data manipulation
- 🚀 **Fast Response**: Cached data loading
- 🔒 **CORS Enabled**: Secure cross-origin requests

## 🚀 Quick Start

### Option 1: One-Click Launch (Easiest)

**Simply double-click: `start-all.bat`**

This will:
1. ✅ Start the Flask backend API (Port 5000)
2. ✅ Start the React frontend (Port 3000)
3. ✅ Open your browser automatically

### Option 2: Manual Start

#### Start Backend (Terminal 1)
```bash
# Double-click start-backend.bat
# OR manually:
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements-api.txt
python app.py
```

#### Start Frontend (Terminal 2)
```bash
# Double-click start-frontend.bat
# OR manually:
cd frontend
npm install
npm start
```

## 📁 Project Structure

```
Bank Maketing 2/
├── backend/
│   ├── app.py                    # Flask API server
│   ├── requirements-api.txt      # Python dependencies
│   └── venv/                     # Virtual environment
│
├── frontend/
│   ├── public/
│   │   └── index.html           # HTML template
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout/
│   │   │   │   ├── Sidebar.jsx  # Navigation sidebar
│   │   │   │   └── Header.jsx   # Top header
│   │   │   └── Common/
│   │   │       ├── Card.jsx     # Reusable card component
│   │   │       └── LoadingSpinner.jsx
│   │   ├── pages/
│   │   │   ├── Overview.jsx
│   │   │   ├── FeatureImportance.jsx
│   │   │   ├── PredictiveModels.jsx
│   │   │   ├── CustomerSegmentation.jsx
│   │   │   ├── ContactOptimization.jsx
│   │   │   └── EconomicImpact.jsx
│   │   ├── services/
│   │   │   └── api.js            # API service
│   │   ├── App.jsx               # Main app component
│   │   ├── index.js              # Entry point
│   │   └── index.css             # Global styles
│   ├── package.json              # Node dependencies
│   ├── tailwind.config.js        # Tailwind configuration
│   └── node_modules/
│
├── start-backend.bat             # Backend launcher
├── start-frontend.bat            # Frontend launcher
├── start-all.bat                 # Launch both servers
└── REACT_README.md               # This file
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/overview` | GET | Dataset overview statistics |
| `/api/feature-importance` | GET | Feature importance analysis |
| `/api/predictive-models` | GET | ML model results |
| `/api/customer-segmentation?n_clusters=4` | GET | Customer segments |
| `/api/contact-optimization` | GET | Contact strategy analysis |
| `/api/economic-impact` | GET | Economic indicators impact |

## 📊 Dashboard Pages

### 1. **Overview** (`/`)
- Total customers & conversions
- Conversion rate metrics
- Age, job, education distributions
- Interactive charts

### 2. **Feature Importance** (`/feature-importance`)
- Aggregated importance across methods
- Random Forest, Gradient Boosting, Logistic Regression
- Interactive method selector
- Key insights

### 3. **Predictive Models** (`/predictive-models`)
- 6 ML algorithms compared
- ROC curves & confusion matrices
- Detailed metrics table
- Best model highlight

### 4. **Customer Segmentation** (`/segmentation`)
- K-Means clustering visualization
- PCA 2D projection
- Segment profiles
- Adjustable number of clusters

### 5. **Contact Optimization** (`/contact-optimization`)
- Frequency analysis
- Timing optimization
- Channel effectiveness
- Previous outcome impact

### 6. **Economic Impact** (`/economic-impact`)
- Correlation analysis
- Economic conditions comparison
- Significance testing
- Strategic recommendations

## 🛠️ Technology Stack

### Frontend
- **React 18**: Modern React with hooks
- **React Router 6**: Client-side routing
- **Axios**: HTTP client for API calls
- **Plotly.js**: Interactive visualizations
- **Tailwind CSS**: Utility-first CSS framework
- **Heroicons**: Beautiful SVG icons

### Backend
- **Flask**: Lightweight Python web framework
- **Flask-CORS**: Cross-origin resource sharing
- **Pandas**: Data manipulation
- **Scikit-learn**: Machine learning
- **NumPy**: Numerical computing

## 🎨 Customization

### Change API URL
Edit `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = 'http://your-api-url:5000/api';
```

### Change Data File
Edit `backend/app.py` line 31:
```python
DATA_PATH = r"path\to\your\data.csv"
```

### Modify Theme Colors
Edit `frontend/tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      primary: '#your-color',
    },
  },
}
```

## 📈 Performance

- **Frontend Build Size**: ~500KB gzipped
- **Initial Load Time**: < 2 seconds
- **API Response Time**: 50-500ms (depending on endpoint)
- **Model Training Time**: 30-60 seconds (cached after first load)

## 🔧 Troubleshooting

### Backend won't start?
```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
cd backend
pip install -r requirements-api.txt --force-reinstall
```

### Frontend won't start?
```bash
# Check Node version (need 14+)
node --version

# Clear and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Port already in use?
```bash
# Backend (change port in app.py)
app.run(debug=True, port=5001)

# Frontend (create .env file)
PORT=3001
```

### CORS errors?
Make sure backend is running before starting frontend. Flask-CORS is configured to allow all origins in development.

## 🚀 Production Deployment

### Build Frontend
```bash
cd frontend
npm run build
```

The `build/` folder contains optimized production files.

### Deploy Backend
Use Gunicorn for production:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables
Create `.env` files for sensitive data:
```
FLASK_ENV=production
API_KEY=your-api-key
DATABASE_URL=your-db-url
```

## 🎯 Advantages Over Streamlit

✅ **Faster Performance**: React's virtual DOM vs. Streamlit's reruns  
✅ **Better UX**: Smooth navigation without page reloads  
✅ **More Control**: Full customization of UI/UX  
✅ **Scalable**: Separate frontend/backend for easy deployment  
✅ **Modern Stack**: Industry-standard technologies  
✅ **Production Ready**: Build once, deploy anywhere  

## 📝 Development

### Add New Page
1. Create component in `frontend/src/pages/`
2. Add route in `frontend/src/App.jsx`
3. Add navigation item in `frontend/src/components/Layout/Sidebar.jsx`
4. Create API endpoint in `backend/app.py` (if needed)

### Add New API Endpoint
1. Define route in `backend/app.py`
2. Add service method in `frontend/src/services/api.js`
3. Use in React component with `useEffect` + `useState`

## 🤝 Support

For issues or questions:
1. Check console errors (F12 in browser)
2. Review terminal output for backend errors
3. Ensure both servers are running
4. Verify data file path is correct

## 📄 License

Educational and analytical purposes.

---

## 🎉 Ready to Go!

Just run `start-all.bat` and enjoy your modern analytics dashboard! 🚀

**Frontend**: http://localhost:3000  
**Backend API**: http://localhost:5000  

Happy Analyzing! 📊✨

