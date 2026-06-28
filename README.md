<div align="center">

# 👁️ VigilanceAI

### Production-Grade AI Surveillance Platform for Intelligent Threat Detection & Security Analytics

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python">

<img src="https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge&logo=flask">

<img src="https://img.shields.io/badge/Streamlit-Frontend-red?style=for-the-badge&logo=streamlit">

<img src="https://img.shields.io/badge/Machine-Learning-success?style=for-the-badge">

<img src="https://img.shields.io/badge/Semantic-Search-orange?style=for-the-badge">

<img src="https://img.shields.io/badge/Vector-Database-blueviolet?style=for-the-badge">

<img src="https://img.shields.io/badge/Production-Live-success?style=for-the-badge">

<img src="https://img.shields.io/github/license/wyldex3ml-pro/VigilanceAI?style=for-the-badge">

</p>

### 🚀 AI-Powered Surveillance Platform for Real-Time Threat Analysis, Semantic Search & Intelligent Event Routing

🌐 **Live Dashboard**

https://wyldex3ml-pro-vigilanceai-dashboard-q9celx.streamlit.app

⚙️ **Backend API**

https://vigilanceai-vt78.onrender.com

</div>

---

# 📑 Table of Contents

- Overview
- Why VigilanceAI?
- Features
- Architecture
- AI Workflow
- Technology Stack
- Project Structure
- Installation
- Running the Project
- Deployment
- Skills Demonstrated
- Future Roadmap
- Screenshots
- License
- Author

---

# 📖 Overview

VigilanceAI is a production-ready Artificial Intelligence surveillance platform designed to help organizations monitor, analyze, classify, and prioritize security events using Machine Learning and Semantic Search.

Unlike traditional monitoring systems that only display alerts, VigilanceAI intelligently understands incoming events, searches similar historical incidents using vector embeddings, and assists operators through an interactive dashboard.

The project demonstrates real-world AI engineering concepts including:

- Production AI deployment
- Semantic Search
- Machine Learning
- Intelligent Event Routing
- REST API Development
- Dashboard Engineering
- Backend–Frontend Integration

---

# 🎯 Why VigilanceAI?

Modern organizations generate thousands of security events every day.

Traditional systems:

❌ Generate too many alerts

❌ Require manual investigation

❌ Lack contextual understanding

❌ Cannot prioritize intelligently

VigilanceAI solves these challenges using Artificial Intelligence.

It enables security teams to:

- Detect suspicious events faster
- Search semantically similar incidents
- Reduce investigation time
- Prioritize threats automatically
- Visualize analytics in real time

---

# ✨ Key Features

## 🔍 AI Threat Detection

Analyze surveillance events using AI-powered classification models.

---

## 🧠 Semantic Search

Search similar security incidents using vector embeddings instead of simple keyword matching.

---

## 🚨 Intelligent Event Routing

Automatically categorizes incidents based on severity and context.

---

## 📊 Interactive Dashboard

Real-time visualization built with Streamlit.

---

## 📈 Analytics

Monitor:

- Total Events
- Threat Levels
- System Metrics
- Processing Statistics

---

## 🌐 Production Deployment

Fully deployed with separated backend and frontend.

Frontend

Streamlit Cloud

Backend

Render

---

# 🏗 System Architecture

```text
                    Security Events
                           │
                           ▼
                  Flask REST Backend
                           │
         ┌─────────────────┴─────────────────┐
         ▼                                   ▼
Machine Learning Engine            Semantic Search Engine
         │                                   │
         └──────────────┬────────────────────┘
                        ▼
              Vector Database Processing
                        │
                        ▼
            Intelligent Threat Classification
                        │
                        ▼
              Streamlit Dashboard
                        │
                        ▼
                 Security Analyst
```

---

# 🤖 AI Workflow

```text
Incoming Event

↓

Data Validation

↓

Feature Extraction

↓

Machine Learning Analysis

↓

Semantic Similarity Search

↓

Threat Classification

↓

Severity Prediction

↓

Dashboard Visualization
```

---

# 🚀 Technology Stack

| Category | Technologies |
|----------|--------------|
| Language | Python |
| Backend | Flask |
| Frontend | Streamlit |
| Machine Learning | Scikit-learn |
| Search | Semantic Search |
| Database | Vector Database |
| APIs | REST API |
| Deployment | Render, Streamlit Cloud |

---

# 📂 Project Structure

```text
VigilanceAI
│
├── backend
│   ├── app.py
│   ├── api
│   ├── routes
│   ├── models
│   └── services
│
├── frontend
│   ├── dashboard.py
│   ├── pages
│   └── components
│
├── vector_database
│
├── requirements.txt
│
├── README.md
│
└── screenshots
```

---

# ⚙ Installation

Clone repository

```bash
git clone https://github.com/wyldex3ml-pro/VigilanceAI.git
```

Move inside

```bash
cd VigilanceAI
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run backend

```bash
python app.py
```

Run dashboard

```bash
streamlit run dashboard.py
```

---

# 🌐 Live Deployment

### Frontend

https://wyldex3ml-pro-vigilanceai-dashboard-q9celx.streamlit.app

### Backend

https://vigilanceai-vt78.onrender.com

---

# 📊 Skills Demonstrated

✅ Python

✅ Flask

✅ Streamlit

✅ Machine Learning

✅ Semantic Search

✅ Vector Databases

✅ REST APIs

✅ AI Dashboard Development

✅ Production Deployment

✅ Software Architecture

---

# 📈 Performance Highlights

| Metric | Value |
|---------|------|
| Architecture | Production Ready |
| Frontend | Live |
| Backend | Live |
| AI Search | Semantic |
| Dashboard | Real-time |
| Deployment | Cloud |

---

# 🚧 Challenges Solved

### Challenge

Processing large numbers of surveillance events efficiently.

### Solution

Implemented intelligent routing and semantic search to quickly identify relevant incidents.

---

### Challenge

Providing an intuitive monitoring interface.

### Solution

Developed an interactive Streamlit dashboard with real-time analytics.

---

### Challenge

Separating frontend and backend for scalability.

### Solution

Designed a modular architecture with independent deployments.

---

# 🚀 Future Roadmap

- Face Recognition
- Object Detection
- Video Analytics
- Edge AI Deployment
- Docker Support
- Kubernetes
- AWS Deployment
- Authentication
- Notification System
- Mobile Dashboard
- Multi-Camera Support

---

# 📸 Screenshots

Create a folder named

```
screenshots
```

Then add:

```
screenshots/dashboard.png

screenshots/home.png

screenshots/analytics.png

screenshots/search.png

screenshots/api.png
```

Display them like this:

```html
<h2>Dashboard</h2>

<p align="center">

<img src="screenshots/dashboard.png" width="900">

</p>

---

<h2>Threat Analytics</h2>

<p align="center">

<img src="screenshots/analytics.png" width="900">

</p>

---

<h2>Semantic Search</h2>

<p align="center">

<img src="screenshots/search.png" width="900">

</p>
```

---

# 🤝 Contributing

Contributions are welcome.

If you would like to improve VigilanceAI, fork the repository and submit a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

## Aditya Sarap

**AI Developer | ML Engineer | Generative AI Specialist | Python Automation Expert**

📍 Pune, Maharashtra, India

🔗 LinkedIn

https://linkedin.com/in/aditya-sarap

💻 GitHub

https://github.com/wyldex3ml-pro

🌐 Portfolio

https://ai-portfolio-i4cj.onrender.com

---

<div align="center">

### ⭐ If you found this project useful, consider giving it a Star!

**Building Production-Ready AI Systems**

</div>
