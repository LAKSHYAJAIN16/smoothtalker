# Import all the functions and classes from the shuttleai package
from shuttleai import *

# Initialize the ShuttleClient with your API key.
shuttle = ShuttleClient(api_key="shuttle-v4q4afj7p330f64pb5t8")

# Define the message you want to send to ShuttleAI.
messages = [{"role": "user", "content": "Hi"}]

# Use the chat_completion method to send the message to ShuttleAI.
response = shuttle.chat_completion(
    model="gpt-4", 
    messages=messages, 
    stream=False,
    plain=False,
    image=None, 
    citations=False
)

# Print the response received from ShuttleAI.
message = response['choices'][0]['message']['content']
print(message)