This project demostrates the basic MCP client and server concepts. This project does not require a LLM model to work. 

Step 1. Initialize virtual environment
```bash
python3 -m venv mcp_client_env
source mcp_client_env/bin/activate
```

or in Windows,
```pwsh
python3 -m venv mcp_client_env
.\mcp_client_env\Scripts\activate.ps1
```

Step 2. Install dependencies
```bash
pip install mcp==1.16.0 fastmcp==2.12.5
```

Step 3. Run the scripts
```bash
python mcp_client.py mcp_server.py
```