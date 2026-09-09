import customtkinter as ctk
import threading
import urllib.request
import urllib.error
import json
from tkinter import END

# ==========================================
# 1. GEMINI API CONFIGURATION
# ==========================================

API_KEY = "AIzaSyAyLTglaYYtFlFQqKEsIS8ixDD0YVzgkLQ"

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

chat_history = []


# ==========================================
# 2. AI RESPONSE FUNCTION
# ==========================================

def get_ai_response(user_text):                                     #used to send text to ai

    global chat_history

    chat_history.append({                                           #adds user msg  to the conversation
        "role": "user",
        "parts": [{"text": user_text}]
    })

    data_dict = {
        "contents": chat_history
    }

    data_bytes = json.dumps(data_dict).encode('utf-8')               #used to convert text into json

    req = urllib.request.Request(API_URL, data=data_bytes, method='POST')     #generates request
    req.add_header('Content-Type', 'application/json')

    try:
        with urllib.request.urlopen(req, timeout=15) as response:  #if above timeout session ends

            response_data = response.read().decode('utf-8')    #converts byte into text
            response_json = json.loads(response_data)          #convert json into python

            ai_reply = response_json['candidates'][0]['content']['parts'][0]['text']

            chat_history.append({                              #add message from ai to chatbox
                "role": "model",
                "parts": [{"text": ai_reply}]
            })

            return ai_reply.strip()

    except urllib.error.HTTPError as e:                        #handles api errors
        error_details = e.read().decode('utf-8')
        chat_history.pop()
        return f"\n[API ERROR {e.code}]: {error_details}"

    except urllib.error.URLError:                              #handles network error
        chat_history.pop()
        return "\n[NETWORK ERROR]: Check your internet connection."

    except Exception as e:                                     #handles unexpected error
        chat_history.pop()
        return f"\n[SYSTEM ERROR]: {e}"


# 3. UI SETTINGS 

ctk.set_appearance_mode("dark")               #defines theme and color of theme
ctk.set_default_color_theme("dark-blue")


# 4. MAIN WINDOW

app = ctk.CTk()                            #creates and defines geometry of chatbot window
app.title("Student AI Chatbot")
app.geometry("600x600")


# TITLE

title = ctk.CTkLabel(                         #sets text label 
    app,
    text="🎓 Student AI Chatbot",
    font=("Arial", 22, "bold")
)

title.pack(pady=10)                          #adds padding 


# CHAT DISPLAY

chat_box = ctk.CTkTextbox(                  #adds a chatbox 
    app,
    width=550,
    height=420,
    font=("Arial", 14)
)

chat_box.pack(pady=10)                      #adds padding

chat_box.insert(END, "Chatbot: Hello! Ask me anything about science, maths or programming.\n\n")        #default msg
chat_box.configure(state="disabled")


# INPUT FRAME

input_frame = ctk.CTkFrame(app)                               #adds a textbox for user to enter
input_frame.pack(pady=10, fill="x", padx=10)


user_entry = ctk.CTkEntry(                                  #we can insert text using this function
    input_frame,
    placeholder_text="Type your question...",
    width=420
)

user_entry.pack(side="left", padx=10, pady=10)


# SEND MESSAGE FUNCTION

def send_message():

    user_text = user_entry.get()                #fetches msg from input frame

    if user_text.strip() == "":
        return                                 #check empty strings

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


# CLEAR CHAT FUNCTION (NEW)

def clear_chat():
    global chat_history
    chat_history = []

    chat_box.configure(state="normal")
    chat_box.delete("1.0", END)
    chat_box.insert(END, "Chatbot: Chat cleared! Ask a new question.\n\n")
    chat_box.configure(state="disabled")


# SEND BUTTON

send_button = ctk.CTkButton(
    input_frame,
    text="Send",
    width=100,
    command=send_message
)

send_button.pack(side="right", padx=10)


# CLEAR CHAT BUTTON (NEW)

clear_button = ctk.CTkButton(
    app,
    text="Clear Chat",
    width=120,
    command=clear_chat
)

clear_button.pack(pady=5)


# # ENTER KEY SUPPORT

app.bind("<Return>", lambda event: send_message())


# RUN APPLICATION

app.mainloop()