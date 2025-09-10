import sys
import time
import re
from textblob import TextBlob
from colorama import Fore, Style, init

init(autoreset=True)

# Data storage
conversation_history = []
sentiment_stats = {
    "positive": 0,
    "negative": 0,
    "neutral": 0,
    "total_sentences": 0
}
user_name = ""

def show_processing_animation():
    animation = "|/-\\"
    for i in range(10):
        time.sleep(0.1)
        sys.stdout.write(f"\rAnalyzing... {animation[i % len(animation)]}")
        sys.stdout.flush()
    sys.stdout.write("\r              \r")

def get_valid_name():
    global user_name
    while True:
        name = input("Hello there! What's your name? ")
        if re.fullmatch(r"[a-zA-Z]+", name):
            user_name = name
            print(f"Welcome, {user_name}! I'm a sentiment analysis bot.")
            print("You can tell me anything, and I'll analyze the sentiment. Type 'help' for a list of commands.")
            break
        else:
            print("Please enter a name with only alphabetic characters.")

def analyze_sentiment(text):
    analysis = TextBlob(text)
    
    if analysis.sentiment.polarity > 0:
        return "positive", Fore.GREEN
    elif analysis.sentiment.polarity < 0:
        return "negative", Fore.RED
    else:
        return "neutral", Fore.YELLOW

def execute_command(command):
    global conversation_history
    global sentiment_stats
    
    if command == "summary":
        total = sentiment_stats["total_sentences"]
        if total > 0:
            pos_percent = (sentiment_stats["positive"] / total) * 100
            neg_percent = (sentiment_stats["negative"] / total) * 100
            neu_percent = (sentiment_stats["neutral"] / total) * 100
            print(f"\nTotal Sentences Analyzed: {total}")
            print(f"{Fore.GREEN}Positive: {sentiment_stats['positive']} ({pos_percent:.2f}%)")
            print(f"{Fore.RED}Negative: {sentiment_stats['negative']} ({neg_percent:.2f}%)")
            print(f"{Fore.YELLOW}Neutral: {sentiment_stats['neutral']} ({neu_percent:.2f}%)")
        else:
            print("No sentences have been analyzed yet.")
    
    elif command == "reset":
        conversation_history.clear()
        sentiment_stats = {
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "total_sentences": 0
        }
        print("\nAll data has been reset.")
    
    elif command == "history":
        if conversation_history:
            print("\n--- Conversation History ---")
            for entry in conversation_history:
                print(entry)
        else:
            print("The conversation history is empty.")
    
    elif command == "help":
        print("\nAvailable commands:")
        print("  summary: Shows a summary of sentiment statistics.")
        print("  history: Displays all previous messages and their sentiment analyses.")
        print("  reset: Clears all stored data and history.")
        print("  exit: Ends the chat and generates a final report.")
    
    else:
        return False
    
    return True

def generate_report():
    report_filename = f"{user_name}_sentiment_analysis.txt"
    with open(report_filename, "w") as file:
        file.write("--- Final Sentiment Analysis Report ---\n\n")
        file.write("Sentiment Summary:\n")
        total = sentiment_stats["total_sentences"]
        if total > 0:
            file.write(f"Total Sentences Analyzed: {total}\n")
            file.write(f"Positive: {sentiment_stats['positive']}\n")
            file.write(f"Negative: {sentiment_stats['negative']}\n")
            file.write(f"Neutral: {sentiment_stats['neutral']}\n")
        else:
            file.write("No sentences were analyzed.\n")
        file.write("\nConversation History:\n")
        for entry in conversation_history:
            file.write(f"{entry}\n")
    print(f"\nFinal report saved to {report_filename}")

def main_chatbot_loop():
    get_valid_name()
    
    while True:
        try:
            user_input = input("\n> ")
            
            if user_input.lower() == "exit":
                generate_report()
                print("Goodbye! 👋")
                sys.exit()
            
            if execute_command(user_input.lower()):
                continue
            
            show_processing_animation()
            
            sentiment, color = analyze_sentiment(user_input)
            
            print(f"{color}Sentiment: {sentiment.capitalize()}{Style.RESET_ALL}")
            
            conversation_history.append(f"User: {user_input} | Sentiment: {sentiment.capitalize()}")
            sentiment_stats[sentiment] += 1
            sentiment_stats["total_sentences"] += 1

        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! 👋")
            sys.exit()
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main_chatbot_loop()