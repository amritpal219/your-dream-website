# 🌐 ThindWorldWeb — Custom Website Order System

Built with: **HTML + CSS + JavaScript + Python (Flask)**

---

## 📁 Project Structure

```
thindworldweb/
├── static/
│   └── index.html       ← Frontend (HTML + CSS + JS)
├── uploads/             ← Uploaded files (auto-created)
├── app.py               ← Python Flask backend
├── requirements.txt     ← Python dependencies
├── render.yaml          ← Render.com deploy config
├── .env.example         ← Email config template
├── .gitignore
└── README.md
```

---

## 🚀 Local Setup

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
```

Edit `.env`:
```
EMAIL_USER=thindworld3d@gmail.com
EMAIL_PASS=xxxx xxxx xxxx xxxx
DEVELOPER_EMAIL=thindworld3d@gmail.com
```

> **Gmail App Password:** Google Account → Security → 2-Step Verification → App Passwords → Generate

### 3. Run locally
```bash
python app.py
```

Visit: `http://localhost:5000`

---

## ☁️ Deploy on Render

1. Push to GitHub
2. Go to [render.com](https://render.com) → New Web Service → Connect repo
3. Render auto-detects `render.yaml`
4. Add Environment Variables:
   - `EMAIL_USER` = thindworld3d@gmail.com
   - `EMAIL_PASS` = your Gmail App Password
5. Click **Deploy** ✅

---

## 💰 Pricing

| Option | Price |
|--------|-------|
| Plain UI | $49 |
| Glow UI | $79 |
| Custom Colors | +$15 |
| Developer Media | +$40 |
| Upload Images | +$10 |
| Upload Videos | +$15 |
| Upload Both | +$22 |
| Hosting 1 Year | $50 |
| Hosting 2 Years | $90 |
| Hosting 3 Years | $120 |
| Domain 1 Year | $15 |

To change prices, edit the `PRICES` object in `static/index.html`.
