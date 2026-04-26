import tkinter as tk
from tkinter import messagebox

class InventoryItem:
    def __init__(self, name, quantity, reorder_level):
        self.name = name
        self.quantity = int(quantity)
        self.reorder_level = int(reorder_level)

class Supplier:
    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

class InventoryManager:
    def __init__(self):
        # Using a dictionary as a collection for fast lookups
        self.items = {} 
        self.suppliers = []

    def add_item(self, name, qty, reorder):
        self.items[name] = InventoryItem(name, qty, reorder)

    def remove_item(self, name):
        if name in self.items:
            del self.items[name]

    def get_low_stock_report(self):
        # Using a list comprehension to filter items
        return [item.name for item in self.items.values() if item.quantity <= item.reorder_level]

class CoffeeInventoryApp:
    def __init__(self, root):
        self.manager = InventoryManager()
        self.root = root
        self.root.title("Sarah's Coffee Shop Inventory")
        self.root.geometry("400x400")

        # --- GUI Elements ---
        tk.Label(root, text="Item Name:").pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        tk.Label(root, text="Quantity:").pack()
        self.qty_entry = tk.Entry(root)
        self.qty_entry.pack()

        tk.Label(root, text="Reorder Level:").pack()
        self.reorder_entry = tk.Entry(root)
        self.reorder_entry.pack()

        tk.Button(root, text="Add/Update Item", command=self.add_item).pack(pady=5)
        tk.Button(root, text="Check Low Stock", command=self.check_alerts).pack(pady=5)
        tk.Button(root, text="Show Inventory", command=self.show_all).pack(pady=5)

    def add_item(self):
        name = self.name_entry.get()
        qty = self.qty_entry.get()
        reorder = self.reorder_entry.get()
        
        if name and qty and reorder:
            self.manager.add_item(name, qty, reorder)
            messagebox.showinfo("Success", f"{name} updated!")
        else:
            messagebox.showwarning("Error", "All fields are required.")

    def check_alerts(self):
        low_stock = self.manager.get_low_stock_report()
        if low_stock:
            messagebox.showwarning("Low Stock Alert", f"Restock needed for: {', '.join(low_stock)}")
        else:
            messagebox.showinfo("Status", "All stock levels are healthy.")

    def show_all(self):
        report = "\n".join([f"{i.name}: {i.quantity}" for i in self.manager.items.values()])
        messagebox.showinfo("Current Inventory", report if report else "Inventory is empty.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeInventoryApp(root)
    root.mainloop()
