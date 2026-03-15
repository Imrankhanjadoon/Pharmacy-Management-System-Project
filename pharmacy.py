import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date, datetime

class PharmacyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Uzair Pharmacy - Management System")

        # Make window full screen initially
        self.root.state('zoomed')  # This opens the window maximized (full screen)

        # Optional: allow resizing (you can comment out if you want to restrict)
        self.root.resizable(True, True)

        # Background color
        self.root.configure(bg="#f8fafc")

        self.conn = sqlite3.connect('pharmacy.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

        self.current_user = None
        self.show_login_screen()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS admin 
                              (username TEXT PRIMARY KEY, password TEXT)''')
        self.cursor.execute("INSERT OR IGNORE INTO admin VALUES ('admin', 'admin123')")

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS medicines 
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               name TEXT UNIQUE NOT NULL,
                               company TEXT,
                               price REAL NOT NULL,
                               quantity INTEGER NOT NULL)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sales 
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               sale_date TEXT,
                               medicine_name TEXT,
                               quantity INTEGER,
                               total_price REAL)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS logs 
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               timestamp TEXT,
                               action TEXT,
                               details TEXT)''')
        self.conn.commit()

    def log_action(self, action, details=""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO logs (timestamp, action, details) VALUES (?,?,?)",
                            (timestamp, action, details))
        self.conn.commit()

    # ────────────────────────────────────────────────
    #                  LOGIN SCREEN
    # ────────────────────────────────────────────────
    def show_login_screen(self):
        self.clear_screen()

        # Main frame
        frame = tk.Frame(self.root, bg="#f8fafc")
        frame.pack(expand=True, pady=80)

        # Title
        tk.Label(frame, text="Uzair Pharmacy", font=("Arial", 32, "bold"), bg="#f8fafc", fg="#1e40af").pack(pady=5)
        tk.Label(frame, text="Management System (انتظامی نظام)", font=("Arial", 16), bg="#f8fafc", fg="#4b5563").pack(
            pady=5)

        # Username
        tk.Label(frame, text="Username (اسم صارف)", font=("Arial", 16), bg="#f8fafc").pack(pady=(60, 5))
        self.username_entry = tk.Entry(frame, font=("Arial", 16), width=36)
        self.username_entry.pack(pady=8)

        # Password
        tk.Label(frame, text="Password (پاس ورڈ)", font=("Arial", 16), bg="#f8fafc").pack(pady=5)
        self.password_entry = tk.Entry(frame, font=("Arial", 16), width=36, show="*")
        self.password_entry.pack(pady=12)

        # Login Button
        tk.Button(frame, text="Login (لاگ ان کریں)", font=("Arial", 16, "bold"), bg="#10b981", fg="white", width=22,
                  command=self.login).pack(pady=35)

        # Forgot Password
        tk.Button(frame, text="Forgot Password? (پاس ورڈ بھول گئے؟)", font=("Arial", 13), fg="#ef4444", bg="#f8fafc",
                  bd=0,
                  command=self.show_forgot_password).pack()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror(
                "Error (غلطی)",
                "Please enter both username and password. (براہ کرم یوزر نیم اور پاس ورڈ دونوں درج کریں)"
            )
            return

        # Check database for matching username AND password
        row = self.cursor.execute(
            "SELECT username FROM admin WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        if row:
            self.current_user = row[0]
            self.log_action(
                "Login Successful (لاگ ان کامیاب)",
                f"User: {self.current_user}"
            )
            self.show_main_menu()
        else:
            messagebox.showerror(
                "Error (غلطی)",
                "Wrong username or password! (یوزر نیم یا پاس ورڈ غلط ہے)"
            )
    def show_forgot_password(self):
        self.clear_screen()
        frame = tk.Frame(self.root, bg="#f8fafc")
        frame.pack(expand=True, pady=120)

        tk.Label(frame, text="Forgot Password (پاس ورڈ کی بحالی)", font=("Arial", 22, "bold"), bg="#f8fafc", fg="#1e40af").pack(pady=20)
        tk.Label(frame, text="What is your pet name? (آپ کا پالتو جانور کا نام کیا ہے؟)", font=("Arial", 15), bg="#f8fafc").pack()
        self.answer_entry = tk.Entry(frame, font=("Arial", 15), width=35)
        self.answer_entry.pack(pady=15)

        tk.Button(frame, text="Submit (جمع کروائیں)", font=("Arial", 15), bg="#f59e0b", fg="white", width=20,
                  command=self.check_security_answer).pack(pady=25)

        tk.Button(frame, text="Back to Login (واپس لاگ ان پر)", font=("Arial", 13), fg="#3b82f6", bg="#f8fafc", bd=0,
                  command=self.show_login_screen).pack()

    def check_security_answer(self):
        if self.answer_entry.get().strip().lower() == "max":
            messagebox.showinfo("Recovery (بحالی)", "Your current password is: admin123\n(Change from settings) (آپ کا موجودہ پاس ورڈ ہے: admin123\n(سیٹنگز سے تبدیل کریں))")
            self.show_login_screen()
        else:
            messagebox.showerror("Wrong Answer (غلط جواب)", "Incorrect answer (جواب درست نہیں ہے)")

    # ────────────────────────────────────────────────
    #                  MAIN MENU
    # ────────────────────────────────────────────────
    def show_main_menu(self):
        self.clear_screen()

        tk.Label(self.root, text="Welcome to Uzair Pharmacy (خوش آمدید - عذیر فارمیسی)",
                 font=("Arial", 26, "bold"), bg="#f8fafc", fg="#1e40af").pack(pady=20)
        tk.Label(self.root, text="Use buttons below (نیچے دیئے گئے بٹن استعمال کریں)",
                 font=("Arial", 15), bg="#f8fafc", fg="#6b7280").pack(pady=(0, 25))

        frame = tk.Frame(self.root, bg="#f8fafc")
        frame.pack()

        buttons = [
            ("Add New Medicine (نئی دوائی شامل کریں)", self.show_add_medicine, "#10b981"),
            ("Sell Medicine (دوائی فروخت کریں)", self.show_sell_medicine, "#3b82f6"),
            ("Stock & Search (اسٹاک چیک / تلاش)", self.show_stock_search, "#f59e0b"),
            ("Sales Report (سیل رپورٹ دیکھیں)", self.show_sales_report, "#8b5cf6"),
            ("View Activity Logs (سرگرمیاں دیکھیں)", self.show_logs, "#4b5563"),
            ("Change Password (پاس ورڈ تبدیل کریں)", self.show_change_password, "#ef4444"),
            ("Add Admin (ایڈمن شامل کریں)", self.show_change_username, "#14b8a6"),
            ("Logout / Exit (لاگ آؤٹ / بند کریں)", self.logout, "#6b7280"),
        ]

        def on_enter(e, btn, color):
            btn['bg'] = "#ffffff"  # Hover color (white)
            btn['fg'] = color  # Change text to original color

        def on_leave(e, btn, color):
            btn['bg'] = color  # Original background color
            btn['fg'] = "white"  # Original text color

        for i, (text, cmd, color) in enumerate(buttons):
            row = i // 2
            col = i % 2
            btn = tk.Button(
                frame,
                text=text,
                font=("Arial", 12, "bold"),  # slightly smaller font to fit one line
                bg=color,
                fg="white",
                width=45,  # increase width so text fits
                height=2,  # adjust height for one line
                command=cmd,
                wraplength=0,  # disables wrapping
                justify="center"
            )
            btn.grid(row=row, column=col, padx=25, pady=18)

            # Bind hover effects
            btn.bind("<Enter>", lambda e, b=btn, c=color: on_enter(e, b, c))
            btn.bind("<Leave>", lambda e, b=btn, c=color: on_leave(e, b, c))
    # ────────────────────────────────────────────────
    #                  ADD MEDICINE (Fixed - Update stock if exists)
    # ────────────────────────────────────────────────
    def show_add_medicine(self):
        self.clear_screen()
        tk.Label(self.root, text="Add New Medicine (نئی دوائی شامل کریں)", font=("Arial", 24, "bold"), bg="#f8fafc", fg="#10b981").pack(pady=15)
        tk.Label(self.root, text="Name, Price & Quantity required (نام، قیمت اور مقدار لازمی بھریں)", font=("Arial", 15), bg="#f8fafc", fg="#6b7280").pack(pady=(0,30))

        frame = tk.Frame(self.root, bg="#f8fafc")
        frame.pack()

        fields = [
            ("Medicine Name * (دوائی کا نام *)", "red"),
            ("Company Name (کمپنی کا نام)", "black"),
            ("Price per Unit (Rs) * (قیمت فی یونٹ (روپے) *)", "red"),
            ("Quantity to Add * (شامل کرنے کی مقدار *)", "red")
        ]

        self.add_entries = []
        for label_text, color in fields:
            tk.Label(frame, text=label_text, font=("Arial", 16), fg=color, bg="#f8fafc").pack(anchor="w", padx=90, pady=12)
            e = tk.Entry(frame, font=("Arial", 16), width=36)
            e.pack(pady=8)
            self.add_entries.append(e)

        tk.Button(self.root, text="Save / Update Medicine", font=("Arial", 16, "bold"), bg="#10b981", fg="white", width=24,
                  command=self.save_medicine).pack(pady=40)

        tk.Button(self.root, text="Back to Menu (واپس مینو پر)", font=("Arial", 14), fg="#ef4444", bg="#f8fafc", bd=0,
                  command=self.show_main_menu).pack()

    def save_medicine(self):
        name = self.add_entries[0].get().strip()
        company = self.add_entries[1].get().strip()
        price_str = self.add_entries[2].get().strip()
        qty_str = self.add_entries[3].get().strip()

        if not name:
            messagebox.showerror("Error (غلطی)", "Medicine Name is required (دوائی کا نام لازمی ہے)")
            return

        try:
            price = float(price_str.replace(',', '').replace(' ', ''))
            if price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error (غلطی)", "Price must be a valid number (e.g. 150 or 150.5) (قیمت درست نمبر میں درج کریں)")
            return

        try:
            add_qty = int(qty_str)
            if add_qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error (غلطی)", "Quantity must be a positive number (مقدار مثبت عدد میں درج کریں)")
            return

        # Check if medicine already exists
        existing = self.cursor.execute("SELECT quantity FROM medicines WHERE name=?", (name,)).fetchone()

        if existing:
            # Update existing stock
            current_qty = existing[0]
            new_qty = current_qty + add_qty
            self.cursor.execute("UPDATE medicines SET quantity = ?, company = ?, price = ? WHERE name = ?",
                                (new_qty, company or "", price, name))
            action_msg = f"Stock Updated: {add_qty} added → Total {new_qty}"
        else:
            # New medicine
            self.cursor.execute("INSERT INTO medicines (name, company, price, quantity) VALUES (?,?,?,?)",
                                (name, company, price, add_qty))
            action_msg = f"New Medicine Added: {add_qty} qty"

        self.conn.commit()
        self.log_action("Medicine Operation (دوائی آپریشن)", f"{name} - {action_msg}")
        messagebox.showinfo("Success (کامیابی)", f"{name} saved/updated successfully!\nQuantity: {add_qty} added. ({name} محفوظ/اپ ڈیٹ ہو گئی!\nمقدار: {add_qty} شامل کی گئی۔)")
        self.show_main_menu()

    # ────────────────────────────────────────────────
    # SELL MEDICINE (unchanged - already good)
    # ────────────────────────────────────────────────
    def show_sell_medicine(self):
        self.clear_screen()
        tk.Label(self.root, text="Sell Medicine (دوائی فروخت کریں)", font=("Arial", 24, "bold"), bg="#f8fafc", fg="#3b82f6").pack(pady=15)
        tk.Label(self.root, text="Enter medicine name and quantity (دوائی کا نام اور فروخت کی مقدار درج کریں)", font=("Arial", 15), bg="#f8fafc", fg="#6b7280").pack(pady=(0,30))

        frame = tk.Frame(self.root, bg="#f8fafc")
        frame.pack()

        tk.Label(frame, text="Medicine Name (دوائی کا نام)", font=("Arial", 16), bg="#f8fafc").pack(anchor="w", padx=90, pady=12)
        self.sell_name = tk.Entry(frame, font=("Arial", 16), width=36)
        self.sell_name.pack(pady=8)

        tk.Label(frame, text="Quantity to Sell (فروخت کی مقدار)", font=("Arial", 16), bg="#f8fafc").pack(anchor="w", padx=90, pady=12)
        self.sell_qty = tk.Entry(frame, font=("Arial", 16), width=36)
        self.sell_qty.pack(pady=8)

        tk.Button(self.root, text="Complete Sale (فروخت مکمل کریں)", font=("Arial", 16, "bold"), bg="#3b82f6", fg="white", width=24,
                  command=self.process_sale).pack(pady=40)

        tk.Button(self.root, text="Back to Menu (واپس مینو پر)", font=("Arial", 14), fg="#ef4444", bg="#f8fafc", bd=0,
                  command=self.show_main_menu).pack()

    def process_sale(self):
        name = self.sell_name.get().strip()
        qty_str = self.sell_qty.get().strip()

        if not name:
            messagebox.showerror("Error (غلطی)", "Medicine Name is required (دوائی کا نام لازمی ہے)")
            return

        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error (غلطی)", "Quantity must be a positive whole number (مقدار مثبت عدد میں درج کریں)")
            return

        row = self.cursor.execute("SELECT quantity, price FROM medicines WHERE name=?", (name,)).fetchone()
        if not row:
            messagebox.showerror("Not Found (نہیں ملی)", f"{name} not in stock ({name} اسٹاک میں موجود نہیں)")
            return

        stock, price = row
        if qty > stock:
            messagebox.showerror("Low Stock (اسٹاک کم ہے)", f"Only {stock} available (صرف {stock} دستیاب ہیں)")
            return

        total = qty * price
        today = date.today().isoformat()

        self.cursor.execute("UPDATE medicines SET quantity = quantity - ? WHERE name=?", (qty, name))
        self.cursor.execute("INSERT INTO sales (sale_date, medicine_name, quantity, total_price) VALUES (?,?,?,?)",
                            (today, name, qty, total))
        self.conn.commit()
        self.log_action("Sale Completed (فروخت ہوئی)", f"{qty} × {name} = Rs {total}")

        messagebox.showinfo("Sale Done (فروخت مکمل ✓)", f"Sold {qty} × {name}\nTotal: Rs {total}\nDate: {today} ({qty} × {name} فروخت ہو گئی\nکل رقم: Rs {total}\nتاریخ: {today})")
        self.show_main_menu()

    # ────────────────────────────────────────────────
    # STOCK + SEARCH + DELETE (Urdu font size reduced in brackets)
    # ────────────────────────────────────────────────
    def show_stock_search(self):
        self.clear_screen()
        tk.Label(self.root, text="Stock & Search Medicine (اسٹاک چیک اور تلاش)", font=("Arial", 24, "bold"), bg="#f8fafc", fg="#f59e0b").pack(pady=15)
        tk.Label(self.root, text="Search or select to delete (دوائی تلاش کریں یا منتخب کرکے ڈیلیٹ کریں)", font=("Arial", 15), bg="#f8fafc", fg="#6b7280").pack(pady=(0,20))

        tk.Label(self.root, text="Search (تلاش کریں):", font=("Arial", 15), bg="#f8fafc").pack()
        self.search_entry = tk.Entry(self.root, font=("Arial", 15), width=45)
        self.search_entry.pack(pady=12)

        btn_frame = tk.Frame(self.root, bg="#f8fafc")
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Search (تلاش کریں)", font=("Arial", 14), bg="#3b82f6", fg="white", width=14,
                  command=self.show_search_result).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Delete Selected", font=("Arial", 14), bg="#ef4444", fg="white", width=18,
                  command=self.delete_selected_medicine).pack(side="left", padx=10)

        self.stock_tree = ttk.Treeview(self.root, columns=("Name", "Company", "Price", "Stock"), show="headings", height=14)
        self.stock_tree.heading("Name", text="Name (دوائی کا نام)")
        self.stock_tree.heading("Company", text="Company (کمپنی)")
        self.stock_tree.heading("Price", text="Price (قیمت)")
        self.stock_tree.heading("Stock", text="Stock (اسٹاک)")
        self.stock_tree.column("Name", width=220)
        self.stock_tree.column("Company", width=180)
        self.stock_tree.column("Price", width=110)
        self.stock_tree.column("Stock", width=110)
        self.stock_tree.pack(pady=15, padx=50, fill="both", expand=True)

        self.load_all_stock()

        tk.Button(self.root, text="Back to Menu (واپس مینو پر)", font=("Arial", 14), fg="#ef4444", bg="#f8fafc", bd=0,
                  command=self.show_main_menu).pack(pady=15)

    # Baqi functions same hain (load_all_stock, show_search_result, delete_selected_medicine, show_sales_report, load_sales_for_date, show_logs, show_change_password, update_password, clear_screen, logout)

    def load_all_stock(self):
        for i in self.stock_tree.get_children():
            self.stock_tree.delete(i)
        for row in self.cursor.execute("SELECT name, company, price, quantity FROM medicines ORDER BY name"):
            tag = "low" if row[3] < 10 else ""
            self.stock_tree.insert("", "end", values=row, tags=(tag,))
        self.stock_tree.tag_configure("low", foreground="red", font=("Arial", 11, "bold"))

    def show_search_result(self):
        term = self.search_entry.get().strip()
        for i in self.stock_tree.get_children():
            self.stock_tree.delete(i)
        q = "SELECT name, company, price, quantity FROM medicines WHERE name LIKE ? ORDER BY name"
        for row in self.cursor.execute(q, (f"%{term}%",)):
            tag = "low" if row[3] < 10 else ""
            self.stock_tree.insert("", "end", values=row, tags=(tag,))

    def delete_selected_medicine(self):
        selected = self.stock_tree.selection()
        if not selected:
            messagebox.showwarning("Select (انتخاب کریں)", "First select a medicine (پہلے دوائی منتخب کریں)")
            return
        name = self.stock_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm Delete (ڈیلیٹ تصدیق)", f"Really delete?\n{name} (کیا واقعی ڈیلیٹ کرنا ہے؟\n{name})"):
            self.cursor.execute("DELETE FROM medicines WHERE name=?", (name,))
            self.conn.commit()
            self.log_action("Medicine Deleted (دوائی ڈیلیٹ کی گئی)", name)
            messagebox.showinfo("Deleted (ڈیلیٹ ہو گئی)", f"{name} deleted successfully ({name} حذف ہو گئی)")
            self.load_all_stock()

    # SALES REPORT (same as before)
    def show_sales_report(self):
        self.clear_screen()
        tk.Label(self.root, text="Sales Report (سیل رپورٹ)", font=("Arial", 24, "bold"), bg="#f8fafc", fg="#8b5cf6").pack(pady=15)
        tk.Label(self.root, text="Enter date (YYYY-MM-DD) or leave blank for all (تاریخ درج کریں یا خالی چھوڑیں سب دیکھنے کے لیے)", font=("Arial", 15), bg="#f8fafc", fg="#6b7280").pack(pady=(0,20))

        self.report_date = tk.Entry(self.root, font=("Arial", 15), width=25)
        self.report_date.insert(0, date.today().isoformat())
        self.report_date.pack(pady=12)

        tk.Button(self.root, text="Show Report (رپورٹ دکھائیں)", font=("Arial", 15, "bold"), bg="#8b5cf6", fg="white", width=22,
                  command=self.load_sales_for_date).pack(pady=20)

        self.sales_tree = ttk.Treeview(self.root, columns=("Date", "Medicine", "Qty", "Amount"), show="headings", height=13)
        self.sales_tree.heading("Date", text="Date (تاریخ)")
        self.sales_tree.heading("Medicine", text="Medicine (دوائی)")
        self.sales_tree.heading("Qty", text="Qty (مقدار)")
        self.sales_tree.heading("Amount", text="Amount (رقم)")
        self.sales_tree.column("Date", width=140)
        self.sales_tree.column("Medicine", width=220)
        self.sales_tree.column("Qty", width=100, anchor="center")
        self.sales_tree.column("Amount", width=140, anchor="center")
        self.sales_tree.pack(pady=15, padx=50, fill="both", expand=True)

        tk.Button(self.root, text="Back to Menu (واپس مینو پر)", font=("Arial", 14), fg="#ef4444", bg="#f8fafc", bd=0,
                  command=self.show_main_menu).pack(pady=15)

    def load_sales_for_date(self):
        for i in self.sales_tree.get_children():
            self.sales_tree.delete(i)

        date_input = self.report_date.get().strip()
        total = 0.0

        if date_input:
            rows = self.cursor.execute("SELECT sale_date, medicine_name, quantity, total_price FROM sales WHERE sale_date=? ORDER BY id DESC",
                                       (date_input,)).fetchall()
        else:
            rows = self.cursor.execute("SELECT sale_date, medicine_name, quantity, total_price FROM sales ORDER BY sale_date DESC, id DESC").fetchall()

        for row in rows:
            self.sales_tree.insert("", "end", values=(row[0], row[1], row[2], f"Rs {row[3]:,.0f}"))
            total += row[3]

        tk.Label(self.root, text=f"Grand Total: Rs {total:,.0f} (کل رقم)", font=("Arial", 16, "bold"), fg="#10b981", bg="#f8fafc").pack(pady=15)

    # ────────────────────────────────────────────────
    #                  ACTIVITY LOGS
    # ────────────────────────────────────────────────
    def show_logs(self):
        self.clear_screen()
        tk.Label(self.root, text="Activity Logs (سرگرمیوں کی فہرست)", font=("Arial", 24, "bold"), bg="#f8fafc", fg="#4b5563").pack(pady=15)
        tk.Label(self.root, text="All actions with time (تمام کارروائیاں وقت کے ساتھ)", font=("Arial", 15), bg="#f8fafc", fg="#6b7280").pack(pady=(0,20))

        tree = ttk.Treeview(self.root, columns=("Time", "Action", "Details"), show="headings", height=18)
        tree.heading("Time", text="Time & Date (وقت اور تاریخ)")
        tree.heading("Action", text="Action (کارروائی)")
        tree.heading("Details", text="Details (تفصیلات)")
        tree.column("Time", width=200)
        tree.column("Action", width=200)
        tree.column("Details", width=350)
        tree.pack(pady=15, padx=50, fill="both", expand=True)

        for row in self.cursor.execute("SELECT timestamp, action, details FROM logs ORDER BY id DESC"):
            tree.insert("", "end", values=row)

        tk.Button(self.root, text="Back to Menu (واپس مینو پر)", font=("Arial", 14), fg="#ef4444", bg="#f8fafc", bd=0,
                  command=self.show_main_menu).pack(pady=15)

    # ────────────────────────────────────────────────
    #               CHANGE PASSWORD
    # ────────────────────────────────────────────────
    def show_change_password(self):
        self.clear_screen()
        tk.Label(self.root, text="Change Password (پاس ورڈ تبدیل کریں)", font=("Arial", 24, "bold"), bg="#f8fafc", fg="#ef4444").pack(pady=30)

        frame = tk.Frame(self.root, bg="#f8fafc")
        frame.pack()

        tk.Label(frame, text="Old Password (پرانا پاس ورڈ)", font=("Arial", 15), bg="#f8fafc").pack(anchor="w", padx=90, pady=12)
        self.old_pass = tk.Entry(frame, font=("Arial", 15), width=36, show="*")
        self.old_pass.pack(pady=8)

        tk.Label(frame, text="New Password (نیا پاس ورڈ)", font=("Arial", 15), bg="#f8fafc").pack(anchor="w", padx=90, pady=12)
        self.new_pass = tk.Entry(frame, font=("Arial", 15), width=36, show="*")
        self.new_pass.pack(pady=8)

        tk.Button(self.root, text="Update Password", font=("Arial", 15, "bold"), bg="#ef4444", fg="white", width=24,
                  command=self.update_password).pack(pady=40)

        tk.Button(self.root, text="Back to Menu (واپس مینو پر)", font=("Arial", 14), fg="#3b82f6", bg="#f8fafc", bd=0,
                  command=self.show_main_menu).pack()

    def update_password(self):
        old = self.old_pass.get().strip()
        new = self.new_pass.get().strip()
        if not old or not new:
            messagebox.showerror("Error (غلطی)", "Both fields required (دونوں فیلڈز بھریں)")
            return

        row = self.cursor.execute("SELECT password FROM admin WHERE username='admin'").fetchone()
        if row[0] != old:
            messagebox.showerror("Error (غلطی)", "Old password is wrong (پرانا پاس ورڈ غلط ہے)")
            return

        self.cursor.execute("UPDATE admin SET password=? WHERE username='admin'", (new,))
        self.conn.commit()
        self.log_action("Password Changed (پاس ورڈ تبدیل کیا گیا)")
        messagebox.showinfo("Success (کامیابی)", "Password updated!\nLogin with new password next time. (پاس ورڈ تبدیل ہو گیا!\nاگلی بار نئے پاس ورڈ سے لاگ ان کریں)")
        self.logout()
     # ────────────────────────────────────────────────
    #               ADD ADMIN USERNAME
    # ────────────────────────────────────────────────
    def show_change_username(self):
        self.clear_screen()

        # Top Label: Add Username
        tk.Label(
            self.root,
            text="Add Username (یوزر نیم شامل کریں)",  # <-- changed label
            font=("Arial", 24, "bold"),
            bg="#f8fafc",
            fg="#3b82f6"
        ).pack(pady=30)

        frame = tk.Frame(self.root, bg="#f8fafc")
        frame.pack()

        # Input Field Label
        tk.Label(
            frame,
            text="New Username (نیا یوزر نیم)",
            font=("Arial", 15),
            bg="#f8fafc"
        ).pack(anchor="w", padx=90, pady=12)

        self.new_username_entry = tk.Entry(frame, font=("Arial", 15), width=36)
        self.new_username_entry.pack(pady=8)

        # Update Button: Add Username
        tk.Button(
            self.root,
            text="Add (یوزر نیم شامل کریں)",  # <-- changed button text
            font=("Arial", 15, "bold"),
            bg="#14b8a6",
            fg="white",
            width=24,
            command=self.update_username
        ).pack(pady=40)

        # Back Button
        tk.Button(
            self.root,
            text="Back to Menu (واپس مینو پر)",
            font=("Arial", 14),
            fg="#ef4444",
            bg="#f8fafc",
            bd=0,
            command=self.show_main_menu
        ).pack()

    def update_username(self):
        new_user = self.new_username_entry.get().strip()

        if not new_user:
            messagebox.showerror("Error (غلطی)", "Username cannot be empty! (یوزر نیم خالی نہیں ہو سکتا)")
            return

        # Check if new username already exists
        row = self.cursor.execute(
            "SELECT username FROM admin WHERE username=?", (new_user,)
        ).fetchone()
        if row:
            messagebox.showwarning(
                "Warning (خبردار)",
                f"Username '{new_user}' already exists! (یہ یوزر نیم پہلے سے موجود ہے)"
            )
            return

        # Update username in database using current session user
        self.cursor.execute(
            "UPDATE admin SET username=? WHERE username=?",
            (new_user, self.current_user)
        )
        self.conn.commit()

        # Log the action
        self.log_action("Admin Username Changed (یوزر نیم تبدیل کیا گیا)", f"{self.current_user} -> {new_user}")

        # Update current session username
        self.current_user = new_user

        # Show success message
        messagebox.showinfo(
            "Success (کامیابی)",
            f"Username updated to '{new_user}' (یوزر نیم تبدیل ہو گیا: '{new_user}')"
        )

    # ────────────────────────────────────────────────
    #                  HELPERS
    # ────────────────────────────────────────────────
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def logout(self):
        self.log_action("Logout (لاگ آؤٹ)", f"User: {self.current_user}")
        if messagebox.askyesno("Logout (لاگ آؤٹ)", "Really exit? (کیا واقعی بند کرنا چاہتے ہیں؟)"):
            self.root.destroy()
            PharmacyApp()


if __name__ == "__main__":
    app = PharmacyApp()
    app.root.mainloop()