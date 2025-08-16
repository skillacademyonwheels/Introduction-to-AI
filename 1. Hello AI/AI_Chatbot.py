print("Hello ! Welcome to the AI Chatbot.")

name = input("Please enter your name: ")

print(f"Nice to meet you, {name}!")

print("How are you feeling today?")
mood = input("Enter your mood (happy, sad, excited, etc.): ")
if mood.lower() in ["happy", "excited"]:
    print("That's great to hear! Keep smiling :)")
elif mood.lower() == "sad":
    print("I'm sorry to hear that. Remember, it's okay to feel sad sometimes.")
else:
    print("Thanks for sharing your mood with me!")

print("It was nice chatting with you, " + name + ". Have a great day!")