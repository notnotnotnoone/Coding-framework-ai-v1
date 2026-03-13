import ollama
import json

def analyze_error(spec, broken_code, error_traceback):
    instructions = (
        "You are an Expert Python Debugger. Your job is to analyze a crashed script "
        "and tell the Junior Developer exactly how to fix it.\n"
        "RULES:\n"
        "1. Be concise. Explain the bug in 1 to 3 sentences.\n"
        "2. DO NOT rewrite the full code. Only provide the targeted fix.\n"
        "3. Focus on resolving the exact Error Traceback provided."
    )

    prompt_context = (
        f"--- ORIGINAL SPECIFICATION ---\n{spec}\n\n"
        f"--- BROKEN CODE ---\n{broken_code}\n\n"
        f"--- TERMINAL ERROR ---\n{error_traceback}\n"
    )

    response = ollama.generate(
        model="llama3.2:3b", 
        system=instructions,
        prompt=prompt_context
    )
    return response['response'].strip()

def observe_execution(spec, terminal_output):
    instructions = (
        "You are an AI Supervisor monitoring a Python script. The script ran continuously for 10 seconds.\n"
        "Look at the Technical Spec and the Terminal Output. You must decide if it is working as intended.\n\n"
        "Respond strictly in JSON format with two keys:\n"
        "1. 'decision': 'SUCCESS' (working perfectly), 'FAIL' (errors or doing the wrong thing), or 'EXTEND' (needs more time).\n"
        "2. 'notes': A 1-sentence explanation of your choice."
    )

    prompt_context = (
        f"--- SPECIFICATION ---\n{spec}\n\n"
        f"--- TERMINAL OUTPUT (First 10 Seconds) ---\n{terminal_output}\n"
    )

    response = ollama.generate(
        model="llama3.2:3b", 
        system=instructions,
        prompt=prompt_context,
        format="json"
    )

    try:
        return json.loads(response['response'].strip())
    except Exception:
        return {"decision": "FAIL", "notes": "Observer failed to parse JSON."}