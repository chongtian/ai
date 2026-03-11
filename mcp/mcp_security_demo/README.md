This project demostrates how to implement security control from MCP client. The MCP server is implemented with stdio transport.


Step 1. Initialize virtual environment
```bash
python3 -m venv venv
source venv/bin/activate # or in Windows, .\venv\Scripts\activate.ps1
```

Step 2. Install dependencies
```bash
pip install -r requirements.txt
```

Step 3. Run the client app 

- This is a simple menu interface which does not require a LLM. Url: http://127.0.0.1:7864
```bash
python mcp_permission_client_app.py mcp_permission_server.py
```

This is a chatbot interface which requires OpenAI. An OpenAi API Key is required. Url: http://127.0.0.1:7865
```bash
python mcp_permission_host_app_openai.py mcp_permission_server.py
```

- This is a chatbot interface which uses LiteLLM to communicate with LLM. It uses Ollama with model *qwen3.5:9b*. Url: http://127.0.0.1:7866
```bash
python mcp_permission_host_app_litellm.py mcp_permission_server.py
```