#receive change
#error logs
#sales report


import tkinter as tk
from tkinter import messagebox

class VendingMachineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vending Machine")
        self.root.geometry("500x700")
        self.root.config(bg="black")
        self.items = {
            "0001": {"name": "Coke", "price": 1.25},
            "0002": {"name": "Fanta", "price": 1.00},
            "0003": {"name": "Sprite", "price": 0.75},
            "0004": {"name": "Water", "price": 1.00},
            "0005": {"name": "Rubicon", "price": 0.85},
            "0006": {"name": "Pepsi", "price": 0.90},
            "0007": {"name": "Vimto", "price": 0.75},
            "0008": {"name": "Rio", "price": 0.60},
            "0009": {"name": "7up", "price": 0.65},
            "0010": {"name": "Lipton", "price": 0.95},
            "0011": {"name": "Monster", "price": 1.30},
            "0012": {"name": "Redbull", "price": 1.45}
        }
        
        self.balance = 0.0
        self.loyalty_discount = 0.10
        self.loyalty_cards = {"customer01", "customer02", "customer03", "customer04"}
        
        self.create_widgets()

    def create_widgets(self):
        display_frame = tk.Frame(self.root, bg="black")
        display_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        row, col = 0, 0
        for code, item in self.items.items():
            item_frame = tk.Frame(display_frame, bg="darkgrey", bd=2, relief="raised")
            item_frame.grid(row=row, column=col, padx=5, pady=5)
            tk.Label(item_frame, text=code, font=("Arial", 10, "bold"), bg="darkgrey").pack()
            tk.Label(item_frame, text=item["name"], font=("Arial", 10), bg="darkgrey").pack()
            tk.Label(item_frame, text=f"£{item['price']:.2f}", font=("Arial", 10), bg="darkgrey").pack()
            
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.balance_label = tk.Label(self.root, text="Balance: £0.00", font=("Arial", 12), bg="black", fg="white")
        self.balance_label.pack(pady=5)

        side_panel = tk.Frame(self.root, bg="black", width=150)
        side_panel.pack(side="right", fill="y", padx=10)

        payment_frame = tk.Frame(side_panel, bg="darkblue", bd=3, relief="sunken")
        payment_frame.pack(pady=10)
        tk.Label(payment_frame, text="Insert Coins", font=("Arial", 12), fg="white", bg="darkblue").pack()
        tk.Button(payment_frame, text="£0.05", command=lambda: self.insert_money(0.05)).pack(padx=5, pady=5)
        tk.Button(payment_frame, text="£0.10", command=lambda: self.insert_money(0.10)).pack(padx=5, pady=5)
        tk.Button(payment_frame, text="£0.20", command=lambda: self.insert_money(0.20)).pack(padx=5, pady=5)
        tk.Button(payment_frame, text="£0.50", command=lambda: self.insert_money(0.50)).pack(padx=5, pady=5)
        tk.Button(payment_frame, text="£1.00", command=lambda: self.insert_money(1.00)).pack(padx=5, pady=5)
        tk.Button(payment_frame, text="£2.00", command=lambda: self.insert_money(2.00)).pack(padx=5, pady=5)

        card_frame = tk.Frame(side_panel, bg="darkgreen", bd=3, relief="sunken")
        card_frame.pack(pady=10)
        self.card_entry = tk.Entry(card_frame, font=("Arial", 10), width=10)
        self.card_entry.pack(pady=5)
        tk.Button(card_frame, text="Apply Loyalty Card", command=self.apply_loyalty_card).pack(padx=5, pady=5)
        tk.Button(card_frame, text="Pay with Card", command=self.pay_with_card).pack(padx=5, pady=5)

        keypad_frame = tk.Frame(side_panel, bg="black")
        keypad_frame.pack(pady=20)
        self.code_entry = tk.Entry(keypad_frame, font=("Arial", 14), justify="center", width=6)
        self.code_entry.grid(row=0, column=0, columnspan=3, pady=10)
        self.create_keypad(keypad_frame)

        tk.Button(side_panel, text="Purchase", command=self.make_purchase, font=("Arial", 12), bg="red", fg="white").pack(pady=15, fill="x")

    def create_keypad(self, frame):
        buttons = [
            ('1', 1, 0), ('2', 1, 1), ('3', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2),
            ('0', 4, 1), ('Clear', 4, 0), ('Enter', 4, 2)
        ]
        for (text, row, col) in buttons:
            if text == 'Clear':
                btn = tk.Button(frame, text=text, width=5, command=self.clear_code)
            elif text == 'Enter':
                btn = tk.Button(frame, text=text, width=5, command=self)
            else:
                btn = tk.Button(frame, text=text, width=5, command=lambda t=text: self.enter_code(t))
            btn.grid(row=row, column=col, padx=2, pady=2)

    def enter_code(self, value):
        self.code_entry.insert(tk.END, value)

    def clear_code(self):
        self.code_entry.delete(0, tk.END)

    def insert_money(self, amount):
        self.balance += amount
        self.update_balance()

    def update_balance(self):
        self.balance_label.config(text=f"Balance: £{self.balance:.2f}")

    def apply_loyalty_card(self):
        code = self.card_entry.get().strip()
        if code in self.loyalty_cards:
            self.discount_applied = True
            messagebox.showinfo("Loyalty Card", "Loyalty card accepted! 10% discount will be applied.")
        else:
            self.discount_applied = False
            messagebox.showwarning("Loyalty Card", "Invalid loyalty card code.")
    
    def pay_with_card(self):
        item_code = self.code_entry.get().strip()
        if item_code not in self.items:
            messagebox.showwarning("Invalid Code", "Item code not found.")
            return

        item = self.items[item_code]
        total_cost = item["price"]
        
        if hasattr(self, 'discount_applied') and self.discount_applied:
            total_cost *= (1 - self.loyalty_discount)

        messagebox.showinfo("Card Payment", f"Payment accepted with card for £{total_cost:.2f}")
        self.clear_code()
        self.discount_applied = False

    def make_purchase(self):
        item_code = self.code_entry.get().strip()
        if item_code not in self.items:
            messagebox.showwarning("Invalid Code", "Item code not found.")
            return
        item = self.items[item_code]
        total_cost = item["price"]
        if hasattr(self, 'discount_applied') and self.discount_applied:
            total_cost *= (1 - self.loyalty_discount)
        if self.balance >= total_cost:
            self.balance -= total_cost
            self.update_balance()
            messagebox.showinfo("Success", f"Enjoy your {item['name']}!")
            self.clear_code()
            self.discount_applied = False
        else:
            messagebox.showwarning("Funds", "Insufficient balance.")

root = tk.Tk()
app = VendingMachineGUI(root)
root.mainloop()
