import time
import sys
import threading
import itertools
from datetime import datetime
from agents.prompt_engineer import prompt_engineer
from agents.evaluator import evaluate_task
from agents.coder import run_coder
from agents.executor import run_in_sandbox
from agents.reviewer import analyze_error, observe_execution

# --- CYBERPUNK COLOR PALETTE ---
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"

is_thinking = False

def fake_boot_sequence():
    print(f"\n{BLUE}{BOLD}INITIALIZING NEURAL LINK...{RESET}")
    for i in range(21):
        percent = int((i / 20) * 100)
        bar = '█' * (i * 2) + '░' * (40 - (i * 2))
        sys.stdout.write(f"\r{CYAN}   Booting Subsystems: [{bar}] {percent}%{RESET}")
        sys.stdout.flush()
        time.sleep(0.02)
    print(f"\n{GREEN}{BOLD}   [OK] AI SQUAD ONLINE.{RESET}\n")

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

    print(f"{CYAN}{BOLD}🏗️  LAYER 1: ARCHITECT{RESET}")
    spec = run_with_spinner(prompt_engineer, (user_input,), "Drafting Blueprint", CYAN)
    print(f"{CYAN}   [SUCCESS] Specification locked.{RESET}\n")

    print(f"{MAGENTA}{BOLD}⚖️  LAYER 2: EVALUATOR{RESET}")
    difficulty = run_with_spinner(evaluate_task, (spec,), "Analyzing Logic", MAGENTA)
    print(f"{MAGENTA}   [ROUTING] Task classified as: {difficulty}{RESET}\n")

    max_retries = 3
    attempt = 1
    code_works = False
    current_prompt = spec

    while attempt <= max_retries and not code_works:
        print(f"{GREEN}{BOLD}💻  LAYER 3: CODER (Attempt {attempt}/{max_retries}){RESET}")
        file_saved = run_with_spinner(run_coder, (current_prompt, difficulty), "Compiling Code", GREEN)
        
        print(f"{YELLOW}{BOLD}⚙️  LAYER 4: EXECUTOR (Sandbox){RESET}")
        sandbox_result = run_with_spinner(run_in_sandbox, (file_saved,), "Executing", YELLOW)
        
        if sandbox_result['status'] == "SUCCESS":
            print(f"{GREEN}   [SUCCESS] Code ran flawlessly!{RESET}\n")
            code_works = True
            
        elif sandbox_result['status'] == "OBSERVE":
            print(f"{MAGENTA}{BOLD}👁️  LAYER 4.5: OBSERVER{RESET}")
            obs = run_with_spinner(observe_execution, (spec, sandbox_result['output']), "Reviewing Output", MAGENTA)
            
            if obs.get('decision') == "SUCCESS":
                print(f"{GREEN}   [SUCCESS] {obs.get('notes')}{RESET}\n")
                code_works = True
            else:
                print(f"{RED}   [FAILED] {obs.get('notes')}{RESET}\n")
                sandbox_result['error'] = f"Observer rejected output: {obs.get('notes')}\nTerminal printed:\n{sandbox_result['output']}"
                sandbox_result['status'] = "FAILED" # Force it into the Reviewer block below

        if not code_works and sandbox_result['status'] != "OBSERVE":
            print(f"{RED}   [CRASH] {sandbox_result['error'][:100]}...{RESET}")
            if attempt < max_retries:
                print(f"{MAGENTA}{BOLD}🔧  LAYER 5: DEBUGGER{RESET}")
                with open(file_saved, "r") as f:
                    broken_code = f.read()
                
                feedback = run_with_spinner(analyze_error, (spec, broken_code, sandbox_result['error']), "Diagnosing Issue", MAGENTA)
                print(f"{MAGENTA}   [FEEDBACK] {feedback}{RESET}\n")
                
                current_prompt = f"{spec}\n\n--- CRITICAL FIX REQUIRED ---\nError:\n{sandbox_result['error']}\n\nDebugger Instructions:\n{feedback}\nRewrite code to fix this."
            attempt += 1

    elapsed = round(time.time() - start_time, 2)
    print(f"{BLUE}{BOLD}{'='*65}{RESET}")
    if code_works:
        print(f"{GREEN}{BOLD}   MISSION ACCOMPLISHED IN {elapsed} SECONDS{RESET}")
    else:
        print(f"{RED}{BOLD}   MISSION FAILED AFTER {elapsed} SECONDS{RESET}")
    print(f"{YELLOW}{BOLD}   TARGET SAVED TO: {file_saved}{RESET}")
    print(f"{BLUE}{BOLD}{'='*65}{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        is_thinking = False
        print(f"\n\n{RED}{BOLD}[!] SYSTEM SHUTDOWN.{RESET}")