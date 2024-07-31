import subprocess
import requests
import json
import os

def get_openai_command(prompt):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        return None

    model = "gpt-4o-mini"
    system_content = f"You are a ubuntu shell expert user name jack will ask you for something he want to do and you will simply provide im with the command ONLY! do not explain do not add anything beside the command and most importent always keep it one command you can use && or whatever just dont replay more them one command keep it oneline \n e.g. user: I would like to create a folder named x under my Downloads directory. Inside this folder, I want to create a file named x.txt which will contain a random number.. your reply: mkdir -p /home/jack/Downloads/x && echo $RANDOM > /home/jack/Downloads/x/x.txt"
    user_content = prompt
    max_tokens = 150
    temperature = 0.7

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_json = response.json()
        command = response_json['choices'][0]['message']['content'].strip()
        return command
    else:
        print(f"Failed to get response: {response.status_code}, {response.text}")
        return None

def execute_shell_command(command):
    try:
        # Execute the shell command
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Print the output
        print("Output:\n", result.stdout)
        if result.stderr:
            print("Errors:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

if __name__ == "__main__":
    while True:
        # Ask the user for a prompt
        prompt = input("Please enter your request (or type 'exit' to quit): ")

        # Check if the user wants to exit
        if prompt.lower() == 'exit':
            print("Exiting...")
            break

        # Get the command from OpenAI API
        command = get_openai_command(prompt)
        if command:
            # Confirm with the user before executing
            print(f"Generated command: {command}")
            confirmation = input("Are you sure you want to execute this command? (Press Enter to execute, 'q' to quit): ")
            if confirmation.lower() == 'q':
                print("Command execution cancelled.")
                continue
            else:
                execute_shell_command(command)
