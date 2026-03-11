import os
import ollama
import re

class OllamaAgent:
    def __init__(self, memory, model):
        self.memory = memory
        self.tools = {}
        self.model = model

    def register_tool(self, name, tool):
        self.tools[name] = tool

    def _call_ollama(self, prompt):
        try:
            resp = ollama.chat(
                model=self.model,
                messages=[{'role':'user','content':prompt}],
                think = False,
                options={
                    'temperature': 0.7,
                    'num_predict': 200  # this is max tokens
                    }
            )
            self.memory.add({'agent': resp})
            return resp.message.content.strip()
        except Exception as e:
            return f"No reponse from LLM. Error: {str(e)}"


    def _use_tool(self, user_input):
        # Tool invocation: if tool name appears in input, use it
        for name, tool in self.tools.items():
            if re.search(rf"\b{name}\b", user_input, flags=re.IGNORECASE):
                try:
                    return tool.run(user_input, self.memory)
                except Exception as e:
                    return f"Tool '{name}' error: {e}"
        return None

    def handle(self, user_input):
        # save to memory
        try:
            self.memory.add({'user': user_input})
        except Exception:
            pass
        # check tools first
        tool_result = self._use_tool(user_input)
        if tool_result:
            try:
                self.memory.add({'agent': tool_result})
            except Exception:
                pass
            return tool_result

        prompt = f"You are an assistant. User said: {user_input}"
        resp = self._call_ollama(prompt)
        
        try:
            self.memory.add({'agent': resp})
        except Exception:
            pass
        return resp
