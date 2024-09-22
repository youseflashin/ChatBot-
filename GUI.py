import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from main import load_knowledge_base,save_knowledge_base,find_best_match,get_answer_for_question



def chat_bot_gui():
    knowledge_base = load_knowledge_base('knowledge_base.json')

    def send_message():
        user_input = user_entry.get()
        if not user_input:
            return

        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, f"You: {user_input}\n")
        chat_log.config(state=tk.DISABLED)

        user_entry.delete(0, tk.END)

        if user_input.lower() == 'quit':
            root.quit()
            return

        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(tk.END, f"Bot: {answer}\n")
            chat_log.config(state=tk.DISABLED)
        else:
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(tk.END, "Bot: I don't know the answer, can you teach me?\n")
            chat_log.config(state=tk.DISABLED)
            new_answer = simpledialog.askstring("Teach me", "Type the answer or write down skip:")
            if new_answer and new_answer.lower() != "skip":
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base("knowledge_base.json", knowledge_base)
                chat_log.config(state=tk.NORMAL)
                chat_log.insert(tk.END, "Bot: Thank you, I have learned a new response.\n")
                chat_log.config(state=tk.DISABLED)

    root = tk.Tk()
    root.title("Chatbot")
    root.configure(bg="black")

    chat_label = tk.Label(root, text="Chatbot", bg="black", fg="white", font=("Arial", 16))
    chat_label.pack(pady=(10, 0))

    messages_label = tk.Label(root, text="Chat Messages", bg="black", fg="white", font=("Arial", 12))
    messages_label.pack(padx=10, pady=(10, 0), anchor="w")

    chat_log = scrolledtext.ScrolledText(root, state=tk.DISABLED, bg="white", fg="black")
    chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    user_entry = tk.Entry(root, width=100, bg="white", fg="black")
    user_entry.pack(padx=10, pady=10, side=tk.LEFT, expand=True)

    button_frame = tk.Frame(root, bg="black")
    button_frame.pack(padx=10, pady=10, side=tk.RIGHT)

    send_button = tk.Button(button_frame, text="Send", command=send_message, bg="black", fg="white")
    send_button.pack(side=tk.LEFT, padx=(0, 5))

    exit_button = tk.Button(button_frame, text="Exit", command=root.quit, bg="black", fg="white")
    exit_button.pack(side=tk.LEFT)

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == '__main__':
    chat_bot_gui()




