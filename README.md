# 🏦 Bank Marketing Analytics Dashboard

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Created by [Masood Nazari](https://michaeltheanalyst.github.io/)**  
*Business Intelligence Analyst | Data Science | AI | Clinical Research*

[🌐 Portfolio](https://michaeltheanalyst.github.io/) | [💼 LinkedIn](https://www.linkedin.com/in/masood-nazari/) | [📧 Email](mailto:M.Nazari@soton.ac.uk)

---

## 📊 Project Overview

A comprehensive **dual-interface analytics platform** for analyzing Portuguese bank marketing campaign data. This project showcases end-to-end data science capabilities from ETL to machine learning to production-ready web applications, featuring both **Streamlit** and **React** dashboards.

**Dataset:** 41,188 customer records from direct marketing campaigns (phone calls)  
**Objective:** Predict term deposit subscriptions and optimize campaign strategies  
**Tech Stack:** Python (Flask + Scikit-learn) + React + Tailwind CSS + Plotly

---

## ✨ Key Features

### 📈 **Dual Dashboard Interfaces**
- **Streamlit Dashboard** - Rapid prototyping with Python-only solution
- **React Dashboard** - Production-ready with premium UI/UX and Flask API backend

### 🤖 **Machine Learning**
- **6 ML Algorithms** - Random Forest, Gradient Boosting, Logistic Regression, Decision Tree, KNN, Naive Bayes
- **Realistic Pre-Call Predictions** - Models exclude call duration for deployment-ready scoring
- **SMOTE Class Balancing** - Handle imbalanced target variable
- **Comprehensive Metrics** - ROC curves, confusion matrices, precision-recall analysis

### 👥 **Customer Segmentation**
- **K-Means Clustering** - Identify 3-6 customer personas
- **PCA Visualization** - 2D projection of segments
- **Detailed Profiles** - Demographics, behavior, conversion rates per segment

### 📞 **Contact Optimization**
- **Frequency Analysis** - Optimal number of contacts (1-2 maximum)
- **Timing Recommendations** - Best months and days for contact
- **Channel Effectiveness** - Cellular vs telephone performance
- **Campaign Fatigue Detection** - Identify diminishing returns

### 💰 **Economic Impact Analysis**
- **Macroeconomic Correlations** - Employment rate, consumer confidence, Euribor rate
- **Economic Conditions Segmentation** - Favorable vs unfavorable timing
- **Temporal Trends** - Monthly economic indicator tracking
- **Strategic Recommendations** - When to scale campaigns up or down

### ⭐ **Feature Importance**
- **Multi-Algorithm Comparison** - Random Forest, Gradient Boosting, Logistic Regression
- **Aggregated Scoring** - Consensus feature importance
- **Actionable Insights** - Business-focused interpretations

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│     Streamlit Dashboard (Port 8501)     │
│  - Single-page application              │
│  - Integrated analysis modules          │
│  - Python-only solution                 │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│     React Frontend (Port 3000)          │
│  - Modern SPA with React Router         │
│  - Premium UI with Tailwind CSS         │
│  - Plotly.js interactive charts         │
│  - Dark sidebar, glass morphism         │
└──────────────┬──────────────────────────┘
               │ REST API (JSON)
┌──────────────▼──────────────────────────┐
│     Flask Backend (Port 5000)           │
│  - 7 REST API Endpoints                 │
│  - ML Model Training & Inference        │
│  - Data Processing Pipeline             │
│  - CORS-Enabled                         │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│    Data: bank-additional-full.csv       │
│    41,188 records                       │
└─────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+ (for React dashboard)
- npm or yarn

### **Option 1: Streamlit Dashboard** (Fastest)

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run dashboard.py
```

Access at: **http://localhost:8501**

### **Option 2: React Dashboard** (Production-Ready)

#### Backend:
```bash
cd backend
pip install -r requirements-api.txt
python app.py
```
Backend API: **http://localhost:5000**

#### Frontend (new terminal):
```bash
cd frontend
npm install
npm start
```
Frontend: **http://localhost:3000**

### **One-Click Launch (Windows)**
```bash
# Streamlit
run_dashboard.bat

# React (both servers)
start-all.bat
```

---

## 📁 Project Structure

```
bank-marketing-analytics-dashboard/
├── 📊 Streamlit Dashboard
│   ├── dashboard.py              # Main Streamlit app
│   ├── data_loader.py           # ETL pipeline
│   ├── feature_importance.py    # Feature analysis
│   ├── predictive_models.py     # ML models (6 algorithms)
│   ├── customer_segmentation.py # K-Means clustering
│   ├── contact_optimization.py  # Strategy analysis
│   └── economic_impact.py       # Economic correlations
│
├── 🌐 React Dashboard
│   ├── backend/
│   │   ├── app.py              # Flask REST API
│   │   └── requirements-api.txt
│   └── frontend/
│       ├── src/
│       │   ├── components/     # Layout, Cards, Spinner
│       │   ├── pages/          # 6 analysis pages
│       │   ├── services/       # API integration
│       │   └── App.jsx         # Main app with routing
│       ├── package.json
│       └── tailwind.config.js
│
├── 📝 Documentation
│   ├── README.md
│   ├── REACT_README.md
│   ├── README_PORTFOLIO.md
│   └── QUICK_START.md
│
├── 🚀 Launchers
│   ├── run_dashboard.bat        # Streamlit launcher
│   ├── start-backend.bat        # Flask API launcher
│   ├── start-frontend.bat       # React launcher
│   └── start-all.bat            # Launch both servers
│
└── 📊 Data
    └── bank-additional-full.csv
```

---

## 🎯 Business Insights Delivered

### **Campaign Optimization**
- ✅ **Optimal Contact Frequency:** 1-2 contacts maximum (diminishing returns after 3+)
- ✅ **Best Months:** March, September, October, December
- ✅ **Best Days:** Thursday and Monday
- ✅ **Channel Performance:** Cellular contact 15-20% better than telephone

### **Customer Segmentation**
- **High-Value Targets (15-25% conversion):** Previous responders, stable employment
- **Moderate Potential (8-12% conversion):** Middle-aged professionals
- **Low Converters (3-5% conversion):** Over-contacted during poor economic times
- **Unexplored Segment (5-8% conversion):** First-time contacts with potential

### **Economic Impact**
- **5-10% variance** in conversion rates based on economic conditions
- **Euribor 3M rate** and **employment levels** are strongest predictors
- **Consumer confidence** positively correlates with subscription likelihood
- **Strategic timing** during favorable economic windows maximizes ROI

---

## 📈 Machine Learning Performance

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| **Random Forest** | 90.5% | 0.601 | 0.312 | 0.410 | 0.914 |
| **Gradient Boosting** | 91.0% | 0.645 | 0.289 | 0.399 | 0.921 |
| Logistic Regression | 88.8% | 0.472 | 0.376 | 0.419 | 0.895 |
| Decision Tree | 88.1% | 0.446 | 0.412 | 0.428 | 0.866 |
| KNN | 89.8% | 0.532 | 0.198 | 0.289 | 0.858 |
| Naive Bayes | 80.3% | 0.291 | 0.748 | 0.419 | 0.871 |

**Note:** Models exclude call duration for realistic pre-call prediction

### **Top 5 Predictive Features:**
1. **Euribor 3M Rate** - Economic indicator (interest rates)
2. **Number Employed** - Labor market health
3. **Previous Campaign Outcome** - Historical behavior
4. **Month of Contact** - Seasonal patterns
5. **Employment Variation Rate** - Economic stability

---

## 🛠️ Technology Stack

### **Backend & Analysis**
- **Python 3.13** - Core programming language
- **Flask** - REST API framework
- **Pandas & NumPy** - Data manipulation
- **Scikit-learn** - Machine learning
- **Imbalanced-learn** - SMOTE for class balancing
- **SciPy** - Statistical analysis

### **Frontend**
- **React 18** - Modern JavaScript framework
- **Tailwind CSS** - Utility-first styling
- **Plotly.js** - Interactive visualizations
- **Axios** - HTTP client
- **Heroicons** - Icon library

### **Visualization**
- **Plotly** - Interactive charts
- **Matplotlib & Seaborn** - Statistical plots
- **Streamlit** - Rapid dashboard prototyping

---

## 🎨 UI/UX Features

### **Premium Design Elements**
- 🌙 **Dark Elegant Sidebar** - Professional banking aesthetic
- ✨ **Glass Morphism** - Modern frosted glass effects
- 🎭 **Gradient Accents** - Subtle color transitions
- 📊 **Premium Cards** - Soft shadows with hover animations
- 🔄 **Smooth Transitions** - Professional micro-interactions
- 📱 **Responsive Design** - Works on desktop and tablet

### **Typography**
- **Display Font:** Poppins (headings)
- **Body Font:** Inter (content)
- **Professional Hierarchy** - Clear visual structure

---

## 💡 Skills Demonstrated

### **Data Science**
- ✅ Exploratory Data Analysis (EDA)
- ✅ Feature Engineering & Selection
- ✅ Machine Learning (6 classification algorithms)
- ✅ Model Evaluation & Comparison
- ✅ Statistical Analysis & Hypothesis Testing
- ✅ Class Imbalance Handling (SMOTE)
- ✅ Unsupervised Learning (K-Means clustering)

### **Software Engineering**
- ✅ Full-Stack Development (Python + JavaScript)
- ✅ REST API Design & Implementation
- ✅ Component-Based Architecture (React)
- ✅ State Management (React Hooks)
- ✅ Responsive UI/UX Design
- ✅ Version Control (Git & GitHub)
- ✅ Code Organization & Documentation

### **Business Intelligence**
- ✅ KPI Dashboard Design
- ✅ Data Storytelling & Visualization
- ✅ Actionable Insights Generation
- ✅ ROI Analysis & Business Impact
- ✅ Strategic Recommendations

---

## 📊 Dataset Information

**Source:** UCI Machine Learning Repository - Bank Marketing Dataset  
**Institution:** Portuguese Banking Institution (anonymized)  
**Records:** 41,188 customers  
**Features:** 20 attributes (demographic, behavioral, economic)  
**Target:** Binary classification (term deposit subscription: yes/no)  
**Class Distribution:** Imbalanced (~11% positive class)

**Attribute Categories:**
- **Demographics:** Age, job, marital status, education
- **Financial:** Credit default, housing loan, personal loan
- **Campaign:** Contact type, month, day of week, number of contacts
- **Economic:** Employment variation rate, consumer price index, consumer confidence, Euribor 3M rate, number of employees

---

## 🎯 Potential Business Impact

### **Estimated ROI:**
- **15-20% increase** in conversion through segment-based targeting
- **30-40% time savings** through automated analysis vs manual Excel
- **Improved resource allocation** by prioritizing high-probability customers
- **Strategic campaign timing** during favorable economic windows
- **Reduced customer fatigue** by limiting contacts to optimal frequency

### **Operational Benefits:**
- Pre-call customer scoring for prioritization
- Real-time campaign performance monitoring
- Data-driven decision making
- Reduced manual reporting overhead
- Actionable insights for campaign managers

---

## 🤝 Contributing

This is a portfolio project showcasing data science and full-stack development capabilities. While it's primarily for demonstration purposes, feedback and suggestions are welcome!

### **Issues**
Feel free to open issues for:
- Bug reports
- Feature suggestions
- Questions about implementation
- Collaboration opportunities

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 📞 Contact

**Masood Nazari**  
*Business Intelligence Analyst | Data Science | AI | Clinical Research*

- 📧 **Email:** [M.Nazari@soton.ac.uk](mailto:M.Nazari@soton.ac.uk)
- 🌐 **Portfolio:** [https://michaeltheanalyst.github.io/](https://michaeltheanalyst.github.io/)
- 💼 **LinkedIn:** [linkedin.com/in/masood-nazari](https://www.linkedin.com/in/masood-nazari/)
- 🔗 **GitHub:** [github.com/michaeltheanalyst](https://github.com/michaeltheanalyst)

---

## 🙏 Acknowledgments

- **Dataset:** UCI Machine Learning Repository - Bank Marketing Dataset
- **Research:** S. Moro, P. Cortez and P. Rita. A Data-Driven Approach to Predict the Success of Bank Telemarketing. Decision Support Systems, Elsevier, 62:22-31, June 2014
- **Institution:** Portuguese Banking Institution
- **Purpose:** Educational & Portfolio Demonstration
- **University:** University of Southampton

---

## 📚 Documentation

- **[REACT_README.md](REACT_README.md)** - Detailed React dashboard documentation
- **[QUICK_START.md](QUICK_START.md)** - Quick start guide
- **[README_PORTFOLIO.md](README_PORTFOLIO.md)** - Portfolio-focused documentation

---

**⭐ If you found this project helpful or interesting, please star the repository!**

**Built with ❤️ by Masood Nazari | 2025**
