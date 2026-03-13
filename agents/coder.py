import ollama
import os

def run_coder(specification, difficulty):
    # Determine which model to use based on the Evaluator's choice
    if difficulty == "SIMPLE":
        selected_model = "llama3.2:3b"
        print(f"[*] Task is {difficulty}: Using Llama 3B (Fast Mode)")
    else:
        selected_model = "qwen2.5-coder:7b"
        print(f"[*] Task is {difficulty}: Using Qwen 7B (Power Mode)")

    instructions = (
        "You are a Senior Python Developer. Write a complete, working Python script "
        "based on the technical specification. "
        "RULES: Output ONLY the code. No markdown formatting. No backticks. No explanations."
        "MANDATORY RULE: The program MUST run entirely in the terminal/console. Do NOT use tkinter, pygame, or any GUI libraries. If a user asks for a visual app (like a clock), design it as a text-based terminal output."
    )

    response = ollama.generate(
        model=selected_model,
        system=instructions,
        prompt=specification
    )

    code = response['response'].strip()

    # --- THE SCRUBBER ---
    # Strip out markdown code fences if the model ignored the rules
    lines = code.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]  # Remove the top ```python
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1] # Remove the bottom ```
    
    # Rejoin the clean lines
    clean_code = "\n".join(lines).strip()

    # Create output directory if it doesn't exist
    if not os.path.exists("output"):
        os.makedirs("output")

    # Save the clean code
    file_path = "output/current_task.py"
    with open(file_path, "w") as f:
        f.write(clean_code)

    return file_path