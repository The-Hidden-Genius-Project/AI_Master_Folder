# Lesson Plan: Building a Basic AI Chatbot in Python 

## **Duration:**
45 minutes

## **Lesson Overview:**
Geniuses will begin creating a basic AI chatbot using Python, applying concepts from previous lessons. This session focuses on designing the chatbot's structure and implementing simple response logic.

## **Objectives:**
- Plan the structure of a simple AI chatbot.
- Implement conditional statements to drive chatbot responses.
- Test and debug Python code for functionality.

## **Materials:**
- **Computers with VSCode**
- **Chatbot planning worksheet**
- **Sample code templates**
- **Projector for demonstrations**

## **Standards:**
- Apply programming skills to create AI applications.
- Develop debugging and problem-solving techniques.

## **Lesson Activity:**

### 1. **Introduction (Time: 5 minutes)**
   - **Objective:** Set the stage for building the chatbot.
   - Recap previous Python programming lesson.
   - Present the goal: to build a basic AI chatbot over two sessions.

### 2. **Direct Instruction (Time: 10 minutes)**
   - **Objective:** Outline the chatbot's structure.
   - Discuss key components: greeting, user input, response logic.
   - Introduce conditional statements and string matching.

### 3. **Guided Practice (Time: 25 minutes)**
   - **Objective:** Start coding the chatbot with guidance.
   - **Activity:** "Chatbot Construction Part 1"
     - Geniuses plan their chatbot using blank doc.
     - Begin coding the introduction and basic conversation flow.
     - Implement conditional responses based on user input.
     - Educator demonstrates examples and assists as needed.

### 4. **Independent Practice (Time: 5 minutes)**
   - **Objective:** Personalize the chatbot.
   - Geniuses add unique responses or additional dialogue options.
   - Encourage incorporating elements from prior lessons (e.g., prompt engineering).

### 5. **Closure (Time: 5 minutes)**
   - **Objective:** Review progress and prepare for the next session.
   - Share successes and challenges faced.
   - Outline next steps: enhancing the chatbot's intelligence.

## **Assessment:**
- Check geniuses' code for correct implementation of conditional logic.
- Observe engagement and problem-solving during the coding process.

## **Extra Activities:**
- Geniuses can explore Python libraries for natural language processing (optional, for advanced students).

## **Reflection / Takeaways:**
- Geniuses were excited to see their chatbot take shape.
- Allocate extra time for debugging in the next session.

## Resources(2 different options)

### Step-by-Step Implementation:

#### Step 1: Install Required Libraries
Make sure you have `nltk` installed. You can install it using pip if you haven't already:

```bash
pip install nltk
```

#### Step 2: Set Up the Simple Chatbot

```python
import nltk
from nltk.chat.util import Chat, reflections

# Define a set of pairs - this is the list of patterns and responses
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, how can I help you today?",]
    ],
    [
        r"hi|hey|hello",
        ["Hello!", "Hey there!",]
    ],
    [
        r"what is your name?",
        ["I am a simple chatbot.",]
    ],
    [
        r"how are you?",
        ["I'm just a bunch of code, but thanks for asking!",]
    ],
    [
        r"sorry (.*)",
        ["It's okay, don't worry about it!",]
    ],
    [
        r"I need help with (.*)",
        ["How can I assist you with %1?", "What about %1 is troubling you?",]
    ],
    [
        r"quit",
        ["Goodbye! Have a nice day!",]
    ],
    [
        r"(.*)",
        ["I'm not sure how to respond to that.",]
    ],
]

# Create a chatbot using the defined pairs and reflections
chatbot = Chat(pairs, reflections)

# Function to interact with the chatbot
def chat():
    print("Hello, I am your chatbot. How can I assist you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Goodbye! Have a nice day!")
            break
        else:
            response = chatbot.respond(user_input)
            if response:
                print("Bot:", response)
            else:
                print("Bot: I'm not sure how to respond to that.")

chat()
```

### Explanation:

- **Pairs:** This is a list of keyword-response pairs. The patterns use regular expressions to match input strings. When the pattern is matched, the chatbot returns a response from the corresponding list.
- **Reflections:** This is a dictionary that helps the chatbot adjust responses, flipping input pronouns to make the conversation more natural (e.g., "I am" becomes "you are").
- **Chat Class:** This is an `nltk` utility that processes the input text and tries to find a match in the pairs list.

### Python Code: Simple Rule-Based Chatbot

```python
def chatbot_response(user_input):
    # Convert user input to lowercase for case insensitivity
    user_input = user_input.lower()

    # Keyword-based responses
    if "my name is" in user_input:
        name = user_input.split("my name is")[-1].strip()
        return f"Hello {name}, how can I help you today?"
    
    elif any(greeting in user_input for greeting in ["hello", "hi", "hey"]):
        return "Hello! How can I assist you?"

    elif "your name" in user_input:
        return "I am a simple chatbot."

    elif "how are you" in user_input:
        return "I'm just a program, but I'm functioning as expected. How about you?"

    elif "sorry" in user_input:
        return "It's okay, no worries!"

    elif "help with" in user_input:
        topic = user_input.split("help with")[-1].strip()
        return f"How can I assist you with {topic}?"

    elif "quit" in user_input:
        return "Goodbye! Have a nice day!"

    else:
        return "I'm not sure how to respond to that."

def chat():
    print("Hello, I am your chatbot. How can I assist you today?")
    
    while True:
        user_input = input("You: ")
        response = chatbot_response(user_input)
        print(f"Bot: {response}")

        if "Goodbye!" in response:
            break

chat()
```

### Explanation:

- **Function `chatbot_response`:** This function takes the user input and checks for specific keywords or phrases using simple string operations. It returns appropriate responses based on the matches.
  
- **If-Else Execution:**
  - **Name Recognition:** If the input includes "my name is," it extracts the name and responds with a greeting.
  - **Greeting:** It checks if any common greeting words are present and responds in kind.
  - **Identity and Status:** It handles questions about the bot's identity and status.
  - **Apologies:** It responds to any form of apology.
  - **Help Requests:** It provides a response structure for help requests.
  - **Exit Condition:** When the input includes "quit," it bids farewell and exits.
