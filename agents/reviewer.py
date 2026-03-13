import ollama

def analyze_error(spec, broken_code, error_traceback):
    """
    Acts as the Senior Developer. Analyzes the crashed code and the error,
    then writes clear instructions for the Coder on how to fix it.
    """
    
    # We explicitly tell the Reviewer NOT to write the code itself.
    # Its only job is to diagnose the problem.
    instructions = (
        "You are an Expert Python Debugger. Your job is to analyze a crashed script "
        "and tell the Junior Developer exactly how to fix it.\n"
        "RULES:\n"
        "1. Be concise. Explain the bug in 1 to 3 sentences.\n"
        "2. DO NOT rewrite the full code. Only provide the targeted fix or logic correction.\n"
        "3. Focus on resolving the exact Error Traceback provided."
    )

    # We pack all the context into one massive prompt so the Reviewer has the full picture
    prompt_context = (
        f"--- ORIGINAL SPECIFICATION ---\n{spec}\n\n"
        f"--- BROKEN CODE ---\n{broken_code}\n\n"
        f"--- TERMINAL ERROR (TRACEBACK) ---\n{error_traceback}\n\n"
        "Analyze the error. What went wrong, and what exact changes does the Coder need to make?"
    )

    response = ollama.generate(
        model="llama3.2:3b", 
        system=instructions,
        prompt=prompt_context
    )

    feedback = response['response'].strip()
    return feedback