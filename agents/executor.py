import subprocess
import sys

def run_in_sandbox(file_path, timeout_seconds=10, test_inputs=""):
    """
    Simulates a terminal environment. 
    `test_inputs` allows us to "type" into the program if it asks for input (e.g., "y\n10\n").
    """
    print(f"   [SYSTEM] Spinning up sandbox environment for {file_path}...")
    
    try:
        # We run the process and pipe in our test inputs
        result = subprocess.run(
            [sys.executable, file_path],
            input=test_inputs,      # <--- THIS IS THE INTERACTION
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )
        
        if result.returncode == 0:
            return {
                "status": "SUCCESS",
                "output": result.stdout.strip(),
                "error": None
            }
        else:
            return {
                "status": "FAILED",
                "output": result.stdout.strip(),
                "error": result.stderr.strip()
            }
            
    except subprocess.TimeoutExpired as e:
        # --- THE OBSERVATION FIX ---
        # It timed out, but we salvage everything it printed to the terminal before it died!
        captured_output = e.stdout if e.stdout else "No text was printed."
        
        return {
            "status": "TIMEOUT",
            "output": captured_output.strip(),
            "error": f"Process reached {timeout_seconds} second observation limit. Terminal output captured."
        }
    except Exception as e:
        return {
            "status": "SYSTEM_ERROR",
            "output": "",
            "error": str(e)
        }