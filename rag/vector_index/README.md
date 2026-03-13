# Icebreaker Bot - Demo VectorIndex and basic retriever

An AI-powered assistant that generates personalized icebreakers and conversation starters based on LinkedIn profiles. Built with Ollama and LlamaIndex, it helps make professional introductions more personal and engaging.

Reference: https://github.com/HaileyTQuach/icebreaker.git

### Using the Command Line Interface

Run the bot using the terminal:

```bash
# Use mock data (no API key needed)
python main.py
```

### Using the Web Interface

Launch the web app:

```bash
python app.py
```

Then open your browser to the URL shown in the terminal (typically http://127.0.0.1:7860).

## 🧠 How It Works

The Icebreaker Bot uses a Retrieval-Augmented Generation (RAG) pipeline:

1. **Data Extraction**: LinkedIn profile data is retrieved via ProxyCurl API or mock data
2. **Text Processing**: Profile data is split into manageable chunks
3. **Vector Embedding**: Text chunks are converted to vector embeddings using IBM watsonx
4. **Storage**: Embeddings are stored in a vector database
5. **Query & Generation**: When asked a question, relevant profile sections are retrieved and an IBM watsonx LLM generates contextually accurate responses

## 🛠️ Project Structure

```
icebreaker_bot/
├── requirements.txt           # Dependencies
├── config.py                  # Configuration settings
├── modules/
│   ├── __init__.py
│   ├── data_extraction.py     # LinkedIn profile data extraction
│   ├── data_processing.py     # Data splitting and indexing
│   ├── llm_interface.py       # LLM setup and interaction
│   └── query_engine.py        # Query processing and response generation
├── app.py                     # Gradio web interface
└── main.py                    # CLI application
```

## 📝 Examples

Here are some example questions you can ask:

- "What is this person's current job title?"
- "Where did they get their education?"
- "What skills do they have related to machine learning?"
- "How long have they been working at their current company?"
- "What was their career progression?"


## How to use

Step 1. Initialize virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Step 2. Install dependencies
```bash
pip install -r requirements.txt
```
