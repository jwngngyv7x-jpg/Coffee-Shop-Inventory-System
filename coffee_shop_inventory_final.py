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
        if not name.strip():
            raise ValueError("Item name cannot be empty")
        self.items[name] = InventoryItem(name, qty, reorder, supplier)
        self.save_data()

    def update_item(self, name, qty, reorder, supplier="General"):
        """Update an existing item's details."""
        if name not in self.items:
            raise ValueError(f"Item '{name}' not found")
        self.items[name] = InventoryItem(name, qty, reorder, supplier)
        self.save_data()

    def delete_item(self, name):
        """Remove an item from inventory."""
        if name in self.items:
            del self.items[name]
            self.save_data()
        else:
            raise ValueError(f"Item '{name}' not found")

    def get_low_stock_report(self):
        return [item for item in self.items.values() if item.quantity <= item.reorder_level]

    def save_data(self):
        """Persists inventory to a CSV file."""
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for item in self.items.values():
                writer.writerow([item.name, item.quantity, item.reorder_level, item.supplier_name])

    def load_data(self):
        """Loads data from CSV on startup. FIXED: No recursion with add_item()"""
        if os.path.exists(self.filename):
            with open(self.filename, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and len(row) >= 3:
                        # Direct assignment to avoid calling add_item() and triggering save
                        name = row[0]
                        self.items[name] = InventoryItem(
                            name, 
                            row[1], 
                            row[2], 
                            row[3] if len(row) > 3 else "General"
                        )

class CoffeeInventoryApp:
    def __init__(self, root):
        self.manager = InventoryManager()
        self.root = root
        self.root.title("Coffee Inventory System")
        self.root.geometry("500x550")
        
        # Header
        tk.Label(root, text="☕ Coffee Shop Inventory", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Input Frame
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Item Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = tk.Entry(input_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Quantity:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.qty_entry = tk.Entry(input_frame, width=20)
        self.qty_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Reorder Level:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.reorder_entry = tk.Entry(input_frame, width=20)
        self.reorder_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Supplier:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.supplier_entry = tk.Entry(input_frame, width=20)
        self.supplier_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Button Frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Add Item", command=self.add_item, bg="green", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Update Item", command=self.update_item, bg="blue", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Item", command=self.delete_item, bg="red", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        
        # Action Buttons
        action_frame = tk.Frame(root)
        action_frame.pack(pady=10)
        
        tk.Button(action_frame, text="Check Orders", command=self.process_orders, bg="orange", fg="white", width=20).pack(pady=5)
        tk.Button(action_frame, text="View All Items", command=self.view_all_items, bg="purple", fg="white", width=20).pack(pady=5)
        
        # Status/Info Display
        self.info_text = tk.Text(root, height=10, width=60)
        self.info_text.pack(pady=10, padx=10)
        
        self.refresh_display()

    def clear_inputs(self):
        """Clear all input fields."""
        self.name_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)
        self.reorder_entry.delete(0, tk.END)
        self.supplier_entry.delete(0, tk.END)

    def refresh_display(self):
        """Update the info display with current items."""
        self.info_text.delete(1.0, tk.END)
        if not self.manager.items:
            self.info_text.insert(tk.END, "No items in inventory yet.")
            return
        
        self.info_text.insert(tk.END, "CURRENT INVENTORY:\n" + "="*50 + "\n")
        for item in self.manager.items.values():
            status = "⚠️ LOW" if item.quantity <= item.reorder_level else "✓ OK"
            self.info_text.insert(tk.END, 
                f"{item.name} | Qty: {item.quantity} | Reorder: {item.reorder_level} | Supplier: {item.supplier_name} | {status}\n")

    def add_item(self):
        try:
            name = self.name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Item name cannot be empty")
                return
            
            qty = int(self.qty_entry.get())
            reorder = int(self.reorder_entry.get())
            supplier = self.supplier_entry.get().strip() or "General"
            
            if qty < 0 or reorder < 0:
                messagebox.showerror("Error", "Quantity and reorder level must be non-negative")
                return
            
            self.manager.add_item(name, qty, reorder, supplier)
            messagebox.showinfo("Success", f"Item '{name}' added successfully!")
            self.clear_inputs()
            self.refresh_display()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

    def update_item(self):
        try:
            name = self.name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter an item name to update")
                return
            
            if name not in self.manager.items:
                messagebox.showerror("Error", f"Item '{name}' not found in inventory")
                return
            
            qty = int(self.qty_entry.get())
            reorder = int(self.reorder_entry.get())
            supplier = self.supplier_entry.get().strip() or "General"
            
            if qty < 0 or reorder < 0:
                messagebox.showerror("Error", "Quantity and reorder level must be non-negative")
                return
            
            self.manager.update_item(name, qty, reorder, supplier)
            messagebox.showinfo("Success", f"Item '{name}' updated successfully!")
            self.clear_inputs()
            self.refresh_display()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

    def delete_item(self):
        try:
            name = self.name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter an item name to delete")
                return
            
            if messagebox.askyesno("Confirm", f"Delete '{name}' from inventory?"):
                self.manager.delete_item(name)
                messagebox.showinfo("Success", f"Item '{name}' deleted successfully!")
                self.clear_inputs()
                self.refresh_display()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def view_all_items(self):
        """Display all items in inventory."""
        self.refresh_display()
        messagebox.showinfo("Inventory View", f"Total items: {len(self.manager.items)}\n\nSee display area for details.")

    def process_orders(self):
        low_items = self.manager.get_low_stock_report()
        
        if not low_items:
            messagebox.showinfo("Restock Orders", "No items need restocking! ✓")
            return
        
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
