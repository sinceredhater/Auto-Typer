import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import keyboard
import sys
from datetime import datetime

class AutoTyperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto-Typer GUI")
        self.root.geometry("500x600")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.is_running = False
        self.typing_thread = None
        self.message_var = tk.StringVar(value="")
        self.interval_var = tk.StringVar(value="3")
        self.countdown_var = tk.StringVar(value="5")
        self.status_var = tk.StringVar(value="Ready")
        self.count_var = tk.StringVar(value="Messages sent: 0")
        
        self.message_count = 0
        
        # Style configuration
        self.setup_styles()
        
        # Create GUI elements
        self.create_widgets()
        
        # Center the window
        self.center_window()
        
    def setup_styles(self):
        """Configure ttk styles for better appearance"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'), 
                       background='#2c3e50', 
                       foreground='#ecf0f1')
        
        style.configure('Custom.TLabel', 
                       font=('Arial', 10), 
                       background='#2c3e50', 
                       foreground='#ecf0f1')
        
        style.configure('Status.TLabel', 
                       font=('Arial', 10, 'bold'), 
                       background='#2c3e50', 
                       foreground='#e74c3c')
        
        style.configure('Count.TLabel', 
                       font=('Arial', 12, 'bold'), 
                       background='#2c3e50', 
                       foreground='#27ae60')
        
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c3e50', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="🤖 Auto-Typer GUI", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Message input section
        message_frame = tk.LabelFrame(main_frame, text="Message Settings", 
                                    bg='#34495e', fg='#ecf0f1', font=('Arial', 10, 'bold'))
        message_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(message_frame, text="Message to type:", style='Custom.TLabel').pack(anchor='w', padx=10, pady=(10, 5))
        
        message_entry = tk.Entry(message_frame, textvariable=self.message_var, 
                               font=('Arial', 11), bg='#ecf0f1', fg='#2c3e50')
        message_entry.pack(fill='x', padx=10, pady=(0, 10))
        
        # Timing settings section
        timing_frame = tk.LabelFrame(main_frame, text="Timing Settings", 
                                   bg='#34495e', fg='#ecf0f1', font=('Arial', 10, 'bold'))
        timing_frame.pack(fill='x', pady=(0, 15))
        
        # Interval setting
        interval_row = tk.Frame(timing_frame, bg='#34495e')
        interval_row.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(interval_row, text="Interval (seconds):", style='Custom.TLabel').pack(side='left')
        
        interval_spinbox = tk.Spinbox(interval_row, from_=1, to=60, textvariable=self.interval_var,
                                    width=10, font=('Arial', 10), bg='#ecf0f1', fg='#2c3e50')
        interval_spinbox.pack(side='right')
        
        # Countdown setting
        countdown_row = tk.Frame(timing_frame, bg='#34495e')
        countdown_row.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(countdown_row, text="Start countdown (seconds):", style='Custom.TLabel').pack(side='left')
        
        countdown_spinbox = tk.Spinbox(countdown_row, from_=0, to=30, textvariable=self.countdown_var,
                                     width=10, font=('Arial', 10), bg='#ecf0f1', fg='#2c3e50')
        countdown_spinbox.pack(side='right')
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(fill='x', pady=15)
        
        self.start_button = tk.Button(button_frame, text="▶ Start Auto-Typer", 
                                    command=self.start_typing, font=('Arial', 12, 'bold'),
                                    bg='#27ae60', fg='white', relief='raised', bd=3)
        self.start_button.pack(side='left', padx=(0, 10), fill='x', expand=True)
        
        self.stop_button = tk.Button(button_frame, text="⏸ Stop Auto-Typer", 
                                   command=self.stop_typing, font=('Arial', 12, 'bold'),
                                   bg='#e74c3c', fg='white', relief='raised', bd=3, state='disabled')
        self.stop_button.pack(side='right', padx=(10, 0), fill='x', expand=True)
        
        # Status section
        status_frame = tk.LabelFrame(main_frame, text="Status", 
                                   bg='#34495e', fg='#ecf0f1', font=('Arial', 10, 'bold'))
        status_frame.pack(fill='x', pady=(0, 15))
        
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, style='Status.TLabel')
        self.status_label.pack(pady=10)
        
        self.count_label = ttk.Label(status_frame, textvariable=self.count_var, style='Count.TLabel')
        self.count_label.pack(pady=(0, 10))
        
        # Instructions section
        instructions_frame = tk.LabelFrame(main_frame, text="Instructions", 
                                         bg='#34495e', fg='#ecf0f1', font=('Arial', 10, 'bold'))
        instructions_frame.pack(fill='both', expand=True)
        
        instructions_text = """
1. Enter the message you want to auto-type
2. Set the interval between messages
3. Set countdown time to switch to target window
4. Click 'Start Auto-Typer'
5. Quickly switch to your target application
6. Press ESC key anytime to stop typing
7. Or use the 'Stop' button in this window

⚠️ Use responsibly and ensure you have permission!
        """
        
        instructions_label = tk.Label(instructions_frame, text=instructions_text.strip(), 
                                    justify='left', bg='#34495e', fg='#bdc3c7', 
                                    font=('Arial', 9), wraplength=450)
        instructions_label.pack(padx=10, pady=10, anchor='w')
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def start_typing(self):
        """Start the auto-typing process"""
        if self.is_running:
            return
            
        try:
            interval = float(self.interval_var.get())
            countdown = int(self.countdown_var.get())
            message = self.message_var.get().strip()
            
            if not message:
                messagebox.showerror("Error", "Please enter a message to type!")
                return
                
            if interval < 0.1:
                messagebox.showerror("Error", "Interval must be at least 0.1 seconds!")
                return
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for interval and countdown!")
            return
        
        self.is_running = True
        self.message_count = 0
        self.update_count()
        
        # Update button states
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        
        # Start typing in a separate thread
        self.typing_thread = threading.Thread(target=self.typing_worker, 
                                            args=(message, interval, countdown), 
                                            daemon=True)
        self.typing_thread.start()
        
    def stop_typing(self):
        """Stop the auto-typing process"""
        self.is_running = False
        self.status_var.set("Stopping...")
        
        # Update button states
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        
    def typing_worker(self, message, interval, countdown):
        """Worker thread for auto-typing"""
        try:
            # Countdown phase
            if countdown > 0:
                for i in range(countdown, 0, -1):
                    if not self.is_running:
                        return
                    self.status_var.set(f"Starting in {i} seconds... Switch to target window!")
                    time.sleep(1)
            
            if not self.is_running:
                return
                
            self.status_var.set("Auto-typing active! Press ESC to stop.")
            
            # Main typing loop
            while self.is_running:
                try:
                    # Check if ESC is pressed
                    if keyboard.is_pressed('esc'):
                        self.status_var.set("Stopped by ESC key")
                        break
                    
                    # Type the message
                    keyboard.write(message)
                    keyboard.press_and_release('enter')
                    
                    # Update counter
                    self.message_count += 1
                    self.update_count()
                    
                    # Wait for the specified interval
                    start_time = time.time()
                    while time.time() - start_time < interval and self.is_running:
                        if keyboard.is_pressed('esc'):
                            self.status_var.set("Stopped by ESC key")
                            self.is_running = False
                            break
                        time.sleep(0.1)  # Small sleep to prevent high CPU usage
                        
                except Exception as e:
                    self.status_var.set(f"Error: {str(e)}")
                    break
                    
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
        finally:
            self.cleanup()
            
    def update_count(self):
        """Update the message counter display"""
        self.count_var.set(f"Messages sent: {self.message_count}")
        
    def cleanup(self):
        """Clean up when stopping"""
        self.is_running = False
        
        # Update UI on main thread
        self.root.after(0, lambda: [
            self.start_button.config(state='normal'),
            self.stop_button.config(state='disabled'),
            self.status_var.set("Ready") if self.status_var.get() == "Stopping..." else None
        ])
        
    def on_closing(self):
        """Handle window closing"""
        if self.is_running:
            if messagebox.askokcancel("Quit", "Auto-typer is running. Do you want to quit?"):
                self.stop_typing()
                self.root.after(500, self.root.destroy)  # Give time for cleanup
        else:
            self.root.destroy()

def main():
    """Main function to run the application"""
    try:
        # Test if keyboard library is available
        import keyboard
    except ImportError:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror("Missing Dependency", 
                           "The 'keyboard' library is required.\n\n" +
                           "Please install it using:\n" +
                           "pip install keyboard")
        root.destroy()
        return
    
    # Create and run the application
    root = tk.Tk()
    app = AutoTyperGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Make window resizable but set minimum size
    root.minsize(400, 500)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Error running application: {e}")

if __name__ == "__main__":
    main()
