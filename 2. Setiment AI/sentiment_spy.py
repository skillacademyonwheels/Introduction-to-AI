# Import necessary libraries
# - TextBlob for natural language processing tasks like sentiment analysis
import colorama
from textblob import TextBlob
# - Colorama for colored terminal output
from colorama import Fore, Style, init
# - sys and time for animations and delays
import sys
import time

# Initialize Colorama to reset terminal colors automatically after each output
colorama.init(autoreset=True)


# Define global variables
# - `user_name`: To store the name of the user (Agent)
user_name = ""
# - `conversation_history`: A list to store all user inputs
conversation_history = []
# - Sentiment counters (`positive_count`, `negative_count`, `neutral_count`) to track sentiment trends
positive_count = 0
negative_count = 0

# Define a function to simulate a processing animation
def loading_dots():
    """Simulate a loading animation with dots."""
    print("Analyzing your sentiment", end="")
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(0.5)  # Delay for half a second
    print()  # New line after the loading animation
# - Prints "loading dots" to make the chatbot feel interactive

# - Use a loop to display three dots with a slight delay

# Define a function to analyze sentiment of the text
def analyze_sentiment(text):
    """Analyze the sentiment of the input text and update sentiment counters."""
    global positive_count, negative_count, neutral_count, conversation_history

    # Create a TextBlob object for sentiment analysis
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # Get the polarity score

    # Determine sentiment category based on polarity
    if polarity > 0.5:
        sentiment = "Very Positive"
        positive_count += 1
        color = Fore.GREEN
    elif polarity > 0:
        sentiment = "Positive"
        positive_count += 1
        color = Fore.LIGHTGREEN_EX
    elif polarity == 0:
        sentiment = "Neutral"
        neutral_count += 1
        color = Fore.YELLOW
    elif polarity < -0.5:
        sentiment = "Very Negative"
        negative_count += 1
        color = Fore.RED
    else:
        sentiment = "Negative"
        negative_count += 1
        color = Fore.LIGHTRED_EX

    # Append the user input to conversation history
    conversation_history.append(text)

    # Print the result with color coding
    print(f"{color}Sentiment: {sentiment}{Style.RESET_ALL}")
# - Use TextBlob to calculate the polarity of the input text
# - Categorize the sentiment into "Very Positive," "Positive," "Neutral," "Negative," or "Very Negative"
# - Append the user input to `conversation_history`

# - Update the sentiment counters based on the category
# - Handle exceptions to avoid crashes

# Define a function to handle commands
def handle_command(command):
    """Handle special commands like summary, reset, history, and help."""
    global positive_count, negative_count, neutral_count, conversation_history

    if command == "summary":
        print(f"{Fore.CYAN}Summary of Sentiments:{Style.RESET_ALL}")
        print(f"Positive: {positive_count}, Negative: {negative_count}, Neutral: {neutral_count}")
    elif command == "reset":
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        conversation_history.clear()
        print(f"{Fore.YELLOW}Conversation history and sentiment counters have been reset.{Style.RESET_ALL}")
    elif command == "history":
        print(f"{Fore.MAGENTA}Conversation History:{Style.RESET_ALL}")
        for i, sentence in enumerate(conversation_history, start=1):
            print(f"{i}. {sentence}")
    elif command == "help":
        print(f"{Fore.BLUE}Available Commands:{Style.RESET_ALL}")
        print("1. summary - Show sentiment summary")
        print("2. reset - Reset sentiment counters and history")
        print("3. history - Show conversation history")
        print("4. help - Show this help message")
    else:
        print(f"{Fore.RED}Unknown command: {command}{Style.RESET_ALL}")
# - Handle commands like `summary`, `reset`, `history`, and `help`
# - `summary`: Displays the count of positive, negative, and neutral sentiments
# - `reset`: Clears the conversation history and resets counters
# - `history`: Shows all previous user inputs
# - `help`: Displays a list of available commands
# - Return appropriate responses for each command

# Define a function to validate the user's name
def validate_name(name):
    """Validate the user's name to ensure it is alphabetic and not empty."""
    if name.isalpha() and name.strip():
        return True
    else:
        print(f"{Fore.RED}Invalid name. Please enter a valid alphabetic string.{Style.RESET_ALL}")
        return False
# - Continuously prompt the user for a name until they enter a valid alphabetic string
# - Strip any extra spaces and ensure the input is not empty or invalid

# Define the main function to start the chatbot
def start_sentiment_chat():
    """Start the Sentiment Spy chatbot."""
    global user_name

    # Display welcome message
    print(f"{Fore.CYAN}Welcome to Sentiment Spy!{Style.RESET_ALL}")
    print("I will analyze the sentiment of your sentences.")
    
    # Ask for user's name
    while True:
        user_name = input("Please enter your name: ").strip()
        if validate_name(user_name):
            break

    print(f"{Fore.GREEN}Hello, {user_name}! Let's start analyzing your sentences.{Style.RESET_ALL}")

    # Main loop for user interaction
    while True:
        user_input = input(f"{Fore.YELLOW}{user_name}, enter a sentence or command (type 'exit' to quit): {Style.RESET_ALL}").strip()

        if not user_input:
            print(f"{Fore.RED}Please enter a valid sentence.{Style.RESET_ALL}")
            continue

        if user_input.lower() == "exit":
            print(f"{Fore.CYAN}Thank you for using Sentiment Spy, {user_name}! Goodbye!{Style.RESET_ALL}")
            break
        elif user_input.lower() == "summary":
            handle_command("summary")
        elif user_input.lower() == "reset":
            handle_command("reset")
        elif user_input.lower() == "history":
            handle_command("history")
        elif user_input.lower() == "help":
            handle_command("help")
        else:
            loading_dots()
            analyze_sentiment(user_input)
# - Display a welcome message and introduce the Sentiment Spy activity
# - Ask the user for their name and store it in the `user_name` variable
# - Enter an infinite loop to interact with the user:
#   - Prompt the user to enter a sentence or command
#   - Check for empty input and prompt the user to enter a valid sentence
#   - If the input matches specific commands (`exit`, `summary`, `reset`, `history`, `help`), execute the corresponding functionality
#   - Otherwise, call the `analyze_sentiment` function to analyze the input text
#   - Display the sentiment analysis result with color-coded feedback
# - Exit the loop and display a final summary when the user types `exit`

# Define the entry point for the script
if __name__ == "__main__":
    """Entry point for the Sentiment Spy chatbot."""
    start_sentiment_chat()
# - Ensure the chatbot starts only when the script is run directly (not imported)
# - Call the `start_sentiment_chat` function to begin the activity
