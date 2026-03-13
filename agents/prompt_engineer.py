import ollama

def prompt_engineer(user_task):
    # Updated instructions optimized for the 0.5B model
    instructions = (
        "ROLE: Technical Architect. "
        "TASK: Rewrite the user's messy request into a structured technical specification. "
        "RULES: 1. DO NOT write code. 2. DO NOT use markdown code blocks. "
        "3. Specify Python, required logic, and error handling. "
        "4. Output ONLY the specification text."
    )
    
    # We pass 'system' for instructions and 'options' to lock in the behavior
    response = ollama.generate(
        model="qwen2.5:0.5b", 
        system=instructions, 
        prompt=f"Create a technical specification for: {user_task}",
        options={
            "temperature": 0,    # Forces the model to be predictable
            "num_predict": 150   # Stops it from talking too much
        }
    )
    
    # Return ONLY the text string
    return response['response'].strip()