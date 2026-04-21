# 🛡️ PhishShield AI

PhishShield AI is a **hybrid phishing detection system** that uses both:
- Rule-based detection
- Machine learning

It includes:
- Flask backend (API + model)
- Chrome extension (real-time detection)

---

## 🚀 Features

- Detect phishing URLs in real time
- Chrome extension integration
- Rule-based + ML detection
- Warning alerts for malicious sites
- Simple UI

---

## 🛠️ Tech Stack

- Python (Flask, scikit-learn)
- JavaScript (Chrome Extension)
- HTML/CSS

---

## ⚙️ Setup

### 1. Open project

cd phishshield-ai

---

### 2. Create virtual environment

python -m venv venv

---

### 3. Activate environment

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

---

### 4. Install dependencies

pip install -r requirements.txt

---

### 5. Train model

python train-model.py

---

### 6. Run backend

python app.py

Server runs on:
http://127.0.0.1:5000

---

## 🌐 Chrome Extension Setup

1. Open Chrome  
2. Go to: chrome://extensions/  
3. Enable Developer Mode  
4. Click “Load unpacked”  
5. Select `chrome-extension/`

---

## ▶️ How to Use

1. Open any website  
2. Click extension  
3. Click “Check Website”  

Result:
- ✅ Safe
- 🚨 Phishing

---

## 🧠 How It Works

1. Extension gets current URL  
2. Sends it to Flask API  
3. Backend extracts features  
4. Rule-based detection runs  
5. ML model predicts  
6. Result returned  
7. Extension shows output  

---

## ⚠️ Important

- You must run `app.py` while using extension  
- Reload extension after changes  

---

## 🔧 Troubleshooting

Extension not working:
- Make sure backend is running

No response:
- Install flask-cors
- Add CORS(app) in app.py

Model issue:
- Run train-model.py again

---

## 🚀 Future Improvements

- Deploy backend online
- Auto block phishing sites
- Improve ML accuracy
- Add blacklist API

---

## 👨‍💻 Author

Pratik S. Dabhane

---

## 🎯 Summary

PhishShield AI demonstrates how phishing detection can be built using a hybrid approach of rules and machine learning, integrated into a real-time browser extension.
