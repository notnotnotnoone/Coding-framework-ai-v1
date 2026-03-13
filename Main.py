from agents.prompt_engineer import prompt_engineer
from agents.evaluator import evaluate_task
MAIN_PROMPT = prompt_engineer(input("Describe your task here: "))
DIFFICUTLY = evaluate_task(MAIN_PROMPT)

print("Technical Specification:\n", MAIN_PROMPT)
print("\nTask Difficulty:", DIFFICUTLY)