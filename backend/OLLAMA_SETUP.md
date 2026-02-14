# Ollama Setup Guide

## 🦙 What is Ollama?

Ollama allows you to run large language models locally on your machine. This implementation uses Ollama to generate AI-powered summaries for lead notes.

## 📥 Installation

### Windows
1. Download Ollama from: https://ollama.com/download
2. Run the installer
3. Ollama will start automatically as a service

### Verify Installation
```bash
ollama --version
```

## 🚀 Pull the Model

The application uses `phi3:mini` by default. Pull it with:

```bash
ollama pull phi3:mini
```

**Alternative models you can use:**
- `tinyllama` - Smallest, fastest (637MB)
- `llama3.2` - Larger, needs more RAM (2GB+)
- `mistral` - Good alternative
- `phi3` - Larger version

To change the model, edit `OLLAMA_MODEL` in [`ai_service.py`](file:///e:/Full-Stack%20Role%20Task/backend/services/ai_service.py#L14)

## ✅ Verify Ollama is Running

Check if Ollama is running:
```bash
curl http://localhost:11434/api/tags
```

Or visit: http://localhost:11434

## 🔧 Configuration

The AI service is configured in [`services/ai_service.py`](file:///e:/Full-Stack%20Role%20Task/backend/services/ai_service.py):

```python
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2"
```

## 🛡️ Fallback Behavior

If Ollama is not available, the service automatically falls back to simple text truncation, ensuring the application continues to work.

## 🧪 Test the Integration

1. Start Ollama (should auto-start on Windows)
2. Pull the model: `ollama pull llama3.2`
3. Start the backend: `uvicorn main:app --reload`
4. Add a note to any lead
5. The AI summary will be generated using Ollama!

## 📊 Performance

- **First request**: May take 5-10 seconds (model loading)
- **Subsequent requests**: 1-3 seconds
- **Model size**: ~2GB for llama3.2

## 🔍 Troubleshooting

**Issue: "Connection refused"**
- Ensure Ollama is running: `ollama serve`
- Check port 11434 is not blocked

**Issue: "Model not found"**
- Pull the model: `ollama pull llama3.2`
- Verify: `ollama list`

**Issue: Slow responses**
- Use a smaller model: `llama3.2:1b`
- Ensure sufficient RAM (8GB+ recommended)
