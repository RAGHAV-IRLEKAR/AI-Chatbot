import customtkinter as ctk
import threading
from tkinter import END

from chatbot import stream_ai_response, clear_chat as clear_ai_chat

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Student AI Chatbot")
app.geometry("700x650")
app.minsize(600, 550)

header = ctk.CTkFrame(app, corner_radius=0)
header.pack(fill="x")

title = ctk.CTkLabel(
    header,
    text="🎓 Student AI Chatbot",
    font=("Arial", 25, "bold"),
)
title.pack(pady=(15, 2))

subtitle = ctk.CTkLabel(
    header,
    text="Fast AI Assistant • Gemini 3.6 Flash",
    font=("Arial", 12),
)
subtitle.pack(pady=(0, 15))

chat_box = ctk.CTkTextbox(
    app,
    font=("Arial", 14),
    corner_radius=12,
    wrap="word",
)
chat_box.pack(fill="both", expand=True, padx=20, pady=15)

chat_box.insert(
    END,
    "🤖 Chatbot:\n"
    "Hello! 👋\n\n"
    "I'm your Student AI Assistant. "
    "Ask me about Java, Python, Android, science, "
    "mathematics or programming.\n\n",
)
chat_box.configure(state="disabled")

input_frame = ctk.CTkFrame(app, fg_color="transparent")
input_frame.pack(fill="x", padx=20, pady=(0, 10))

user_entry = ctk.CTkEntry(
    input_frame,
    placeholder_text="Type your question...",
    height=45,
    font=("Arial", 14),
    corner_radius=10,
)
user_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

def insert_text(text):
    chat_box.configure(state="normal")
    chat_box.insert(END, text)
    chat_box.configure(state="disabled")
    chat_box.see(END)

def update_bot_response(text):
    app.after(0, insert_text, text)

def finish_response():
    chat_box.configure(state="normal")
    chat_box.insert(END, "\n\n")
    chat_box.configure(state="disabled")
    chat_box.see(END)

    send_button.configure(state="normal", text="Send ➤")
    user_entry.configure(state="normal")
    user_entry.focus()

def response_finished(_full_response):
    app.after(0, finish_response)

def get_response(user_text):
    stream_ai_response(
        user_text,
        update_bot_response,
        response_finished,
    )

def send_message():
    user_text = user_entry.get().strip()

    if not user_text:
        return

    chat_box.configure(state="normal")
    chat_box.insert(END, f"👤 You:\n{user_text}\n\n")
    chat_box.insert(END, "🤖 Chatbot: ")
    chat_box.configure(state="disabled")
    chat_box.see(END)

    user_entry.delete(0, END)

    send_button.configure(state="disabled", text="Thinking...")
    user_entry.configure(state="disabled")

    threading.Thread(
        target=get_response,
        args=(user_text,),
        daemon=True,
    ).start()

def clear_chat():
    clear_ai_chat()

    chat_box.configure(state="normal")
    chat_box.delete("1.0", END)
    chat_box.insert(
        END,
        "🤖 Chatbot:\n"
        "Chat cleared! 🧹\n\n"
        "Ask me a new question.\n\n",
    )
    chat_box.configure(state="disabled")

send_button = ctk.CTkButton(
    input_frame,
    text="Send ➤",
    width=105,
    height=45,
    corner_radius=10,
    font=("Arial", 14, "bold"),
    command=send_message,
)
send_button.pack(side="right")

clear_button = ctk.CTkButton(
    app,
    text="Clear Chat",
    width=120,
    height=35,
    command=clear_chat,
)
clear_button.pack(pady=(0, 12))

user_entry.bind("<Return>", lambda event: send_message())
user_entry.focus()

app.mainloop()
