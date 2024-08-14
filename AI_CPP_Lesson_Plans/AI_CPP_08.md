<img src="https://github.com/Hgp-GeniusLabs/Curriculum/blob/10734f2c827128dde773ea4f266d154d46977866/Org-Wide/Assets/hgp_logo_original.png" width="150"/>

# LESSON 8: Chatbots in AI

## Overview			
* Understand the basics of AI
* See how AI shapes our future
* Learn how to maneuver around the world of AI
* Learn different components that make up AI
* Work with real world AI Applications

## Learning Activities and Time Duration(2 hours) 


1. **Welcome and Introduction (5 minutes):**
   - Briefly introduce yourself and set the context for the lesson. (Facial Recognition)

2. **Group Discussion (15 minutes):**
   - Ask students what they know about facial recognition. Write their ideas on the whiteboard if available.
   - Define facial recognition in terms of face ID and other softwares we use.
   - Show a short, engaging video about how chatbots learn([How AIs, like ChatGPT, Learn](https://www.youtube.com/watch?v=R9OHn5ZF4Uo)).

3. Play Gartic Phone(https://www.humanornot.ai/)
Play 3 rounds and have students guess if AI or not
Discuss how Ai can imitate humans



4. Play chatgpt games (tic tac toe, hangman)

5.Play Gandalf AI game(https://gandalf.lakera.ai/gpt-is-password-encoded)

6. Take break (10 minutes)

7. Code AI Chatbot 

```
import nltk
from nltk.chat.util import Chat, reflections

# Define the pattern-response pairs
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, How are you today?",]
    ],
    [
        r"hi|hey|hello",
        ["Hello", "Hey there",]
    ],
    [
        r"what is your name?",
        ["I am a bot created by [Your Name]. You can call me ChatBot!",]
    ],
    [
        r"how are you?",
        ["I'm a bot, so I don't have feelings, but thank you for asking!",]
    ],
    [
        r"sorry (.*)",
        ["It's alright", "No problem",]
    ],
    [
        r"I am fine",
        ["Great to hear that!",]
    ],
    [
        r"quit",
        ["Bye! Take care.",]
    ],
    [
        r"(.*)",
        ["I don't quite understand that. Can you rephrase?",]
    ]
]

# Define the chatbot function
def chatbot():
    print("Hi! I am a simple chatbot. Let's chat! (type 'quit' to end the conversation)")
    chat = Chat(pairs, reflections)
    chat.converse()

# Run the chatbot program if this script is executed
if __name__ == "__main__":
    chatbot()
```


9. Complete Kahoot
