# 🌐 InSightMate: AI-Powered News & Job Recommendations

**InSightMate** is an AI-powered recommendation engine that delivers personalized **news articles** and **job openings** based on user interests. It integrates **Groq’s LLaMA-3 model** for contextual explanations, **NewsData API** for real-time news, **Internshala** for job listings, and a polished **Streamlit frontend** for seamless interaction.

---

## ✨ Features

- 🔍 **Search any topic** (e.g., AI, Marketing, Design)
- 📰 Fetch **latest news articles** from NewsData API
- 💼 Discover **strictly filtered job openings** from Internshala based on exact user input
- 🤖 **AI-generated explanations** for each recommendation using Groq LLaMA-3
- 🔄 **Pagination** for easy navigation
- 📊 **Search analytics** (SQLite backend)
- 📚 **Search history** in the sidebar
- 🎨 **Clean, classy UI** with clear sections and icons

---

## 🛠️ Technologies Used

- **Backend API:** FastAPI, HTTPX, BeautifulSoup, SQLite
- **AI Integration:** Groq LLaMA-3 (OpenAI-compatible API)
- **News Source:** NewsData.io
- **Jobs Source:** Internshala (via scraping)
- **Frontend:** Streamlit
- **DevOps:** dotenv, uvicorn

---

## 📦 Project Structure
```
InSightMate/
│
├── .env # API keys & configuration (user-provided)
├── analytics.db # SQLite DB for search analytics
├── groq_llm.py # Groq API integration (batched explanations)
├── main.py # FastAPI backend server
├── recommend.py # News & Jobs fetching + filtering logic
├── requirements.txt # Python dependencies
├── streamlit_app.py # Streamlit frontend (user interface)
└── utils.py # Logging & analytics helpers
```

---

## ⚙️ Setup Instructions

### 1 Clone the Repository
```bash
git clone https://github.com/Ujjwal-Bajpayee/InSightMate.git
cd InSightMate
```

### 2 Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
pip install -r requirements.txt  
```

### 3 Configure .env File
- GROQ_API_KEY=your_groq_api_key
- NEWSDATA_API_KEY=your_newsdata_api_key
- API_BACKEND_URL=http://localhost:8000
- DEFAULT_COUNTRY=in
- DEFAULT_LANGUAGE=en

### 4 Run the Backend API
```bash
uvicorn main:app --reload
```

### 5 Run the Frontend (Streamlit)
```bash
streamlit run streamlit_app.py
```
---

## 🌟 Usage
- Enter a topic of interest in the sidebar (e.g., "AI", "Marketing").
- Click the Get Recommendations button.
- Browse the News Articles and Job Openings sections, each with AI-powered explanations.
- Use the Page Number control in the sidebar to navigate between result pages.
- See your Search History in the sidebar, with the last five queries for quick access.

## 📊 Analytics
- User search queries are automatically logged into a local SQLite database (analytics.db).

