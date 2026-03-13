import ollama
import json

def evaluate_task(specification):
    instructions = (
        "You are a Task Classifier. Review the technical specification. "
        "1. Provide a 2-sentence explanation of why the task is simple or complex. "
        "2. Categorize the task as 'SIMPLE' or 'COMPLEX'. "
        "You MUST respond in JSON format with two keys: 'reasoning' and 'category'."
    )
    
    response = ollama.generate(
        model="llama3.2:3b", 
        system=instructions, 
        prompt=specification,
        format="json", 
        options={
            "temperature": 0, 
            "num_predict": 200 # Bumped slightly for safety
        }
    )
    
    raw_content = response['response'].strip()

    try:
        data = json.loads(raw_content)
        # Success path
        reasoning = data.get("reasoning", "No reasoning provided.")
        category = data.get("category", "COMPLEX").strip().upper()
        
        print(f"\n[EVALUATOR REASONING]: {reasoning}")
        return category

    except Exception as e:
        # Error path - This will tell you exactly what went wrong
        print(f"\n[!] JSON Parse Failed: {e}")
        print(f"[!] Raw output was: {raw_content}")
        return "COMPLEX"