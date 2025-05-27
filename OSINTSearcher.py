"""
OSINT People Investigation Tool
Comprehensive background research across multiple platforms
"""
# Author: Arshia Keshvari
# Date: 2025-05-27
import webbrowser
import urllib.parse
import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from datetime import datetime
import json
import os

class OSINTSearcher:
    def __init__(self):
        self.search_platforms = {
            'Social Media': {
                'LinkedIn': 'https://www.linkedin.com/search/results/people/?keywords={}',
                'Twitter/X': 'https://twitter.com/search?q="{}"&src=typed_query',
                'Facebook': 'https://www.facebook.com/search/people/?q={}',
                'Instagram': 'https://www.instagram.com/explore/tags/{}/',
                'TikTok': 'https://www.tiktok.com/search/user?q={}',
                'YouTube': 'https://www.youtube.com/results?search_query="{}"',
                'Reddit': 'https://www.reddit.com/search/?q="{}"&type=user',
                'Pinterest': 'https://www.pinterest.com/search/users/?q={}'
            },
            'Professional': {
                'Google Scholar': 'https://scholar.google.com/scholar?q=author:"{}"',
                'ResearchGate': 'https://www.researchgate.net/search/researcher?q={}',
                'Academia.edu': 'https://www.academia.edu/search?q={}',
                'ORCID': 'https://orcid.org/orcid-search/search?searchQuery={}',
                'ZoomInfo': 'https://www.zoominfo.com/s/search?q={}',
                'AngelList': 'https://angel.co/search?query={}&type=people'
            },
            'Public Records': {
                'Google (General)': 'https://www.google.com/search?q="{}"',
                'Google (News)': 'https://news.google.com/search?q="{}"',
                'Bing': 'https://www.bing.com/search?q="{}"',
                'DuckDuckGo': 'https://duckduckgo.com/?q="{}"',
                'Whitepages': 'https://www.whitepages.com/name/{}',
                'Spokeo': 'https://www.spokeo.com/search?q={}',
                'PeopleFinder': 'https://www.peoplefinder.com/search/?full_name={}'
            },
            'Business & Legal': {
                'SEC Filings': 'https://www.sec.gov/edgar/search/#/q={}',
                'OpenCorporates': 'https://opencorporates.com/officers?q={}',
                'Crunchbase': 'https://www.crunchbase.com/discover/people/{}',
                'Court Records': 'https://www.judyrecords.com/search?first={}&last={}',
                'Property Records': 'https://www.propertyshark.com/mason/Property-Search/?search_text={}'
            },
            'Dark Web & Breach Data': {
                'Have I Been Pwned': 'https://haveibeenpwned.com/unifiedsearch/{}',
                'DeHashed': 'https://dehashed.com/search?query={}',
                'Intelligence X': 'https://intelx.io/?s={}'
            }
        }
    
    def format_name_for_url(self, name, platform_url):
        """Format name appropriately for different platforms"""
        if '{}' in platform_url:
            return platform_url.format(urllib.parse.quote_plus(name))
        else:
            # For platforms that need first/last name separately
            parts = name.strip().split()
            if len(parts) >= 2:
                first = parts[0]
                last = ' '.join(parts[1:])
                return platform_url.format(first=urllib.parse.quote_plus(first), 
                                         last=urllib.parse.quote_plus(last))
            else:
                return platform_url.format(urllib.parse.quote_plus(name))
    
    def search_person(self, name, selected_categories=None, delay=1):
        """Perform comprehensive search across all platforms"""
        if not name.strip():
            return False, "Name cannot be empty"
        
        search_results = []
        total_searches = 0
        
        categories_to_search = selected_categories or self.search_platforms.keys()
        
        for category in categories_to_search:
            if category in self.search_platforms:
                for platform, url_template in self.search_platforms[category].items():
                    try:
                        search_url = self.format_name_for_url(name, url_template)
                        search_results.append({
                            'category': category,
                            'platform': platform,
                            'url': search_url,
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        total_searches += 1
                    except Exception as e:
                        search_results.append({
                            'category': category,
                            'platform': platform,
                            'url': f"Error: {str(e)}",
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
        
        return True, search_results
    
    def open_searches(self, search_results, delay=2):
        """Open search results in browser with delay"""
        opened = 0
        for result in search_results:
            if result['url'].startswith('http'):
                try:
                    webbrowser.open(result['url'])
                    opened += 1
                    time.sleep(delay)  # Delay between opening tabs
                except Exception as e:
                    print(f"Error opening {result['platform']}: {e}")
        return opened

class OSINTSearchGUI:
    def __init__(self, root):
        self.root = root
        self.searcher = OSINTSearcher()
        self.search_results = []
        self.setup_gui()
    
    def setup_gui(self):
        self.root.title("OSINT People Investigation Tool")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Search Tab
        search_frame = ttk.Frame(notebook)
        notebook.add(search_frame, text="Search")
        self.setup_search_tab(search_frame)
        
        # Results Tab
        results_frame = ttk.Frame(notebook)
        notebook.add(results_frame, text="Results")
        self.setup_results_tab(results_frame)
    
    def setup_search_tab(self, parent):
        # Main search frame
        main_frame = ttk.Frame(parent, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="OSINT People Investigation", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Name input
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(input_frame, text="Full Name:", font=('Arial', 12)).pack(anchor=tk.W)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(input_frame, textvariable=self.name_var, 
                              font=('Arial', 12), width=40)
        name_entry.pack(fill=tk.X, pady=(5, 0))
        name_entry.bind('<Return>', lambda e: self.start_search())
        
        # Category selection
        categories_frame = ttk.LabelFrame(main_frame, text="Search Categories", padding="10")
        categories_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.category_vars = {}
        row = 0
        col = 0
        for category in self.searcher.search_platforms.keys():
            var = tk.BooleanVar(value=True)
            self.category_vars[category] = var
            cb = ttk.Checkbutton(categories_frame, text=category, variable=var)
            cb.grid(row=row, column=col, sticky=tk.W, padx=10, pady=2)
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Delay setting
        delay_frame = ttk.Frame(options_frame)
        delay_frame.pack(fill=tk.X)
        
        ttk.Label(delay_frame, text="Delay between tabs (seconds):").pack(side=tk.LEFT)
        self.delay_var = tk.StringVar(value="2")
        delay_spin = ttk.Spinbox(delay_frame, from_=0.5, to=10, increment=0.5, 
                                textvariable=self.delay_var, width=10)
        delay_spin.pack(side=tk.RIGHT)
        
        # Auto-open option
        self.auto_open_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Auto-open all results in browser", 
                       variable=self.auto_open_var).pack(anchor=tk.W, pady=(10, 0))
        
        # Search button
        search_btn = ttk.Button(main_frame, text="Start Investigation", 
                               command=self.start_search, style='Accent.TButton')
        search_btn.pack(pady=10)
        
        # Status
        self.status_var = tk.StringVar(value="Enter a full name to begin investigation")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                font=('Arial', 10), foreground="gray")
        status_label.pack(pady=(10, 0))
        
        # Warning label
        warning_text = ("⚠️ ETHICAL USE ONLY: This tool is for legitimate research, journalism, "
                       "cybersecurity, and due diligence purposes. Respect privacy laws and platform terms of service.")
        warning_label = ttk.Label(main_frame, text=warning_text, 
                                 font=('Arial', 9), foreground="red", wraplength=600)
        warning_label.pack(pady=(20, 0))
    
    def setup_results_tab(self, parent):
        results_main = ttk.Frame(parent, padding="10")
        results_main.pack(fill=tk.BOTH, expand=True)
        
        # Results header
        header_frame = ttk.Frame(results_main)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="Investigation Results", 
                 font=('Arial', 14, 'bold')).pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text="Export Results", 
                  command=self.export_results).pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(header_frame, text="Open All URLs", 
                  command=self.open_all_results).pack(side=tk.RIGHT)
        
        # Results display
        self.results_text = scrolledtext.ScrolledText(results_main, wrap=tk.WORD, 
                                                     font=('Consolas', 10))
        self.results_text.pack(fill=tk.BOTH, expand=True)
    
    def start_search(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Empty Name", "Please enter a full name")
            return
        
        # Get selected categories
        selected_categories = [cat for cat, var in self.category_vars.items() if var.get()]
        if not selected_categories:
            messagebox.showwarning("No Categories", "Please select at least one category")
            return
        
        self.status_var.set("Generating search queries...")
        
        # Perform search in thread
        def search_thread():
            success, results = self.searcher.search_person(name, selected_categories)
            self.root.after(100, lambda: self.handle_search_results(success, results, name))
        
        threading.Thread(target=search_thread, daemon=True).start()
    
    def handle_search_results(self, success, results, name):
        if not success:
            messagebox.showerror("Search Error", results)
            return
        
        self.search_results = results
        self.display_results(name)
        
        # Auto-open if selected
        if self.auto_open_var.get():
            delay = float(self.delay_var.get())
            self.status_var.set("Opening browser tabs...")
            
            def open_thread():
                opened = self.searcher.open_searches(results, delay)
                self.root.after(100, lambda: self.status_var.set(f"Investigation complete! Opened {opened} tabs"))
            
            threading.Thread(target=open_thread, daemon=True).start()
        else:
            self.status_var.set(f"Investigation complete! Generated {len(results)} search queries")
    
    def display_results(self, name):
        self.results_text.delete(1.0, tk.END)
        
        header = f"OSINT Investigation Results for: {name}\n"
        header += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += "=" * 60 + "\n\n"
        
        self.results_text.insert(tk.END, header)
        
        current_category = None
        for result in self.search_results:
            if result['category'] != current_category:
                current_category = result['category']
                self.results_text.insert(tk.END, f"\n[{current_category}]\n")
                self.results_text.insert(tk.END, "-" * 40 + "\n")
            
            self.results_text.insert(tk.END, f"{result['platform']}: {result['url']}\n")
    
    def open_all_results(self):
        if not self.search_results:
            messagebox.showinfo("No Results", "No search results to open")
            return
        
        delay = float(self.delay_var.get())
        self.status_var.set("Opening all results...")
        
        def open_thread():
            opened = self.searcher.open_searches(self.search_results, delay)
            self.root.after(100, lambda: self.status_var.set(f"Opened {opened} browser tabs"))
        
        threading.Thread(target=open_thread, daemon=True).start()
    
    def export_results(self):
        if not self.search_results:
            messagebox.showinfo("No Results", "No search results to export")
            return
        
        # Simple export to text file
        filename = f"osint_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                content = self.results_text.get(1.0, tk.END)
                f.write(content)
            messagebox.showinfo("Export Complete", f"Results exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting results: {e}")

def main():
    print("OSINT People Investigation Tool")
    print("=" * 40)
    print("⚠️  ETHICAL USE ONLY")
    print("This tool is designed for legitimate purposes:")
    print("• Background checks for employment")
    print("• Journalism and research")
    print("• Cybersecurity investigations")
    print("• Due diligence processes")
    print()
    print("Please respect privacy laws and platform terms of service.")
    print("=" * 40)
    print()
    
    root = tk.Tk()
    app = OSINTSearchGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()