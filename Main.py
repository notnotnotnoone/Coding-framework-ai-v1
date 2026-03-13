import time
import sys
import threading
import itertools
from datetime import datetime
from agents.prompt_engineer import prompt_engineer
from agents.evaluator import evaluate_task
from agents.coder import run_coder
from agents.executor import run_in_sandbox
from agents.reviewer import analyze_error

# --- CYBERPUNK COLOR PALETTE ---
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
DARK_GRAY = "\033[90m"

is_thinking = False

def fake_boot_sequence():
    print(f"\n{BLUE}{BOLD}INITIALIZING NEURAL LINK...{RESET}")
    length = 40
    for i in range(21):
        percent = int((i / 20) * 100)
        filled = int(length * i // 20)
        bar = '█' * filled + '░' * (length - filled)
        sys.stdout.write(f"\r{CYAN}   Booting Subsystems: [{bar}] {percent}%{RESET}")
        sys.stdout.flush()
        time.sleep(0.05)
    print(f"\n{GREEN}{BOLD}   [OK] AI SQUAD ONLINE AND STANDING BY.{RESET}\n")

def animated_spinner(task_name, color):
    global is_thinking
    spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    while is_thinking:
        sys.stdout.write(f"\r{color}{BOLD}   [{next(spinner)}] {task_name}...{RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()

def run_with_spinner(target_func, args, task_name, color):
    global is_thinking
    is_thinking = True
    spin_thread = threading.Thread(target=animated_spinner, args=(task_name, color))
    spin_thread.start()
    result = target_func(*args)
    is_thinking = False
    spin_thread.join()
    return result

def main():
    fake_boot_sequence()

    print(f"{BLUE}{BOLD}{'='*65}{RESET}")
    user_input = input(f"{YELLOW}{BOLD}   [INPUT REQUIRED] Describe your task > {RESET}")
    print(f"{BLUE}{BOLD}{'='*65}{RESET}\n")
    
    start_time = time.time()

    # --- LAYER 1: ARCHITECT ---
    print(f"{CYAN}{BOLD}🏗️  LAYER 1: ARCHITECT (Qwen 0.5B){RESET}")
    spec = run_with_spinner(prompt_engineer, (user_input,), "Drafting Blueprint", CYAN)
    print(f"{CYAN}   [SUCCESS] Specification locked.{RESET}\n")

    # --- LAYER 2: EVALUATOR ---
    print(f"{MAGENTA}{BOLD}⚖️  LAYER 2: EVALUATOR (Llama 3B){RESET}")
    difficulty = run_with_spinner(evaluate_task, (spec,), "Analyzing Logic Complexity", MAGENTA)
    print(f"{MAGENTA}   [ROUTING] Task classified as: {difficulty}{RESET}\n")

    # --- THE AUTO-FIX LOOP (Layers 3, 4, and 5) ---
    max_retries = 3
    attempt = 1
    code_works = False
    current_prompt = spec # Starts as just the spec, but gets feedback added if it fails

    while attempt <= max_retries and not code_works:
        print(f"{GREEN}{BOLD}💻  LAYER 3: CODER (Attempt {attempt}/{max_retries}){RESET}")
        file_saved = run_with_spinner(run_coder, (current_prompt, difficulty), "Compiling Code", GREEN)
        
        # --- LAYER 4: EXECUTOR (Sandbox) ---
        print(f"{YELLOW}{BOLD}⚙️  LAYER 4: EXECUTOR (Sandbox){RESET}")
        sandbox_result = run_with_spinner(run_in_sandbox, (file_saved,), "Testing execution", YELLOW)
        
        if sandbox_result['status'] == "SUCCESS":
            print(f"{GREEN}   [SUCCESS] Code ran flawlessly!{RESET}\n")
            code_works = True
        else:
            print(f"{RED}   [FAILED] Code crashed: {sandbox_result['status']}{RESET}")
            
            if attempt < max_retries:
                # --- LAYER 5: REVIEWER ---
                print(f"{MAGENTA}{BOLD}👁️  LAYER 5: REVIEWER (Llama 3B){RESET}")
                with open(file_saved, "r") as f:
                    broken_code = f.read()
                
                feedback = run_with_spinner(analyze_error, (spec, broken_code, sandbox_result['error']), "Diagnosing Issue", MAGENTA)
                print(f"{MAGENTA}   [FEEDBACK] {feedback}{RESET}\n")
                
                # Update the prompt for the next loop so the Coder knows what to fix
                current_prompt = (
                    f"{spec}\n\n"
                    f"--- CRITICAL FIX REQUIRED ---\n"
                    f"Your previous code failed with this error:\n{sandbox_result['error']}\n\n"
                    f"Senior Developer Instructions:\n{feedback}\n\n"
                    f"Please rewrite the code to fix this issue."
                )
            attempt += 1

    # --- COMPLETION ---
    elapsed = round(time.time() - start_time, 2)
    print(f"{BLUE}{BOLD}{'='*65}{RESET}")
    if code_works:
        print(f"{GREEN}{BOLD}   MISSION ACCOMPLISHED IN {elapsed} SECONDS{RESET}")
    else:
        print(f"{RED}{BOLD}   MISSION FAILED: Max retries reached after {elapsed} seconds.{RESET}")
    print(f"{YELLOW}{BOLD}   TARGET SAVED TO: {file_saved}{RESET}")
    print(f"{BLUE}{BOLD}{'='*65}{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        is_thinking = False
        print(f"\n\n{RED}{BOLD}[!] MANUAL OVERRIDE TRIGGERED. SYSTEM SHUTDOWN.{RESET}")