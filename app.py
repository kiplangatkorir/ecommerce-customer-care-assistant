import requests

# Set up the Llama API key
API_KEY = "API_KEY"

# Define the assistant's personality and name
personality = "I am Chloe, a friendly and helpful customer care assistant for ShopYetu, an e-commerce store. I strive to provide excellent customer service by answering questions, addressing concerns, and offering solutions in a warm and professional manner."
name = "Chloe"

# Define the assistant's functions
functions = [
    "Answering product-related questions (features, specifications, availability, etc.)",
    "Providing order status updates and tracking information",
    "Assisting with returns, exchanges, and refund processes",
    "Offering recommendations and suggestions based on customer preferences",
    "Addressing customer complaints and resolving issues",
    "Explaining shipping and delivery policies",
    "Providing general information about the store and its services"
]

# Define the API endpoint and headers
API_URL = "https://oai.hconeai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Initialize the conversation history
conversation = [
    {"role": "system", "content": f"{personality}\n\nMy name is {name}, and my functions include:\n\n{'- ' + '\n- '.join(functions)}\n"}
]

while True:
    # Get user input
    user_input = input("You: ")

    # Add user input to the conversation history
    conversation.append({"role": "user", "content": user_input})

    # Define the request payload
    payload = {
        "model": "gpt-3.5-turbo-16k",
        "messages": conversation,
        "temperature": 0.7,
        "max_tokens": 1024,
        "n": 1,
        "stop": None
    }

    # Send the request to the Llama API
    response = requests.post(API_URL, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the generated text from the API response
        generated_text = response.json()["choices"][0]["message"]["content"]

        # Print Chloe's response
        print(f"Chloe: {generated_text}")

        # Add Chloe's response to the conversation history
        conversation.append({"role": "assistant", "content": generated_text})
    else:
        # Print the error message
        print(f"Error: {response.json()['error']}")

    # Check if the user wants to exit the conversation
    if user_input.lower() in ["exit", "quit", "bye"]:
        break