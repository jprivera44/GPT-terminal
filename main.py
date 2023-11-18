import sys
import subprocess
from backends import OpenAIChatBackend


class LLMQueryHandler:
    def __init__(self):
        self.backend = OpenAIChatBackend("gpt-4")

    def query_LLM(self, system_prompt, user_prompt):
        response = self.backend.complete(system_prompt, user_prompt)
        return response

def execute_command(command):
    """Executes a given bash command and returns the output."""
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Error executing command: {e}"

def main():
    query_handler = LLMQueryHandler()

    while True:
        user_input = input("User> ")
        if user_input.lower() == 'exit':
            break

        # Assuming no system prompt is needed, or you can set it as per your requirement
        system_prompt = "" 
        response = query_handler.query_LLM(system_prompt, user_input)

        print(f"Model Response: {response}")

        if input("Run suggested command? (y/n): ").lower() == 'y':
            command_to_run = input("Enter command to execute: ")
            output = execute_command(command_to_run)
            print(f"Command Output: {output}")

if __name__ == "__main__":
    main()
