# main.py

import re, random
from colorama import Fore, init

# Initialize colorama (autoreset ensures each print resets after use)
init(autoreset=True)

# Destination & joke data
destinations = {
    "beaches": ["Bali", "Maldives", "Phuket"],
    "mountains": ["Swiss Alps", "Rocky Mountains", "Himalayas"],
    "cities": ["Tokyo", "Paris", "New York"]
}
jokes = [
    "Why don't programmers like nature? Too many bugs!",
    "Why did the computer go to the doctor? Because it had a virus!",
    "Why do travelers always feel warm? Because of all their hot spots!"
]

# Helper function to normalize user input (remove extra spaces, make lowercase)
def normalize_input(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())

# -------- Travel Recommendations (recursive-style refinement) --------
def provide_recommendations():
    """
    Ask the user for a travel category and provide suggestions.
    If the user rejects the suggestions, allow them to refine or pick another category.
    """
    while True:
        print(Fore.CYAN + "Which kind of destination are you interested in? (beaches / mountains / cities)")
        cat_raw = input(Fore.YELLOW + "> ")
        category = normalize_input(cat_raw)

        if category not in destinations:
            print(Fore.RED + "Sorry, I only know: beaches, mountains, cities. Try one of those.")
            continue

        # Suggest places
        options = destinations[category]
        print(Fore.GREEN + f"My {category} picks: " + Fore.WHITE + ", ".join(options))

        # Ask user if they like these
        print(Fore.CYAN + "Do you like these suggestions? (yes / no)")
        ans_raw = input(Fore.YELLOW + "> ")
        ans = normalize_input(ans_raw)

        if ans in ("yes", "y", "yeah", "yep"):
            print(Fore.GREEN + "Awesome! Have a great trip!")
            return
        elif ans in ("no", "n", "nope", "nah"):
            print(Fore.MAGENTA + "No worries. Want to try another category or refine your choice?")
            print(Fore.CYAN + "Type a category name (beaches/mountains/cities) or 'exit' to stop recommendations.")
            follow_raw = input(Fore.YELLOW + "> ")
            follow = normalize_input(follow_raw)
            if follow == "exit":
                print(Fore.GREEN + "Got it. Exiting recommendations.")
                return
            if follow in destinations:
                # loop will continue and re-ask for category, but we can directly use this follow-up
                category = follow
                options = destinations[category]
                print(Fore.GREEN + f"How about these {category} picks: " + Fore.WHITE + ", ".join(options))
                print(Fore.CYAN + "Better? (yes / no)")
                again_raw = input(Fore.YELLOW + "> ")
                again = normalize_input(again_raw)
                if again in ("yes", "y"):
                    print(Fore.GREEN + "Great! Safe travels!")
                    return
                else:
                    # continue the outer loop to try again
                    continue
            else:
                # If they typed something else, loop back up
                continue
        else:
            print(Fore.RED + "Please answer with 'yes' or 'no'. Let's try again.")
            # loop continues

# -------- Packing Tips --------
def packing_tips():
    """
    Offer packing tips based on the user's chosen destination and trip duration.
    """
    print(Fore.CYAN + "What type of destination? (beaches / mountains / cities)")
    dest_raw = input(Fore.YELLOW + "> ")
    dest = normalize_input(dest_raw)

    if dest not in destinations:
        print(Fore.RED + "Sorry, I only have packing tips for: beaches, mountains, cities.")
        return

    print(Fore.CYAN + "Trip duration in days? (e.g., 3, 5, 7)")
    dur_raw = input(Fore.YELLOW + "> ")
    # Extract first integer found; default to 3 if none
    m = re.search(r"\d+", dur_raw)
    days = int(m.group()) if m else 3

    # Base items
    tips = ["Passport/ID", "Wallet & cards", "Phone & charger", "Basic meds", "Toiletries", "Reusable water bottle"]
    # Duration-based clothing heuristic
    tips.append(f"{max(2, days//2 + 1)} casual outfits")
    tips.append(f"{min(days, 7)} pairs of socks")
    tips.append(f"{min(days, 5)} sets of innerwear")
    tips.append("Comfortable walking shoes")

    # Destination-specific adds
    if dest == "beaches":
        tips += ["Swimwear", "Sunscreen (SPF 50+)", "Flip-flops", "Hat & sunglasses", "Light cotton clothes"]
    elif dest == "mountains":
        tips += ["Warm layers / fleece", "Rain jacket", "Hiking boots", "Woolen cap & gloves", "Thermal bottle"]
    elif dest == "cities":
        tips += ["City map / offline maps", "Dressy outfit (optional)", "Compact umbrella", "Small daypack"]

    print(Fore.GREEN + f"Packing tips for a {days}-day {dest} trip:")
    for i, item in enumerate(tips, 1):
        print(Fore.WHITE + f"{i}. {item}")

# -------- Tell a Random Joke --------
def tell_joke():
    print(Fore.GREEN + "Here's a joke for you:")
    print(Fore.WHITE + random.choice(jokes))

# -------- Display Help Menu --------
def show_help():
    print(Fore.CYAN + "I can help with these commands:")
    print(Fore.WHITE + "- 'recommend' or 'travel' → get destination suggestions")
    print(Fore.WHITE + "- 'pack' or 'packing tips' → get a packing checklist")
    print(Fore.WHITE + "- 'joke' → hear a random joke")
    print(Fore.WHITE + "- 'help' → show this menu")
    print(Fore.WHITE + "- 'exit' or 'quit' → leave the chatbot")

# -------- Main Chat Loop --------
def chat():
    print(Fore.GREEN + "Welcome to the Travel Buddy Chatbot!")
    print(Fore.GREEN + "Type 'help' to see what I can do.\n")

    try:
        while True:
            user_raw = input(Fore.YELLOW + "You: ")
            user = normalize_input(user_raw)

            if user in ("exit", "quit", "bye"):
                print(Fore.GREEN + "Goodbye! Safe travels!")
                break

            # Intent detection via simple keyword regex
            if re.search(r"\b(help|menu)\b", user):
                show_help()
            elif re.search(r"\b(recommend|suggest|travel|trip)\b", user):
                provide_recommendations()
            elif re.search(r"\b(pack|packing|checklist)\b", user):
                packing_tips()
            elif re.search(r"\b(joke|funny|laugh)\b", user):
                tell_joke()
            else:
                print(Fore.MAGENTA + "I'm not sure about that. Try 'help' to see options.")
    except KeyboardInterrupt:
        print("\n" + Fore.GREEN + "Interrupted. Goodbye!")
    except Exception as e:
        print(Fore.RED + f"Oops, something went wrong: {e}")

# Run the chatbot
if __name__ == "__main__":
    chat()
