# Model Mapping for the Surface Laptop (16GB RAM)
MODELS = {
    "prompt_fixer": "llama3.2:3b",
    "evaluator": "qwen3:0.6b",
    "coder": "qwen2.5-coder:7b",
    "reviewer": "deepseek-r1:8b",
    "boss": "phi4:14b"
}

# Framework Settings
MAX_RETRIES = 3
TEMP_CODE_FILE = "output/current_task.py"
LOG_FILE = "logs/session_history.log"

