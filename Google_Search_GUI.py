"""
Google Search Script - Command Line and GUI Interface
Supports searching for names or any query on Google
"""
# Author: Arshia Keshvari
# Date: 2025-05-27

import webbrowser
import urllib.parse
import argparse
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import threading

class GoogleSearcher:
    def __init__(self):
        self.base_url = "https://www.google.com/search?q="
    
    def search(self, query):
        """Perform Google search by opening browser"""
        if not query.strip():
            return False, "Query cannot be empty"
        
        # Encode the query for URL
        encoded_query = urllib.parse.quote_plus(query.strip())
        search_url = self.base_url + encoded_query
        
        try:
            webbrowser.open(search_url)
            return True, f"Opened Google search for: {query}"
        except Exception as e:
            return False, f"Error opening browser: {str(e)}"

class GoogleSearchGUI:
    def __init__(self, root):
        self.root = root
        self.searcher = GoogleSearcher()
        self.setup_gui()
    
    def setup_gui(self):
        self.root.title("Google Search Tool")
        self.root.geometry("500x300")
        self.root.resizable(True, True)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Google Search", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Search input
        ttk.Label(main_frame, text="Search Query:").grid(row=1, column=0, 
                                                        sticky=tk.W, padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(main_frame, textvariable=self.search_var, 
                                     font=('Arial', 11), width=30)
        self.search_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Search button
        search_btn = ttk.Button(main_frame, text="Search", 
                               command=self.perform_search)
        search_btn.grid(row=1, column=2)
        
        # Bind Enter key to search
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        
        # Status label
        self.status_var = tk.StringVar(value="Enter a name or search term above")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                foreground="gray")
        status_label.grid(row=2, column=0, columnspan=3, pady=(20, 0))
        
        # Examples frame
        examples_frame = ttk.LabelFrame(main_frame, text="Examples", padding="10")
        examples_frame.grid(row=3, column=0, columnspan=3, pady=(20, 0), 
                           sticky=(tk.W, tk.E))
        examples_frame.columnconfigure(0, weight=1)
        
        examples_text = """• John Smith LinkedIn
• "Jane Doe" software engineer
• Albert Einstein biography
• "Python programming" tutorial"""
        
        ttk.Label(examples_frame, text=examples_text, 
                 justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
        
        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=(20, 0))
        
        ttk.Button(btn_frame, text="Clear", 
                  command=self.clear_search).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(btn_frame, text="Quit", 
                  command=self.root.quit).pack(side=tk.LEFT)
        
        # Focus on entry
        self.search_entry.focus()
    
    def perform_search(self):
        query = self.search_var.get()
        if not query.strip():
            messagebox.showwarning("Empty Query", "Please enter a search term")
            return
        
        self.status_var.set("Opening browser...")
        self.root.update()
        
        # Perform search in thread to avoid GUI freezing
        def search_thread():
            success, message = self.searcher.search(query)
            self.root.after(100, lambda: self.update_status(success, message))
        
        threading.Thread(target=search_thread, daemon=True).start()
    
    def update_status(self, success, message):
        if success:
            self.status_var.set(f"✓ {message}")
        else:
            self.status_var.set(f"✗ {message}")
            messagebox.showerror("Search Error", message)
    
    def clear_search(self):
        self.search_var.set("")
        self.status_var.set("Enter a name or search term above")
        self.search_entry.focus()

def run_cli():
    """Command line interface"""
    parser = argparse.ArgumentParser(description='Search Google for names or any query')
    parser.add_argument('query', nargs='*', help='Search query (name or any terms)')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    searcher = GoogleSearcher()
    
    if args.interactive:
        print("Google Search Tool - Interactive Mode")
        print("Type 'quit' or 'exit' to stop\n")
        
        while True:
            try:
                query = input("Enter search query: ").strip()
                if query.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if query:
                    success, message = searcher.search(query)
                    print(f"{'✓' if success else '✗'} {message}")
                else:
                    print("Please enter a valid search query")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                break
    
    elif args.query:
        query = ' '.join(args.query)
        success, message = searcher.search(query)
        print(f"{'✓' if success else '✗'} {message}")
    
    else:
        # No arguments provided, show help
        parser.print_help()

def run_gui():
    """GUI interface"""
    root = tk.Tk()
    app = GoogleSearchGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] != '--gui':
        # Command line mode
        run_cli()
    else:
        # GUI mode (default or explicit --gui)
        if len(sys.argv) > 1 and sys.argv[1] == '--gui':
            sys.argv.pop(1)  # Remove --gui flag
        run_gui()

if __name__ == "__main__":
    print("Google Search Script")
    print("Usage:")
    print("  python search_google.py 'John Smith'           # Direct search")
    print("  python search_google.py -i                     # Interactive CLI")
    print("  python search_google.py --gui                  # GUI mode")
    print("  python search_google.py                        # GUI mode (default)")
    print()
    
    main()