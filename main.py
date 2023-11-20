import sys
import subprocess
from backends import OpenAIChatBackend
import os
import openai

'''
class LLMQueryHandler:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key is None:
            print("Error: The OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
            sys.exit(1)  # Exit the program if the API key is not set
        self.backend = OpenAIChatBackend("gpt-4")


    def query_LLM(self, system_prompt, user_prompt):

        response = self.backend.complete(system_prompt, user_prompt)
        return response
'''

#The code below is meant for the streaming of tokens, however I kept receiveing a nontype error
#This is likley becuae i am using openai version 0.28, and streaming is not supported on this version.


#new class
class LLMQueryHandler:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key is None:
            print("Error: The OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
            sys.exit(1)  # Exit the program if the API key is not set
        self.backend = OpenAIChatBackend("gpt-4-32k")

    def query_LLM(self, system_prompt, user_prompt):
        try:
            # Prepare the messages for the chat context
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            response_stream = openai.ChatCompletion.create(
                model=self.backend.model_name,
                messages=messages,
                temperature=1.0,
                max_tokens=100,  # Adjust max tokens as needed
                stream=True
            )

            full_response = ""
            for response in response_stream:
                if 'choices' in response and len(response['choices']) > 0:
                    token = response['choices'][0].get('message', {}).get('content', '')
                    full_response += token
                    print(token, end='', flush=True)  # Print each token
            return full_response
        except Exception as e:
            print(f"Error during streaming: {e}")
            return ""


   


def execute_command(command):
    """Executes a given bash command and returns the output."""
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
        return result.stdout.strip() if result.stdout.strip() else result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "Command timed out."
    except Exception as e:
        return f"Error executing command: {e}"
    



def main():
    # Initial system prompt based on the screenshot provided
    system_prompt = (
        "You are being run in a scaffold in a shell on a Macbook. "
        "When you want to run a shell command, write it in a <bash> XML tag. "
        "Other things you say will be sent to the user. "
        "Remember that you can't interact with stdin directly, so if you want to do things over ssh you need to run commands "
        "that will finish and return control to you rather than blocking on stdin. "
        "Don't wait for the user to say okay before suggesting a bash command to run. "
        "If possible, don't include explanation, just say the command.\n"
    )
    

    query_handler = LLMQueryHandler()

    while True:
        user_input = input("User> ")
        if user_input.lower() == 'exit':
            break

        # Fetch the complete response from the model # Changed
        model_response_text = query_handler.query_LLM(system_prompt, user_input) # Changed

        # Check if a valid response was received # Changed
        if model_response_text: # Changed
            print(f"Model Response: {model_response_text}") # Changed

            # Use the complete response to search for the <bash> tag # Changed
            start_tag = "<bash>"
            end_tag = "</bash>"
            start_index = model_response_text.find(start_tag) # Changed
            end_index = model_response_text.find(end_tag) # Changed

            if start_index != -1 and end_index != -1:
                # Extracting the command from within the <bash> tags # Changed
                command_to_run = model_response_text[start_index + len(start_tag):end_index].strip() # Changed
                if input("Do you want to run this command? (yes/no): ").lower() == 'yes':
                    output = execute_command(command_to_run)
                    print(f"Command Output: \n{output}")
                else:
                    print("Command execution cancelled.")
            else:
                print("No command found to execute.")
        else:
            print("No response received from the model.") # Changed

if __name__ == "__main__":
    main()