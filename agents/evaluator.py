import ollama
import json

def evaluate_task(specification):
    # We redefine what SIMPLE and COMPLEX mean to the AI
    instructions = (
        "You are a Senior Technical Lead. Classify this task strictly based on these rules:\n"
        "1. SIMPLE: The task can be solved using built-in Python libraries (os, sys, datetime, math) or a single-file UI (tkinter). "
        "It does not require external API keys, databases, or training machine learning models.\n"
        "2. COMPLEX: Requires external APIs (OpenWeather, OpenAI), multiple files, database integration, or high-level GUI libraries like PyQt.\n\n"
        "Respond in JSON format with 'reasoning' (2 sentences) and 'category' ('SIMPLE' or 'COMPLEX')."
    )
    
    response = ollama.generate(
        model="llama3.2:3b", 
        system=instructions, 
        prompt=specification,
        format="json", 
        options={
            "temperature": 0.1, # Small bump to prevent 'stuck' logic
            "num_predict": 250 
        }
    )
    
    raw_content = response['response'].strip()

    try:
        data = json.loads(raw_content)
        reasoning = data.get("reasoning", "No reasoning provided.")
        category = data.get("category", "COMPLEX").strip().upper()
        
        print(f"\n[EVALUATOR REASONING]: {reasoning}")
        return category

    except Exception as e:
        print(f"\n[!] JSON Parse Failed: {e}")
        return "COMPLEX"