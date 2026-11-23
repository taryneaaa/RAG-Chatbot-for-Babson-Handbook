# Babson Handbook Chatbot

A chatbot that answers questions about the Babson College undergraduate student handbook. Ask something like *"What is the policy on missing class?"* and it finds the relevant parts of the handbook and writes an answer based on them.

Built for OIM 3641: AI-Driven App Development at Babson College (Fall 2026).

## How it works

The app uses **retrieval-augmented generation (RAG)**: instead of asking an AI model to answer from memory, it first looks up the right passages in the handbook, then has the model answer using only those passages.

1. **Load:** LlamaIndex reads the handbook PDF from `data/`.
2. **Index:** each chunk of the handbook is turned into an embedding with the open-source `BAAI/bge-small-en-v1.5` model from Hugging Face and stored in a vector index.
3. **Retrieve:** when you ask a question, the index finds the handbook chunks closest in meaning to it.
4. **Answer:** Google Gemini (`gemini-3.5-flash-lite`) writes an answer from those chunks.
5. **Chat:** a Streamlit interface keeps the conversation on screen. The index is built once per session and cached, so later questions are fast.

## Tech stack

| Part | Tool |
| --- | --- |
| Language | Python 3.14 |
| RAG framework | LlamaIndex |
| Embeddings | Hugging Face `BAAI/bge-small-en-v1.5` (runs locally) |
| Language model | Google Gemini API |
| Interface | Streamlit |
| Package manager | uv |

## Run it yourself

**1. Clone the repository**

```bash
git clone https://github.com/taryneaaa/RAG-Chatbot-for-Babson-Handbook.git
cd RAG-Chatbot-for-Babson-Handbook
```

**2. Add your Gemini API key**

Get a free key at https://aistudio.google.com/apikey, then create a file named `.env` in the project folder:

```
GEMINI_API_KEY=your-key-here
```

The `.env` file is listed in `.gitignore`, so your key is never uploaded.

**3. Install and run**

```bash
uv sync
uv run streamlit run app.py
```

Streamlit opens the chatbot in your browser (usually at http://localhost:8501). The first question takes a little longer while the handbook is indexed.

## Project structure

```
RAG-Chatbot-for-Babson-Handbook/
├── app.py                  # Streamlit app: builds the index and runs the chat
├── data/
│   └── undergraduate-student-handbook.pdf
├── src/rag_chatbot/        # Package folder
├── pyproject.toml          # Dependencies
└── uv.lock
```

## Limitations

- Answers are only as current as the handbook PDF in `data/`. To update them, replace the PDF and restart the app.
- The model can still misread a passage, so check important answers against the handbook itself.
- If the Gemini API is busy or rate-limited, the app shows an error message; try again after a minute.

## Author

Tarynea Aggarwal, Babson College
