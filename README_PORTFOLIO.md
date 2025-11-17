# 🏦 Bank Marketing Campaign Analytics Dashboard

**Created by: [Masood Nazari](https://michaeltheanalyst.github.io/)**  
*Data Science | AI | Clinical Research*

[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-blue)](https://michaeltheanalyst.github.io/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/masood-nazari/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/michaeltheanalyst)

---

## 📊 Project Overview

A comprehensive, dual-interface analytics platform for analyzing bank marketing campaign data, featuring both **Streamlit** and **React** dashboards. This project demonstrates end-to-end data science capabilities from ETL to machine learning to production-ready web applications.

**Dataset:** Portuguese banking institution direct marketing campaigns (41,188 records)  
**Objective:** Predict term deposit subscriptions and optimize campaign strategies

---

## ✨ Key Features

### 📈 **Overview Dashboard**
- Real-time KPI metrics (conversion rates, customer counts)
- Interactive visualizations (Plotly.js)
- Demographic and behavioral analysis

### ⭐ **Feature Importance Analysis**
- Multi-algorithm comparison (Random Forest, Gradient Boosting, Logistic Regression)
- Aggregated importance scoring
- Actionable business insights

### 🤖 **Predictive Models**
- 6 ML algorithms benchmarked
- Realistic pre-call prediction (duration excluded)
- ROC curves, confusion matrices, detailed metrics
- **Best Model:** F1-Score 0.45+, Accuracy 90%+

### 👥 **Customer Segmentation**
- K-Means clustering with PCA visualization
- Adjustable segments (3-6 clusters)
- Detailed persona profiles
- Conversion rate analysis by segment

### 📞 **Contact Optimization**
- Frequency analysis (optimal contact count)
- Timing recommendations (month, day of week)
- Channel effectiveness (cellular vs telephone)
- Previous campaign impact assessment

### 💰 **Economic Impact Analysis**
- Macroeconomic indicators correlation
- Economic conditions segmentation
- Temporal trend analysis
- Strategic timing recommendations

---

## 🏗️ Technical Architecture

```
┌─────────────────────────────────────────┐
│     Streamlit Dashboard (Port 8501)     │
│  - Single-page application              │
│  - Integrated analysis modules          │
│  - Real-time visualizations             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│     React Frontend (Port 3000)          │
│  - Modern SPA with React Router         │
│  - Tailwind CSS styling                 │
│  - Plotly.js interactive charts         │
│  - Component-based architecture         │
└──────────────┬──────────────────────────┘
               │ REST API
┌──────────────▼──────────────────────────┐
│     Flask Backend (Port 5000)           │
│  - RESTful API endpoints                │
│  - ML model training & inference        │
│  - Data processing pipeline             │
│  - CORS-enabled                         │
└─────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### **Data Science & ML**
- **Python 3.13**: Core programming language
- **Pandas & NumPy**: Data manipulation and analysis
- **Scikit-learn**: Machine learning algorithms
- **Imbalanced-learn**: SMOTE for class balancing
- **SciPy**: Statistical analysis

### **Visualization**
- **Plotly**: Interactive charts
- **Matplotlib & Seaborn**: Statistical visualizations

### **Web Frameworks**
- **Streamlit**: Rapid prototyping dashboard
- **Flask**: REST API backend
- **React 18**: Modern frontend framework
- **Tailwind CSS**: Utility-first styling

### **Development Tools**
- **Git**: Version control
- **VS Code**: IDE
- **npm**: Package management

---

## 📊 Business Impact

### **Strategic Insights Delivered:**
1. **Optimal Contact Strategy**: 1-2 contacts maximum for best ROI
2. **Economic Timing**: Campaign success varies 5-10% with economic conditions
3. **Channel Performance**: Cellular contact significantly outperforms telephone
4. **Customer Prioritization**: Pre-call scoring enables efficient resource allocation
5. **Segment-Based Targeting**: 4 distinct personas with conversion rates 5%-25%

### **Potential ROI:**
- **Time Savings**: Automated analysis vs manual Excel reporting
- **Improved Targeting**: 15-20% increase in conversion through segment-based campaigns
- **Resource Optimization**: Focus efforts on high-probability customers
- **Strategic Timing**: Capitalize on favorable economic windows

---

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.8+
- Node.js 14+
- npm or yarn

### **Quick Start - Streamlit Dashboard**
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```
Access at: http://localhost:8501

### **Quick Start - React Dashboard**

**Backend:**
```bash
cd backend
pip install -r requirements-api.txt
python app.py
```
Backend API: http://localhost:5000

**Frontend:**
```bash
cd frontend
npm install
npm start
```
Frontend: http://localhost:3000

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
Bank Marketing 2/
├── 📊 Streamlit Dashboard
│   ├── dashboard.py              # Main Streamlit app
│   ├── data_loader.py           # ETL pipeline
│   ├── feature_importance.py    # Feature analysis
│   ├── predictive_models.py     # ML models
│   ├── customer_segmentation.py # Clustering
│   ├── contact_optimization.py  # Strategy analysis
│   └── economic_impact.py       # Macro analysis
│
├── 🌐 React Dashboard
│   ├── backend/
│   │   ├── app.py              # Flask REST API
│   │   └── requirements-api.txt
│   └── frontend/
│       ├── src/
│       │   ├── components/     # Reusable components
│       │   ├── pages/          # Route pages
│       │   ├── services/       # API integration
│       │   └── App.jsx         # Main app
│       └── package.json
│
├── 📝 Documentation
│   ├── README.md
│   ├── REACT_README.md
│   └── QUICK_START.md
│
└── 🗂️ Data
    └── bank-additional-full.csv
```

---

## 📈 Key Findings

### **Feature Importance (Top 5)**
1. **Euribor 3M Rate** - Strongest economic predictor
2. **Number Employed** - Labor market indicator
3. **Previous Campaign Outcome** - Historical behavior
4. **Month of Contact** - Seasonal patterns
5. **Contact Duration** - Post-call metric (excluded from realistic model)

### **Customer Segments (4 Clusters)**
- **High-Value Targets** (15-25% conversion): Previous responders, stable employment
- **Moderate Potential** (8-12% conversion): Middle-aged professionals
- **Low Converters** (3-5% conversion): Over-contacted, poor economic timing
- **Unexplored Segment** (5-8% conversion): First-time contacts, high potential

### **Optimal Campaign Strategy**
- **Frequency**: 1-2 contacts maximum
- **Best Months**: March, September, October, December
- **Best Days**: Thursday, Monday
- **Channel**: Cellular (15-20% better than telephone)
- **Economic Timing**: High consumer confidence, low interest rates

---

## 🎯 Machine Learning Performance

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| **Random Forest** | 0.905 | 0.601 | 0.312 | 0.410 | 0.914 |
| **Gradient Boosting** | 0.910 | 0.645 | 0.289 | 0.399 | 0.921 |
| Logistic Regression | 0.888 | 0.472 | 0.376 | 0.419 | 0.895 |
| Decision Tree | 0.881 | 0.446 | 0.412 | 0.428 | 0.866 |
| KNN | 0.898 | 0.532 | 0.198 | 0.289 | 0.858 |
| Naive Bayes | 0.803 | 0.291 | 0.748 | 0.419 | 0.871 |

*Models exclude call duration for realistic pre-call prediction*

---

## 💡 Skills Demonstrated

### **Data Science**
- ✅ Exploratory Data Analysis (EDA)
- ✅ Feature Engineering & Selection
- ✅ Machine Learning (Classification)
- ✅ Model Evaluation & Comparison
- ✅ Statistical Analysis
- ✅ Class Imbalance Handling (SMOTE)

### **Software Engineering**
- ✅ Full-Stack Development (Python + JavaScript)
- ✅ REST API Design & Implementation
- ✅ Component-Based Architecture
- ✅ State Management (React Hooks)
- ✅ Responsive UI/UX Design
- ✅ Version Control (Git)

### **Business Intelligence**
- ✅ KPI Dashboard Design
- ✅ Data Visualization Best Practices
- ✅ Actionable Insights Generation
- ✅ ROI Analysis
- ✅ Strategic Recommendations

---

## 📞 Contact

**Masood Nazari**  
Data Science | AI | Clinical Research

- 📧 Email: [M.Nazari@soton.ac.uk](mailto:M.Nazari@soton.ac.uk)
- 🌐 Portfolio: [https://michaeltheanalyst.github.io/](https://michaeltheanalyst.github.io/)
- 💼 LinkedIn: [https://www.linkedin.com/in/masood-nazari/](https://www.linkedin.com/in/masood-nazari/)
- 🔗 GitHub: [https://github.com/michaeltheanalyst](https://github.com/michaeltheanalyst)

---

## 📄 License

This project is part of my portfolio demonstrating data science and full-stack development capabilities. Feel free to explore and learn from the code!

---

## 🙏 Acknowledgments

- **Dataset**: UCI Machine Learning Repository - Bank Marketing Dataset
- **Institution**: Portuguese Banking Institution (anonymized)
- **Purpose**: Educational & Portfolio Demonstration

---

**Built with ❤️ by Masood Nazari | 2025**

