# Lead Sync + AI Notes System

A full-stack application that fetches leads from a public API, allows adding notes per lead, and generates **AI-powered summaries using Ollama** for those notes.

---

## 🚀 Tech Stack

### Backend
- **Python 3.12**
- **FastAPI** - Modern async web framework
- **Uvicorn** - ASGI server
- **Ollama (phi3:mini)** - Local LLM for AI summaries
- **JSON file persistent store** (demo storage layer)
- **Pydantic** - Data validation

### Frontend
- **Next.js 14** (App Router)
- **TypeScript**
- **React** with modern hooks
- **CSS Modules** for styling

### AI Integration
- **Ollama phi3:mini** for local LLM inference (2.2GB)
- AI summary generation (max 20 words)
- Automatic fallback if Ollama unavailable
- Swappable AI provider architecture

---

## 🧩 Features

### 1️⃣ Fetch Leads
- Fetches leads from: `https://jsonplaceholder.typicode.com/users`
- Extracts: **name**, **email**, **phone**
- Served via backend proxy (`/leads` endpoint)
- Beautiful card-based display

### 2️⃣ Add Notes
- Each lead has an "Add Notes" button
- Opens modal for note entry
- Notes are persisted in JSON file store
- Notes mapped by email (unique key)

### 3️⃣ AI Summary with Ollama 🦙
- **Generates summary using Ollama phi3:mini**
- Enforced max 20 words
- Saved alongside note
- AI service abstracted for easy provider swap
- Automatic fallback if Ollama unavailable

---

## 🛠 Setup Instructions

### Prerequisites
- Python 3.12+
- Node.js 18+
- **Ollama** ([Download here](https://ollama.com/download))

---

### 🔹 Step 1: Install Ollama

1. **Download and install Ollama** from: https://ollama.com/download
2. **Pull the model:**
   ```bash
   ollama pull phi3:mini
   ```
3. **Verify Ollama is running:**
   ```bash
   ollama list
   ```

---

### 🔹 Step 2: Backend Setup

```bash
# Create conda environment
conda create -n fullstack python=3.12
conda activate fullstack

# Install dependencies
cd backend
pip install -r requirements.txt

# Run server
uvicorn main:app --reload
```

**Backend runs on:** `http://localhost:8000`  
**Swagger Docs:** `http://localhost:8000/docs`

---

### 🔹 Step 3: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

**Frontend runs on:** `http://localhost:3000`

---

## 📡 API Endpoints

### `GET /leads`
Returns cleaned list of leads.

### `POST /notes`
Creates note with AI summary (using Ollama).

**Request:**
```json
{
  "email": "example@email.com",
  "note": "Your note text here"
}
```

**Response:**
```json
{
  "email": "example@email.com",
  "note": "Your note text here",
  "summary": "AI-generated summary (max 20 words)"
}
```

### `POST /summary`
Generates standalone summary using Ollama.

---

## 🦙 Ollama Configuration

**Current model:** `phi3:mini` (2.2GB)

**To change the model**, edit [`backend/services/ai_service.py`](backend/services/ai_service.py):
```python
OLLAMA_MODEL = "phi3:mini"  # Change to any pulled model
```

**Alternative models:**
- `tinyllama` - Smallest (637MB)
- `llama3.2` - Larger, needs more RAM
- `mistral` - Good alternative

---

## 🏗 Project Structure

```
backend/
├── main.py                 # FastAPI app with CORS
├── requirements.txt        # Python dependencies
├── models/
│   └── schemas.py         # Pydantic models
├── routes/
│   ├── leads.py           # GET /leads
│   └── notes.py           # POST /notes, POST /summary
├── services/
│   ├── leads_service.py   # External API integration
│   └── ai_service.py      # Ollama AI integration
└── storage/
    └── json_store.py      # JSON persistence

frontend/
├── src/
│   ├── app/               # Next.js pages
│   ├── components/        # React components
│   ├── lib/               # API client
│   └── types/             # TypeScript types
└── package.json
```

---

## 🧠 Design Decisions

### Backend Proxy Pattern
Leads are fetched through backend to:
- Avoid CORS issues
- Maintain clean API abstraction
- Enable future caching

### Storage Abstraction
JSON persistent store for demo simplicity.  
Storage layer is abstracted for easy replacement with SQLite/PostgreSQL.

### Service Layer Pattern
Business logic separated from route handlers for better maintainability and testability.

### AI Layer Isolation
AI logic in `ai_service.py` allows switching between providers (Ollama, OpenAI, Claude) without route changes.

---

## 📈 Scalability Considerations

If productionized:

✅ Replace JSON store with **PostgreSQL**  
✅ Add **authentication layer** (JWT)  
✅ Introduce **caching** for leads (Redis)  
✅ Add **background job queue** for AI generation (Celery)  
✅ Add **optimistic UI updates**  
✅ Add **pagination** for large lead sets  

---

## 🎨 UI Features

- **Premium gradient design** with purple-violet theme
- **Smooth animations** (hover effects, modal transitions)
- **Responsive grid layout** for leads
- **Loading states** with spinner
- **Error handling** with retry
- **Stats dashboard** showing metrics
- **AI summary** with sparkle icon ✨

---

## 🔧 Troubleshooting

**Issue: AI summaries not working**
- Ensure Ollama is running: `ollama list`
- Check model is pulled: `ollama pull phi3:mini`
- Verify port 11434 is accessible

**Issue: CORS errors**
- Backend must run on port 8000
- Frontend must run on port 3000

**Issue: Slow AI responses**
- First request loads model (5-10s)
- Subsequent requests faster (1-3s)

---

## 📚 Documentation

- **Setup Guide:** This README
- **Ollama Setup:** [`backend/OLLAMA_SETUP.md`](backend/OLLAMA_SETUP.md)
- **API Docs:** `http://localhost:8000/docs` (when backend running)
- **Testing Guide:** [`TESTING_GUIDE.md`](TESTING_GUIDE.md)

---

## ✨ Features Implemented

✅ Fetch leads from external API  
✅ Display leads in card grid  
✅ Add notes to leads  
✅ AI-powered summaries (Ollama)  
✅ Persistent storage (JSON)  
✅ Auto-generated API docs  
✅ TypeScript for type safety  
✅ Responsive design  
✅ Loading states  
✅ Error handling  
✅ Premium UI/UX  

---

Made with ❤️ using FastAPI, Next.js, and Ollama 🦙
