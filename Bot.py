import tkinter as tk
from tkinter import ttk
import threading
import time
import random
import requests
import pyautogui
import pygetwindow as gw

class WhiteSurvivalBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Whiteout Survival Bot - Setup")
        
        # Notebook for tabs
        self.tab_control = ttk.Notebook(root)
        
        # Define Tabs
        self.setup_tab = ttk.Frame(self.tab_control)
        self.resource_tab = ttk.Frame(self.tab_control)
        self.shelter_tab = ttk.Frame(self.tab_control)
        self.exploration_tab = ttk.Frame(self.tab_control)
        self.darklings_tab = ttk.Frame(self.tab_control)
        self.alliance_tab = ttk.Frame(self.tab_control)
        self.chat_tab = ttk.Frame(self.tab_control)

        # Adding tabs
        self.tab_control.add(self.setup_tab, text="Setup")
        self.tab_control.add(self.resource_tab, text="Resources")
        self.tab_control.add(self.shelter_tab, text="Shelter Upgrades")
        self.tab_control.add(self.exploration_tab, text="Exploration")
        self.tab_control.add(self.darklings_tab, text="Darklings Combat")
        self.tab_control.add(self.alliance_tab, text="Alliance Support")
        self.tab_control.add(self.chat_tab, text="Chat with GPT")

        # Define Actions on each tab
        self.init_setup_tab()
        self.init_resource_tab()
        self.init_shelter_tab()
        self.init_exploration_tab()
        self.init_darklings_tab()
        self.init_alliance_tab()
        self.init_chat_tab()
        
        # Activity log
        self.activity_log = tk.Text(root, height=15, width=60)
        self.activity_log.pack(pady=10)
        
        # Start/Stop buttons
        self.start_button = tk.Button(root, text="Start", command=self.start_bot)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_bot)
        self.stop_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Initialize bot state
        self.running = False
        self.tab_control.pack(expand=1, fill="both")

        # Check initial setup
        self.check_ldplayer_setup()

    def log_activity(self, message):
        """Log messages in the activity log."""
        self.activity_log.insert(tk.END, message + "\n")
        self.activity_log.see(tk.END)

    def init_setup_tab(self):
        """Setup instructions and actions to check LDPlayer connection."""
        self.ldplayer_status = tk.StringVar(value="Checking LDPlayer...")
        tk.Label(self.setup_tab, text="LDPlayer Connection Status:").pack(anchor="w")
        tk.Label(self.setup_tab, textvariable=self.ldplayer_status).pack(anchor="w")
        
        # Button to manually retry connection
        self.retry_button = tk.Button(self.setup_tab, text="Retry Connection", command=self.check_ldplayer_setup)
        self.retry_button.pack(anchor="w", pady=5)

    def check_ldplayer_setup(self):
        """Check if LDPlayer is running."""
        if self.is_ldplayer_running():
            self.ldplayer_status.set("LDPlayer is running.")
            self.log_activity("LDPlayer detected and ready to run the bot.")
        else:
            self.ldplayer_status.set("LDPlayer not detected. Ensure it's running.")
            self.log_activity("Error: LDPlayer not detected. Please start LDPlayer.")

    def is_ldplayer_running(self):
        """Check if LDPlayer is running."""
        return any("LDPlayer" in window.title for window in gw.getAllWindows())

    def init_resource_tab(self):
        """Resource gathering options."""
        self.gather_wood = tk.BooleanVar()
        self.gather_food = tk.BooleanVar()
        tk.Checkbutton(self.resource_tab, text="Gather Wood", variable=self.gather_wood).pack(anchor="w")
        tk.Checkbutton(self.resource_tab, text="Gather Food", variable=self.gather_food).pack(anchor="w")
    
    def init_shelter_tab(self):
        """Shelter upgrade options."""        
        self.upgrade_shelter = tk.BooleanVar()
        self.train_troops = tk.BooleanVar()
        tk.Checkbutton(self.shelter_tab, text="Upgrade Shelter", variable=self.upgrade_shelter).pack(anchor="w")
        tk.Checkbutton(self.shelter_tab, text="Train Troops", variable=self.train_troops).pack(anchor="w")
    
    def init_exploration_tab(self):
        """Exploration options.""" 
        self.send_on_exploration = tk.BooleanVar()
        tk.Checkbutton(self.exploration_tab, text="Send on Exploration", variable=self.send_on_exploration).pack(anchor="w")
    
    def init_darklings_tab(self):
        """Darklings combat options.""" 
        self.fight_darklings = tk.BooleanVar()
        tk.Checkbutton(self.darklings_tab, text="Fight Darklings", variable=self.fight_darklings).pack(anchor="w")
    
    def init_alliance_tab(self):
        """Alliance support options.""" 
        self.send_alliance_help = tk.BooleanVar()
        tk.Checkbutton(self.alliance_tab, text="Send Alliance Help", variable=self.send_alliance_help).pack(anchor="w")

    def init_chat_tab(self):
        """Chat with GPT options."""
        self.chat_input = tk.Entry(self.chat_tab, width=50)
        self.chat_input.pack(pady=5)

        self.chat_button = tk.Button(self.chat_tab, text="Send", command=self.send_chatgpt_message)
        self.chat_button.pack(pady=5)

        self.chat_output = tk.Text(self.chat_tab, height=10, width=60)
        self.chat_output.pack(pady=5)

    def send_chatgpt_message(self):
        """Send message to ChatGPT and get the response."""
        user_input = self.chat_input.get()
        self.chat_output.insert(tk.END, "You: " + user_input + "\n")
        self.chat_input.delete(0, tk.END)

        response = self.get_chatgpt_response(user_input)
        self.chat_output.insert(tk.END, "ChatGPT: " + response + "\n")
    
    def get_chatgpt_response(self, prompt):
        """Send a prompt to ChatGPT and get the response."""
        headers = {
            'Authorization': 'Bearer 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',  # Replace with your actual API key
            'Content-Type': 'application/json',
        }
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': prompt}],
        }
        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            response.raise_for_status()
            response_json = response.json()
            return response_json['choices'][0]['message']['content'] if 'choices' in response_json and len(response_json['choices']) > 0 else "Error: No choices found."
        except requests.exceptions.RequestException as e:
            return f"Request failed: {e}"

    def start_bot(self):
        """Start bot operations."""    
        if "LDPlayer is running." not in self.ldplayer_status.get():
            self.log_activity("Cannot start bot: LDPlayer is not running.")
            return
        self.running = True
        self.log_activity("Bot started.")
        self.bot_thread = threading.Thread(target=self.run_bot)
        self.bot_thread.start()
    
    def stop_bot(self):
        """Stop bot operations."""  
        self.running = False
        self.log_activity("Bot stopped.")
    
    def run_bot(self):
        """Main bot logic to execute selected actions.""" 
        while self.running:
            if self.gather_wood.get():
                self.log_activity("Gathering Wood...")
                self.safe_tap(100, 200)  # Replace with actual coordinates
            if self.gather_food.get():
                self.log_activity("Gathering Food...")
                self.safe_tap(300, 400)  # Replace with actual coordinates
            time.sleep(random.uniform(1, 3))

    def safe_tap(self, x, y):
        """Perform a safe tap with delay to avoid detection.""" 
        pyautogui.click(x, y)
        delay = random.uniform(0.5, 2)
        self.log_activity(f"Tapped at ({x}, {y}), delaying {delay:.2f} seconds.")
        time.sleep(delay)

# Main
if __name__ == "__main__":
    root = tk.Tk()
    bot = WhiteSurvivalBot(root)
    root.mainloop()
