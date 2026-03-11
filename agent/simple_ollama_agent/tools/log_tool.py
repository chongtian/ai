from memory.memory_manager import MemoryManager
class LogTool:
    def run(self, user_input: str, memory:MemoryManager) -> str:
        """
        This function returns all logs from the memory manager.
        """
        logs = memory.all()
        return f"All logs:\n" + "\n".join([f"{log['_ts']}: {log}" for log in logs])
