from langchain_ollama import ChatOllama
from tools.get_objective import get_objective, get_all_objectives
from tools.get_prompts import get_final_prompt

from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage

import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[ logging.StreamHandler(stream=sys.stdout) ]
)
logger = logging.getLogger(__name__)


llm = ChatOllama(model="qwen3-coder:latest")

tools = [get_objective, get_final_prompt]

tool_mapping = {
    "get_objective" : get_objective,
    "get_all_objectives": get_all_objectives
}

llm_with_tools = llm.bind_tools(tools)

query = "I want to generate math practice problem using the learning objective 6 for math CBE test."
messages = [HumanMessage(content = query)]
logger.info(messages)

response_1 = llm_with_tools.invoke(messages)
logger.info(response_1)
messages.append(response_1)

tool_calls_1 = response_1.tool_calls
print(tool_calls_1)

my_tool=tool_mapping[tool_calls_1[0]['name']]
objective = my_tool.invoke(tool_calls_1[0]['args'])
logger.info(objective)

messages.append(ToolMessage(content = objective, tool_call_id = tool_calls_1[0]['id']))

response_2 = llm_with_tools.invoke(messages)
logger.info(response_2)