import nltk
import requests
import os
from nltk.chat.util import Chat, reflections
import pyttsx3

# Define some patterns and responses for the chatbot
pairs = [
    [
        r"hi|hello|hey",
        ["Hello!", "Hi there!", "Hey!"]
    ],
    [
        r"how are you",
        ["I'm just a chatbot, but I'm here to help!", "I'm doing well. How can I assist you?"]
    ],
    [
        r"what is your name|who are you",
        ["I am a chatbot.", "I go by ChatGPT. How can I assist you?"]
    ],
    [
        r"what can you do|help",
        ["I can answer questions, provide information, or just chat with you. Feel free to ask anything!", "I can assist with general information. What do you need?"]
    ],
    [
        r"what is (.*)|tell me about (.*) |(.*)",
        ["Let me find information about {}..."]
    ],
    [
        r"bye|goodbye",
        ["Goodbye!", "Farewell!", "See you later!"]
    ]
]

# Create a chatbot instance
chatbot = Chat(pairs, reflections)

# Wikipedia summary API URL
wikipedia_summary_api_url = "https://en.wikipedia.org/api/rest_v1/page/summary"

# Function to fetch a concise summary from Wikipedia
def get_wikipedia_summary(topic):
    response = requests.get(f"{wikipedia_summary_api_url}/{topic}")
    data = response.json()
    return data.get("extract", "I couldn't find information about that.")

#speak 
def speak_response(response_text):
    engine = pyttsx3.init()
    engine.say(response_text)
    engine.runAndWait()

# Start a conversation with the chatbot
print("Hello! I'm your chatbot. You can type 'bye' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'bye':
        print("Chatbot: Goodbye!")
        break
    else:
        response = chatbot.respond(user_input)
        if "{}" in response:
            topic = user_input.split(" ")[-1]
            info = get_wikipedia_summary(topic)
            print("Chatbot:", response.format(topic))
            print(info)
            speak_response(response.format(topic) + info)
        else:
            print("Chatbot:", response)
            speak_response(response)
