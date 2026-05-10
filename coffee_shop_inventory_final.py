import tkinter as tk
from tkinter import messagebox
import csv
import os

class InventoryItem:
    def __init__(self, name, quantity, reorder_level, supplier_name="General"):
        self.name = name
        self.quantity = int(quantity)
        self.reorder_level = int(reorder_level)
        self.supplier_name = supplier_name

class Order:
    """Automates the creation of restock orders."""
    def __init__(self, supplier_name, items_to_order):
        self.supplier_name = supplier_name
        self.items_to_order = items_to_order 

    def __str__(self):
        details = "\n".join([f"- {name}: +{qty}" for name, qty in self.items_to_order])
        return f"ORDER FOR: {self.supplier_name}\n{details}\n"

class InventoryManager:
    def __init__(self, filename="inventory.csv"):
        self.items = {}
        self.filename = filename
        self.load_data()

    def add_item(self, name, qty, reorder, supplier="General"):
        self.items[name] = InventoryItem(name, qty, reorder, supplier)
        self.save_data()

    def get_low_stock_report(self):
        return [item for item in self.items.values() if item.quantity <= item.reorder_level]

    def save_data(self):
        """Persists inventory to a CSV file."""
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for item in self.items.values():
                writer.writerow([item.name, item.quantity, item.reorder_level, item.supplier_name])

    def load_data(self):
        """Loads data from CSV on startup."""
        if os.path.exists(self.filename):
            with open(self.filename, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        self.add_item(*row)

class CoffeeInventoryApp:
    def __init__(self, root):
        self.manager = InventoryManager()
        self.root = root
        self.root.title("Coffee Inventory")
        self.root.geometry("400x450")
        
        # [GUI Setup omitted for brevity]
        tk.Label(root, text="Item Name:").pack()
        self.name_entry = tk.Entry(root); self.name_entry.pack()
        tk.Label(root, text="Quantity:").pack()
        self.qty_entry = tk.Entry(root); self.qty_entry.pack()
        tk.Label(root, text="Reorder Level:").pack()
        self.reorder_entry = tk.Entry(root); self.reorder_entry.pack()
        tk.Label(root, text="Supplier:").pack()
        self.supplier_entry = tk.Entry(root); self.supplier_entry.pack()
        
        tk.Button(root, text="Add Item", command=self.add_item).pack(pady=5)
        tk.Button(root, text="Check Orders", command=self.process_orders).pack(pady=5)

    def add_item(self):
        try:
            self.manager.add_item(self.name_entry.get(), int(self.qty_entry.get()), 
                                 int(self.reorder_entry.get()), self.supplier_entry.get())
            messagebox.showinfo("Success", "Item Saved")
        except ValueError:
            messagebox.showerror("Error", "Invalid input")

    def process_orders(self):
        low_items = self.manager.get_low_stock_report()
        # Grouping and Order class instantiation logic
        supplier_groups = {}
        for item in low_items:
            supplier_groups.setdefault(item.supplier_name, []).append((item.name, item.reorder_level * 2))
        
        orders = [str(Order(s, items)) for s, items in supplier_groups.items()]
        messagebox.showwarning("Restock Orders", "\n".join(orders))

if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeInventoryApp(root)
    root.mainloop()
