import json
from difflib import get_close_matches



def load_knowledge_base(file_path: str) -> dict:
    """
    This function loads the knowledge base from the specified JSON file path.

    Parameters:
    - file_path (str): The path to the JSON file containing the knowledge base data.

    Returns:
    - dict: A dictionary containing the knowledge base data loaded from the specified JSON file.

    The function uses the built-in json.load() function to load the data from the specified JSON file into a dictionary.
    """
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data
def save_knowledge_base(file_path: str, data: dict) -> None:
    """
    This function saves the given data dictionary to the specified file path in JSON format.

    Parameters:
    - file_path (str): The path to the file where the data will be saved.
    - data (dict): The data to be saved in the JSON format.

    Returns:
    - None: This function does not return any value.

    The function uses the built-in json.dump() function to save the data to the specified file in JSON format. The indent parameter is set to 2 to format the JSON output with indentation for better readability.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    """
    This function finds the best match for the user's input in the given list of questions.

    Parameters:
    - user_question (str): The user's input question.
    - questions (list[str]): A list of questions to search for a match.

    Returns:
    - str | None: The best matching question from the list, or None if no match is found.

    The function uses the difflib.get_close_matches function to find the closest match between the user's input and the questions in the list. It returns the first match found, or None if no match is found.
    """
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    """
    This function searches the knowledge base for a matching question and returns the corresponding answer.

    Parameters:
    - question (str): The user's input question.
    - knowledge_base (dict): A dictionary containing the knowledge base data.

    Returns:
    - str | None: The answer to the user's question if found in the knowledge base, otherwise None.

    The function iterates through the "questions" list in the knowledge_base dictionary. If it finds a question that matches the user's input, it returns the corresponding answer. If no matching question is found, it returns None.
    """
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def chat_bot():
   

    knowledge_base = load_knowledge_base('knowledge_base.json')  # Load the knowledge base from the JSON file
    while True:
        user_input = input("You: ")  # Prompt the user for input

        if user_input.lower() == 'quit':  # Check if the user wants to quit
            break

        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])  # Find the best match for the user's input in the knowledge base

        if best_match:  # If a match is found
            answer = get_answer_for_question(best_match, knowledge_base)  # Get the answer for the best match
            print(f"Bot: {answer}")  # Print the answer
        else:  # If no match is found
            print("Bot: I don't know the answer, can you teach me?")  # Prompt the user to teach the bot
            new_answer = input("Type the answer or write down skip: ")  # Get the user's input

            if new_answer.lower() != "skip":  # If the user didn't input "skip"
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})  # Add the new question and answer to the knowledge base
                save_knowledge_base("knowledge_base.json", knowledge_base)  # Save the updated knowledge base to the JSON file
                print("Bot: Thank you, I have learned a new response.")  # Thank the user for teaching the bot

if __name__ == '__main__':
   
    chat_bot()
    




        
