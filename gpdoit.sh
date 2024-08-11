#!/bin/bash

get_openai_command() {
    local prompt="$1"
    local api_key="$OPENAI_API_KEY"
    
    if [ -z "$api_key" ]; then
        echo "Error: OPENAI_API_KEY environment variable is not set."
        return 1
    fi

    local model="gpt-4o-mini"
    local system_content="You are a ubuntu shell expert user name jack will ask you for something he want to do and you will simply provide him with the command ONLY! do not explain do not add anything beside the command and most importent always keep it one command you can use && or whatever just dont reply more them one command keep it oneline \n e.g. user: I would like to create a folder named x under my Downloads directory. Inside this folder, I want to create a file named x.txt which will contain a random number.. your reply: mkdir -p /home/jack/Downloads/x && echo \$RANDOM > /home/jack/Downloads/x/x.txt"
    local max_tokens=150
    local temperature=0.5

    local response=$(curl -s -X POST https://api.openai.com/v1/chat/completions \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $api_key" \
        -d '{
            "model": "'"$model"'",
            "messages": [
                {"role": "system", "content": "'"$system_content"'"},
                {"role": "user", "content": "'"$prompt"'"}
            ],
            "max_tokens": '"$max_tokens"',
            "temperature": '"$temperature"'
        }')

    if [ $? -ne 0 ]; then
        echo "Failed to get response from API."
        return 1
    fi

    local command=$(echo "$response" | jq -r '.choices[0].message.content' | xargs)

    if [ "$command" == "null" ]; then
        echo "Failed to extract command from API response."
        return 1
    fi

    echo "$command"
}

execute_shell_command() {
    local command="$1"
    eval "$command"
}

while true; do
    read -p "Please enter your request (or type 'exit' to quit): " prompt

    if [ "$prompt" == "exit" ]; then
        echo "Exiting..."
        break
    fi

    command=$(get_openai_command "$prompt")

    if [ $? -ne 0 ]; then
        echo "Error generating command."
        continue
    fi

    echo "Generated command: $command"
    read -p "Are you sure you want to execute this command? (Press Enter to execute, 'q' to quit): " confirmation

    if [ "$confirmation" == "q" ]; then
        echo "Command execution cancelled."
        continue
    fi

    execute_shell_command "$command"
done
