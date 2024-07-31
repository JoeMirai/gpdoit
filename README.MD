# GPT Shell Command Executor

## Description

GPT Shell Command Executor is a Python script that leverages OpenAI's GPT-4 API to generate and execute shell commands based on user prompts. The script is designed to assist users in executing shell commands without needing to remember complex syntax. By providing a natural language prompt, users can generate precise shell commands that are then executed within their system.

## Features

- **Natural Language Processing**: Utilize OpenAI's GPT-4 model to interpret user prompts and generate corresponding shell commands.
- **Interactive Command Execution**: The script interactively asks for user confirmation before executing any generated command, ensuring safety and control.
- **Error Handling**: Proper error messages are displayed if the command generation or execution fails.

## Usage

1. **Set Up OpenAI API Key**: Ensure you have an OpenAI API key set as an environment variable named `OPENAI_API_KEY`.
2. **Run the Script**: Execute the script using Python. The script will prompt you for input.
3. **Enter Your Request**: Type your request in natural language. For example, "Create a folder named `test` and inside it, create a file named `example.txt` containing the text 'Hello, World!'."
4. **Confirm Execution**: Review the generated command and confirm its execution.


