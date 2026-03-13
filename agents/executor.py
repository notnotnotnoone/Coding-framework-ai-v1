import subprocess
import sys

def run_in_sandbox(file_path, timeout_seconds=10, test_inputs=""):
    """
    Simulates a terminal environment. 
    Catches prints, errors, and handles infinite loops by triggering an OBSERVE state.
    """
    try:
        result = subprocess.run(
            [sys.executable, file_path],
            input=test_inputs,
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )
        
        if result.returncode == 0:
            return {"status": "SUCCESS", "output": result.stdout.strip(), "error": None}
        else:
            return {"status": "FAILED", "output": result.stdout.strip(), "error": result.stderr.strip()}
            
    except subprocess.TimeoutExpired as e:
        # It timed out. Capture the text it printed before dying!
        captured = e.stdout if e.stdout else "No output was printed."
        return {
            "status": "OBSERVE",
            "output": captured.strip(),
            "error": "Timeout Reached."
        }
    except Exception as e:
        return {"status": "SYSTEM_ERROR", "output": "", "error": str(e)}