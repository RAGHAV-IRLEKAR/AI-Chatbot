import customtkinter as ctk
import threading
from tkinter import END

# import your AI function file OR paste your code above this GUI
# make sure get_ai_response() function exists
from mp1 import get_ai_response   # if your AI code is in chatbot.py


# ------------------------------
# UI SETTINGS
# ------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ------------------------------
# MAIN WINDOW
# ------------------------------
app = ctk.CTk()
app.title("Student AI Chatbot")
app.geometry("600x600")


# ------------------------------
# TITLE
# ------------------------------
title = ctk.CTkLabel(
    app,
    text="🎓 Student AI Chatbot",
    font=("Arial", 22, "bold")
)
title.pack(pady=10)


# ------------------------------
# CHAT DISPLAY
# ------------------------------
chat_box = ctk.CTkTextbox(
    app,
    width=550,
    height=420,
    font=("Arial", 14)
)
chat_box.pack(pady=10)

chat_box.insert(END, "Chatbot: Hello! Ask me anything about science, maths or programming.\n\n")
chat_box.configure(state="disabled")


# ------------------------------
# INPUT FRAME
# ------------------------------
input_frame = ctk.CTkFrame(app)
input_frame.pack(pady=10, fill="x", padx=10)


user_entry = ctk.CTkEntry(
    input_frame,
    placeholder_text="Type your question...",
    width=420
)
user_entry.pack(side="left", padx=10, pady=10)


# ------------------------------
# SEND MESSAGE FUNCTION
# ------------------------------
def send_message():
    user_text = user_entry.get()

    if user_text.strip() == "":
        return

    chat_box.configure(state="normal")
    chat_box.insert(END, f"You: {user_text}\n")
    chat_box.configure(state="disabled")

    user_entry.delete(0, END)

    threading.Thread(target=get_response, args=(user_text,)).start()


def get_response(user_text):
    response = get_ai_response(user_text)

    chat_box.configure(state="normal")
    chat_box.insert(END, f"Chatbot: {response}\n\n")
    chat_box.configure(state="disabled")
    chat_box.see(END)


# ------------------------------
# SEND BUTTON
# ------------------------------
send_button = ctk.CTkButton(
    input_frame,
    text="Send",
    width=100,
    command=send_message
)
send_button.pack(side="right", padx=10)


# ------------------------------
# ENTER KEY SUPPORT
# ------------------------------
app.bind("<Return>", lambda event: send_message())


# ------------------------------
# RUN APP
# ------------------------------
app.mainloop()