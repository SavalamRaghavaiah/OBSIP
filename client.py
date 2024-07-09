
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import emoji

HOST = '127.0.0.1'
PORT = 1489

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add(message, tag=None):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + "\n", tag)
    message_box.config(state=tk.DISABLED)
    message_box.see(tk.END)  

def connect():
    try:
        client.connect((HOST, PORT))
        username = username_textbox.get()
        if username:
            client.sendall(username.encode())
            username_textbox.config(state=tk.DISABLED)
            username_button.config(state=tk.DISABLED)
            threading.Thread(target=listen_for_messages_from_server).start()
        else:
            messagebox.showerror("Error", "Username should not be empty")
    except Exception as e:
        messagebox.showerror("Error", f"Unable to connect to server: {e}")

def send_message():
    message = message_textbox.get()
    if message:
        client.sendall(emoji.demojize(message).encode())
        add(f"You ~ {message}", 'user_message')
        message_textbox.delete(0, tk.END)

def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        message = f"Uploaded file: {file_path}"
        add(f"You ~ {message}", 'user_message')

def listen_for_messages_from_server():
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                username, content = message.split('~')
                add(f"[{username}] ~ {content}", 'user_message')
        except:
            break

root = tk.Tk()
root.geometry("800x600")
root.title('Chat Application')
root.resizable(False, False)

root.configure(bg='#2F3136')

username_frame = tk.Frame(root, bg='#2F3136')
username_frame.pack(pady=10)

tk.Label(username_frame, text="Enter Username: ", font=("Helvetica", 12), bg='#2F3136', fg='#4CAF50').pack(side=tk.LEFT, padx=10)
username_textbox = tk.Entry(username_frame, font=("Helvetica", 12), width=23)
username_textbox.pack(side=tk.LEFT, padx=10)

username_button = tk.Button(username_frame, text="Join", command=connect, font=("Helvetica", 10), bg='#4CAF50', fg='#E5E5EA')
username_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(root, font=("Helvetica", 10), bg='#E5E5EA', fg='#555555', width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(pady=10)

message_textbox = tk.Entry(root, font=("Helvetica", 12), width=38)
message_textbox.pack(pady=10, padx=10, side=tk.LEFT)

tk.Button(root, text="Send", command=send_message, font=("Helvetica", 10), bg='#4CAF50', fg='#E5E5EA').pack(pady=10, side=tk.LEFT)
tk.Button(root, text="Upload", command=upload_file, font=("Helvetica", 10), bg='#4CAF50', fg='#E5E5EA').pack(pady=10, side=tk.LEFT)

root.mainloop()