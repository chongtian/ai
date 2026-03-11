This project demostrates the MCP client and server with Streamable Http Transport. It uses OpenAI sdk and LiteLLM sdk to call LLM.


Step 1. Initialize virtual environment
```bash
python3 -m venv venv
source venv/bin/activate # or in Windows, .\venv\Scripts\activate.ps1
```

Step 2. Install dependencies
```bash
pip install -r requirements.txt
```

Step 3. Run the server (url is http://127.0.0.1:8000)
```bash
python mcp_http_server.py
```

Step 4. Open a new terminal, and activat virtual environment
```bash
source venv/bin/activate # or in Windows, .\venv\Scripts\activate.ps1
```

Step 5. Run the client app in the virtual environment. 

- This is a simple menu interface without LLM. Url: http://127.0.0.1:7861
```bash
python mcp_http_client_app.py http://127.0.0.1:8000 workspace
```

- This is a chatbot interface which requires OpenAI. An OpenAi API Key is required. Url: http://127.0.0.1:7862
```bash
python mcp_http_host_app_openai.py http://127.0.0.1:8000 workspace
```

- This is a chatbot interface which uses LiteLLM to communicate with LLM. It uses Ollama with model *qwen3.5:9b*. Url: http://127.0.0.1:7863
```bash
python mcp_http_host_app_litellm.py http://127.0.0.1:8000 workspace
```