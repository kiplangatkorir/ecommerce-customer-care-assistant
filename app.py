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

# Knowledge base
knowledge_base = {
    "products": {
        "wireless headphones": {
            "features": "Bluetooth 5.0, noise cancellation, 20-hour battery life",
            "specifications": "Over-ear, black color, includes carrying case",
            "availability": "In stock",
            "price": "$99.99"
        },
        # Add more products as needed
    },
    "orders": {
        "status": "You can track your order using the order ID provided in your confirmation email.",
        "tracking": "To track your order, visit our tracking page and enter your order ID.",
        "delivery": "Orders are typically delivered within 3-5 business days."
    },
    "returns": {
        "process": "To return an item, please visit our returns page and follow the instructions.",
        "exchange": "Exchanges can be processed by visiting our exchanges page or contacting customer support.",
        "refund": "Refunds are issued within 5-7 business days after we receive the returned item."
    },
    "promotions": {
        "current": "Check out our current promotions page for the latest offers.",
        "discount_codes": "Use code SAVE20 for 20% off your next purchase.",
        "special_offers": "Buy one, get one 50% off on select items."
    },
    "shipping": {
        "methods": "We offer standard, expedited, and overnight shipping options.",
        "times": "Standard shipping takes 3-5 business days, expedited takes 2-3 business days, and overnight shipping delivers the next business day.",
        "costs": "Shipping costs vary based on the shipping method selected and the destination."
    },
    "account": {
        "password_reset": "To reset your password, visit our password reset page and enter your email address.",
        "account_update": "You can update your account information by logging into your account and visiting the account settings page."
    },
    "store_info": {
        "services": "We offer a wide range of products, gift wrapping, and personalized recommendations.",
        "contact": "You can contact us via email at support@ecommerce.com or call us at 1-800-123-4567."
    }
}

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

# Function to check the knowledge base for a relevant response
def check_knowledge_base(user_input):
    user_input_lower = user_input.lower()
    for category, items in knowledge_base.items():
        for item, details in items.items():
            if item in user_input_lower:
                response = f"{item.capitalize()} details:\n"
                for key, value in details.items():
                    response += f"- {key.capitalize()}: {value}\n"
                return response.strip()
    return None

while True:
    # Get user input
    user_input = input("You: ")

    # Check if the user wants to exit the conversation
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Chloe: Goodbye! Have a great day!")
        break

    # Check the knowledge base for a response
    kb_response = check_knowledge_base(user_input)
    if kb_response:
        print(f"Chloe: {kb_response}")
        continue

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
