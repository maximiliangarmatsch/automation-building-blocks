
#!/bin/bash

# To set up the environment, install dependencies, login to composio and add other necessary tools:
# Login to your account
echo "Login to your Composio account"
composio login

# Add calendar tool
echo "Add Google sheet tool. Finish the flow"
# composio add googlecalendar 
composio add googlesheets

# Copy env backup to .env file
if [ -f ".env.example" ]; then
    echo "Copying .env.example to .env..."
    cp .env.example .env
else
    echo "No .env.example file found. Creating a new .env file..."
    touch .env
fi

# Prompt user to fill the .env file
echo "Please fill in the .env file with the necessary environment variables."

echo "Setup completed successfully!"
