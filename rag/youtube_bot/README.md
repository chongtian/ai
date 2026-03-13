# YouTube Video Summarizer and Q&A
This project showcases a lightweight Retrieval-Augmented Generation (RAG) agent built around YouTube video transcripts. After the user provides a valid YouTube URL, the system automatically extracts the English transcript from the video. The user can then choose to request a summary or ask questions about the video’s content.

When answering user questions, the agent runs through a complete modern RAG pipeline:

1. Chunking the transcript
2. Embedding the chunks
3. Storing them in an in-memory FAISS vector index
4. Running similarity search to retrieve the most relevant context
5. Passing both the question and retrieved context to an LLM
6. Returning the final answer to the user

The original script from the online course relied on IBM WatsonX.AI and the classic LangChain LLMChain, both of which felt overly complex or outdated for this simple use case. I rewrote the entire workflow to use:
- Modern *LCEL* for cleaner, future-proof pipelines
- Local LLM inference via Ollama, removing the dependency on WatsonX.AI

How to use:
```bash
# create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# run, url is http://127.0.0.1:7860
python ytbot.py
```