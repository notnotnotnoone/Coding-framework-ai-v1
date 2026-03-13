import ollama

def prompt_engineer(user_task):
    instructions = (
        "You are a Technical Architect. Your job is to take a user's request and turn it into a clear, "
        "structured Technical Specification for a Coder to follow.\n"
        "MANDATORY RULE: The program MUST run entirely in the terminal/console. "
        "Do NOT use tkinter, pygame, Flask, or any GUI libraries. If a user asks for a visual app (like a clock), "
        "design it as a continuous text-based terminal output.\n"
        "Keep the specification concise. DO NOT provide code snippets."
    )
    
    response = ollama.generate(
        model="qwen2.5:0.5b", # Or whichever 0.5b model you are using for the Architect
        system=instructions,
        prompt=user_task
    )
    
    return response['response'].strip()