<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776ab?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white" />
  <img src="https://img.shields.io/badge/ChromaDB-FF6F61?style=for-the-badge" />
</p>

# 📚 Study Buddy — AI-Powered Learning Assistant

**Study Buddy** is a RAG (Retrieval-Augmented Generation) web application that lets you upload PDF documents and ask questions about their content using natural language. It combines vector search with a powerful LLM to deliver accurate, context-aware answers grounded in your own study materials.

> Upload any PDF. Ask anything. Get instant, AI-generated answers — sourced directly from your documents.

---

## ✨ Features

- **PDF Upload & Processing** — Upload any PDF and have it automatically chunked, embedded, and stored in a vector database.
- **Conversational Q&A** — Ask questions in natural language and receive clear, well-explained answers.
- **RAG Pipeline** — Retrieves the most relevant document passages before generating an answer, minimizing hallucination.
- **Persistent Vector Store** — Uses ChromaDB for persistent storage so your uploaded documents survive server restarts.
- **Modern Chat UI** — A sleek, dark-themed interface with glassmorphism effects, smooth animations, and responsive design.
- **Real-time Feedback** — Visual upload progress banners, animated loading indicators, and system notifications.
- **Deploy-Ready** — Includes a `render.yaml` for one-click deployment to [Render](https://render.com).

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                  Frontend (HTML/CSS/JS)          │
│          Chat UI  ·  PDF Upload  ·  Animations   │
└────────────────────────┬────────────────────────┘
                         │  HTTP (REST)
┌────────────────────────▼────────────────────────┐
│                  FastAPI Backend                  │
│                                                  │
│  ┌──────────┐   ┌──────────────┐   ┌──────────┐ │
│  │ /upload  │   │  RAG Chain   │   │  /ask    │  │
│  │ endpoint │   │ (LangChain)  │   │ endpoint │  │
│  └────┬─────┘   └──────┬───────┘   └────┬─────┘ │
│       │                │                │        │
│  ┌────▼────────────────▼────────────────▼─────┐  │
│  │            ChromaDB (Vector Store)         │  │
│  │     + FastEmbed (all-MiniLM-L6-v2)        │  │
│  └────────────────────────────────────────────┘  │
│                        │                         │
│               ┌────────▼────────┐                │
│               │  Groq LLM API  │                 │
│               │ (Llama 3.3 70B)│                 │
│               └─────────────────┘                │
└──────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer       | Technology                                                    |
| ----------- | ------------------------------------------------------------- |
| **Backend** | Python, FastAPI, Uvicorn                                      |
| **LLM**     | Groq Cloud API (`llama-3.3-70b-versatile`)                    |
| **RAG**     | LangChain, ChromaDB, FastEmbed (`all-MiniLM-L6-v2`)          |
| **Frontend**| Vanilla HTML, CSS (glassmorphism dark theme), JavaScript      |
| **Deploy**  | Render (via `render.yaml`)                                    |

---

## 📂 Project Structure

```
rag_study_buddy/
├── backend/
│   ├── main.py              # FastAPI app, RAG chain, upload/ask endpoints
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # GROQ_API_KEY (not committed)
│   └── chroma_db/           # Persistent vector database (auto-generated)
├── frontend/
│   ├── index.html           # Chat interface markup
│   ├── style.css            # Dark-themed UI with glassmorphism
│   └── script.js            # Chat logic, upload handling, animations
├── render.yaml              # Render deployment configuration
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- A free **[Groq API Key](https://console.groq.com/keys)**

### 1. Clone the Repository

```bash
git clone https://github.com/Davidayo123/rag_study_buddy.git
cd rag_study_buddy
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file inside the `backend/` directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the Server

```bash
cd backend
uvicorn main:app --reload
```

The app will be available at **[http://127.0.0.1:8000](http://127.0.0.1:8000)**.

---

## 📖 Usage

1. **Open the app** in your browser at `http://127.0.0.1:8000`.
2. **Upload a PDF** using the upload button in the header.
3. Wait for the processing banner to confirm the document has been indexed.
4. **Ask questions** about the document in the chat input — the AI tutor will respond with context-aware answers sourced from your PDF.

---

## ☁️ Deployment (Render)

This project includes a pre-configured `render.yaml` for seamless deployment:

1. Push your code to GitHub.
2. Create a new **Web Service** on [Render](https://render.com) and connect your repo.
3. Render will auto-detect the `render.yaml` configuration.
4. Add your `GROQ_API_KEY` as an environment variable in the Render dashboard.
5. Deploy — your Study Buddy will be live!

---

## 🔑 API Endpoints

| Method | Endpoint  | Description                          | Payload                        |
| ------ | --------- | ------------------------------------ | ------------------------------ |
| `POST` | `/ask`    | Ask a question about uploaded docs   | `{ "question": "..." }`       |
| `POST` | `/upload` | Upload and index a PDF document      | `multipart/form-data` (file)   |

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ using FastAPI, LangChain, and Groq
</p>
