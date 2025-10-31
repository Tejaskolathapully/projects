import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os

# DATABASE SETUP (unchanged)
conn = sqlite3.connect('travel_agency.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_info_name TEXT NOT NULL,
    user_name TEXT UNIQUE NOT NULL,
    user_password TEXT NOT NULL
)
''')
conn.commit()

# Example: 10 days per trip for per/day calculation
TRIP_DAYS = 10

# Extended and enhanced destinations data
destinations = [
    # Asia
    {"name": "Japan", "description": "Cherry blossoms, shrines, Tokyo lights.", "image": "japan.png", "days": 10,
     "costs": {"flight": 45000, "accommodation": 40000, "food": 15000, "entertainment": 12000, "local_travel": 8000}},
    {"name": "Singapore", "description": "Modern city, shopping & multicultural cuisine.", "image": "singapore.png", "days": 7,
     "costs": {"flight": 16000, "accommodation": 25000, "food": 9000, "entertainment": 7000, "local_travel": 5000}},
    {"name": "Thailand", "description": "Exotic beaches, temples & famous street food.", "image": "thailand.png", "days": 7,
     "costs": {"flight": 10000, "accommodation": 15000, "food": 7000, "entertainment": 5000, "local_travel": 3000}},
    {"name": "China", "description": "Great Wall, Beijing food and heritage.", "image": "china.png", "days": 8,
     "costs": {"flight": 35000, "accommodation": 30000, "food": 12000, "entertainment": 9000, "local_travel": 6000}},
    # Europe
    {"name": "United Kingdom", "description": "Buckingham Palace, British museums, London lifestyle.", "image": "uk.png", "days": 10,
     "costs": {"flight": 45000, "accommodation": 55000, "food": 15000, "entertainment": 12000, "local_travel": 7000}},
    {"name": "France", "description": "Eiffel Tower, superb wines, art, fashion.", "image": "france.png", "days": 9,
     "costs": {"flight": 48000, "accommodation": 50000, "food": 16000, "entertainment": 11000, "local_travel": 8000}},
    {"name": "Germany", "description": "Berlin history, beer culture, castles, autobahn.", "image": "germany.png", "days": 8,
     "costs": {"flight": 45000, "accommodation": 45000, "food": 13000, "entertainment": 9000, "local_travel": 7000}},
    {"name": "Italy", "description": "Roman ruins, Florence art, Venetian canals.", "image": "italy.png", "days": 9,
     "costs": {"flight": 47000, "accommodation": 48000, "food": 14000, "entertainment": 9500, "local_travel": 6500}},
    # North America
    {"name": "United States", "description": "NYC, Grand Canyon, Hollywood, diverse eats.", "image": "usa.png", "days": 14,
     "costs": {"flight": 65000, "accommodation": 60000, "food": 20000, "entertainment": 18000, "local_travel": 10000}},
    {"name": "Canada", "description": "Toronto, Vancouver, Rocky Mountains & lakes.", "image": "canada.png", "days": 10,
     "costs": {"flight": 60000, "accommodation": 54000, "food": 18000, "entertainment": 15000, "local_travel": 8500}},
    # South America
    {"name": "Brazil", "description": "Rio Carnival, rainforests, samba nightlife.", "image": "brazil.png", "days": 10,
     "costs": {"flight": 72000, "accommodation": 45000, "food": 14000, "entertainment": 11000, "local_travel": 6000}},
    {"name": "Argentina", "description": "Buenos Aires culture, tango and Patagonia.", "image": "argentina.png", "days": 10,
     "costs": {"flight": 70000, "accommodation": 43000, "food": 12000, "entertainment": 8000, "local_travel": 5000}},
    # Africa
    {"name": "South Africa", "description": "Safari, Cape Town, wine tours, mountain hikes.", "image": "southafrica.png", "days": 8,
     "costs": {"flight": 40000, "accommodation": 35000, "food": 9000, "entertainment": 7000, "local_travel": 4000}},
    {"name": "Egypt", "description": "Pyramids, Nile River, ancient sites.", "image": "egypt.png", "days": 7,
     "costs": {"flight": 35000, "accommodation": 28000, "food": 8000, "entertainment": 6000, "local_travel": 3000}},
    # Oceania
    {"name": "Australia", "description": "Sydney Opera House, Outback, reef diving.", "image": "australia.png", "days": 10,
     "costs": {"flight": 70000, "accommodation": 52000, "food": 15000, "entertainment": 12000, "local_travel": 7000}},
    {"name": "New Zealand", "description": "Queenstown adventure, Maori culture, mountains.", "image": "newzealand.png", "days": 9,
     "costs": {"flight": 82000, "accommodation": 55000, "food": 14000, "entertainment": 11000, "local_travel": 6500}},
    # Middle East
    {"name": "Dubai", "description": "Burj Khalifa, shopping, desert tours.", "image": "dubai.png", "days": 6,
     "costs": {"flight": 12000, "accommodation": 25000, "food": 9000, "entertainment": 7000, "local_travel": 4000}},
    {"name": "Turkey", "description": "Istanbul bazaars, Cappadocia, Turkish food.", "image": "turkey.png", "days": 9,
     "costs": {"flight": 40000, "accommodation": 35000, "food": 9000, "entertainment": 7000, "local_travel": 3500}},
]

def format_price(amount):
    return "₹{:,.0f}".format(amount)

def get_country_tooltip(country):
    # You can extend this dictionary!
    tooltips = {
        "Japan": "Visa: Required | Language: Japanese | Currency: Yen | Best time: Sakura (Mar-Apr)",
        "United States": "Visa: Required | Currency: Dollar | Sights: NYC, LA, Vegas | English spoken",
        "France": "Visa: Required | Currency: Euro | Must see: Eiffel | Language: French",
        "Dubai": "Visa: On Arrival | Currency: Dirham | Best: Nov-Mar | Shopping paradise",
        # Add for more countries as wanted
    }
    return tooltips.get(country, "")

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)
    def show_tip(self, event=None):
        if not self.tipwindow and self.text:
            x = self.widget.winfo_rootx() + 25
            y = self.widget.winfo_rooty() + 20
            self.tipwindow = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            label = tk.Label(tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1, font=("Arial", 10))
            label.pack()
    def hide_tip(self, event=None):
        tw = self.tipwindow
        if tw:
            tw.destroy()
            self.tipwindow = None

class TravelAgencyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Travel Agency")
        self.geometry("1200x800")
        self.config(bg="white")
        self.current_username = None
        self.photo_cache = []
        self.filtered_destinations = list(destinations)
        self.sort_term = "name"  # Sorting term
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        container = tk.Frame(self, bg="white")
        container.grid(row=0, column=0, sticky="nsew")
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, RegisterPage, LoginPage, DestinationsPage, BookingPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)
        self.show_frame(StartPage)
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
    def set_user(self, username):
        self.current_username = username
        self.frames[DestinationsPage].refresh_destinations()
    def sort_destinations(self, term):
        self.sort_term = term
        if term == "name":
            self.filtered_destinations.sort(key=lambda x: x['name'])
        elif term == "total":
            self.filtered_destinations.sort(key=lambda x: sum(x['costs'].values()))
        self.frames[DestinationsPage].refresh_destinations()
    def filter_dest(self, filter_text=""):
        f_text = filter_text.lower()
        self.filtered_destinations = [d for d in destinations if f_text in d["name"].lower()]
        self.sort_destinations(self.sort_term)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.grid(sticky="nsew")
        label = ttk.Label(self, text="Travel Agency", font=("Georgia", 30, "bold"), background="white", foreground="green")
        label.grid(row=0, column=0, padx=20, pady=90, sticky="n")
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.grid(row=1, column=0, pady=40)
        reg_btn = ttk.Button(btn_frame, text="Register", width=20, command=lambda: controller.show_frame(RegisterPage))
        reg_btn.grid(row=0, column=0, padx=40, pady=20)
        login_btn = ttk.Button(btn_frame, text="Login", width=20, command=lambda: controller.show_frame(LoginPage))
        login_btn.grid(row=0, column=1, padx=40, pady=20)

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.grid(sticky="nsew")
        ttk.Label(self, text="Register", font=("Arial", 24, "bold"), background="white").pack(pady=30)
        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(pady=20)
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=3)
        ttk.Label(form_frame, text="Name:", background="white").grid(row=0, column=0, sticky="e", pady=12, padx=10)
        self.entry_name = ttk.Entry(form_frame, width=40)
        self.entry_name.grid(row=0, column=1, pady=12, padx=10, sticky="ew")
        ttk.Label(form_frame, text="Username:", background="white").grid(row=1, column=0, sticky="e", pady=12, padx=10)
        self.entry_username = ttk.Entry(form_frame, width=40)
        self.entry_username.grid(row=1, column=1, pady=12, padx=10, sticky="ew")
        ttk.Label(form_frame, text="Password:", background="white").grid(row=2, column=0, sticky="e", pady=12, padx=10)
        self.entry_password = ttk.Entry(form_frame, width=40, show="*")
        self.entry_password.grid(row=2, column=1, pady=12, padx=10, sticky="ew")
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=28)
        ttk.Button(btn_frame, text="Sign Up", command=self.register).grid(row=0, column=0, padx=26)
        ttk.Button(btn_frame, text="Back", command=lambda: controller.show_frame(StartPage)).grid(row=0, column=1, padx=26)
    def register(self):
        name = self.entry_name.get().strip()
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        if not (name and username and password):
            messagebox.showerror("Error", "All fields are required.")
            return
        try:
            cursor.execute("INSERT INTO user_info (user_info_name,user_name,user_password) VALUES (?, ?, ?)", (name, username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful! You can now login.")
            self.controller.show_frame(StartPage)
            self.entry_name.delete(0, tk.END)
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists. Choose a different one.")

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.grid(sticky="nsew")
        ttk.Label(self, text="Login", font=("Arial", 24, "bold"), background="white").pack(pady=30)
        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(pady=20)
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=3)
        ttk.Label(form_frame, text="Username:", background="white").grid(row=0, column=0, sticky="e", pady=12, padx=10)
        self.entry_username = ttk.Entry(form_frame, width=40)
        self.entry_username.grid(row=0, column=1, pady=12, padx=10, sticky="ew")
        ttk.Label(form_frame, text="Password:", background="white").grid(row=1, column=0, sticky="e", pady=12, padx=10)
        self.entry_password = ttk.Entry(form_frame, width=40, show="*")
        self.entry_password.grid(row=1, column=1, pady=12, padx=10, sticky="ew")
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=28)
        ttk.Button(btn_frame, text="Login", command=self.login).grid(row=0, column=0, padx=26)
        ttk.Button(btn_frame, text="Back", command=lambda: controller.show_frame(StartPage)).grid(row=0, column=1, padx=26)
    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        if not (username and password):
            messagebox.showerror("Error", "Please enter both username and password.")
            return
        cursor.execute("SELECT user_password FROM user_info WHERE user_name = ?", (username,))
        result = cursor.fetchone()
        if result and result[0] == password:
            self.controller.set_user(username)
            messagebox.showinfo("Welcome", f"Welcome {username}!")
            self.controller.show_frame(DestinationsPage)
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Incorrect username or password.")

class DestinationsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.grid(sticky="nsew")
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.label_greet = ttk.Label(self, text="", font=("Helvetica", 16, "bold"), background="white")
        self.label_greet.grid(row=0, column=0, pady=8, sticky="n")

        # Search and sort bar
        search_sort_frame = tk.Frame(self, bg="white")
        search_sort_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=1)
        tk.Label(search_sort_frame, text="Search:", bg="white").pack(side="left", padx=(6,2))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_sort_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side="left", padx=2)
        search_entry.bind("<KeyRelease>", self.on_search)
        ttk.Button(search_sort_frame, text="Sort by Name", command=lambda: controller.sort_destinations("name")).pack(side="left", padx=6)
        ttk.Button(search_sort_frame, text="Sort by Price", command=lambda: controller.sort_destinations("total")).pack(side="left", padx=2)

        # Responsive table canvas
        canvas_frame = tk.Frame(self, bg="white")
        canvas_frame.grid(row=2, column=0, sticky="nsew")
        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(canvas_frame, borderwidth=0, background="#f0f0f0", height=650)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vsb = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.hsb = tk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.hsb.grid(row=1, column=0, sticky="ew")

        self.frame = tk.Frame(self.canvas, background="#f0f0f0")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        def onFrameConfigure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.frame.bind("<Configure>", onFrameConfigure)
        def onCanvasConfigure(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.canvas.bind("<Configure>", onCanvasConfigure)

        btn_frame = tk.Frame(self, bg="white")
        btn_frame.grid(row=3, column=0, pady=16)
        ttk.Button(btn_frame, text="Logout", command=self.logout).pack()

        self.refresh_destinations()

    def on_search(self, event=None):
        txt = self.search_var.get()
        self.controller.filter_dest(txt)

    def refresh_destinations(self):
        self.label_greet.config(text=f"Welcome, {self.controller.current_username}")
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.controller.photo_cache.clear()
        headers = ["Image", "Place", "Price (INR)", "Description", "Book"]
        for i, h in enumerate(headers):
            lbl = ttk.Label(self.frame, text=h, font=("Arial", 11, "bold"), background="#d0d0d0",
                            borderwidth=1, relief="solid", anchor="center")
            lbl.grid(row=0, column=i, sticky="nsew", padx=4, pady=3)
            if i == 3:
                self.frame.columnconfigure(i, weight=4)
            else:
                self.frame.columnconfigure(i, weight=2)
        dests = self.controller.filtered_destinations
        # Alternate row coloring
        for idx, place in enumerate(dests, start=1):
            row_bg = "#eeeeee" if idx % 2 == 0 else "#f7f7f7"
            img_path = place["image"]
            if os.path.isfile(img_path):
                img = Image.open(img_path).resize((90, 70))
                photo = ImageTk.PhotoImage(img)
            else:
                photo = ImageTk.PhotoImage(Image.new("RGB", (90, 70), color="#ccc"))
            self.controller.photo_cache.append(photo)
            ttk.Label(self.frame, image=photo, background=row_bg).grid(row=idx, column=0, padx=7, pady=7, sticky="w")
            ttk.Label(self.frame, text=place["name"], background=row_bg, anchor="w",
                      font=("Arial", 11)).grid(row=idx, column=1, padx=7, pady=7, sticky="w")
            total_cost = sum(place["costs"].values())
            ttk.Label(self.frame, text=format_price(total_cost), background=row_bg, anchor="center",
                      font=("Arial", 11, "bold")).grid(row=idx, column=2, padx=7, pady=7, sticky="e")
            desc_lbl = ttk.Label(self.frame, text=place["description"], background=row_bg, wraplength=420,
                                anchor="w", justify="left", font=("Arial", 11))
            desc_lbl.grid(row=idx, column=3, padx=7, pady=7, sticky="w")
            # Tooltip with extra country info on hover
            ToolTip(desc_lbl, get_country_tooltip(place['name']))
            # Book Now button
            btn = ttk.Button(self.frame, text="Book Now", command=self.make_book_command(place))
            btn.grid(row=idx, column=4, padx=16, pady=7, sticky="e")
        # Summary row
        if len(dests) > 0:
            ave_cost = sum(sum(d['costs'].values()) for d in dests) // len(dests)
            ttk.Label(self.frame, text=f"Average price: {format_price(ave_cost)}", background="#ddeeff",
                      font=("Arial", 12, "bold"), anchor="center").grid(row=len(dests)+1, column=2, sticky="ew", padx=8, pady=10)
    def make_book_command(self, place):
        def cmd():
            self.book_package(place)
        return cmd
    def book_package(self, place):
        booking_frame = self.controller.frames[BookingPage]
        booking_frame.set_package(place)
        self.controller.show_frame(BookingPage)
    def logout(self):
        self.controller.current_username = None
        self.controller.show_frame(StartPage)

class BookingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.grid(sticky="nsew")
        ttk.Label(self, text="Booking Details", font=("Arial", 24, "bold"), background="white").pack(pady=25)
        self.details_label = ttk.Label(self, text="", font=("Arial", 15), background="white", justify="left", wraplength=850)
        self.details_label.pack(pady=14)
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=30)
        ttk.Button(btn_frame, text="Back to Packages",
                   command=lambda: controller.show_frame(DestinationsPage)).grid(row=0, column=0, padx=24)
        ttk.Button(btn_frame, text="Logout", command=self.logout).grid(row=0, column=1, padx=24)
    def set_package(self, package):
        self.package = package
        costs = package.get("costs", {})
        total = sum(costs.values())
        days = package.get("days", TRIP_DAYS)
        cost_per_day = f"₹{total//days:,.0f} per day"
        text = (f"Package: {package['name']}\n\nDescription:\n{package['description']}\n\nEstimated Expenses Breakdown:\n")
        for category, cost in costs.items():
            text += f"  {category.replace('_', ' ').title()}: {format_price(cost)}\n"
        text += f"\nDuration: {days} days\nCost per day: {cost_per_day}\nTotal Estimated Cost: {format_price(total)}"
        text += f"\n\nThank you for choosing this package, {self.controller.current_username}!"
        self.details_label.config(text=text)
    def logout(self):
        self.controller.current_username = None
        self.controller.show_frame(StartPage)

if __name__ == "__main__":
    app = TravelAgencyApp()
    app.mainloop()
    
