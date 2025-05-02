import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.filedialog import asksaveasfilename
from db.database import add_product, get_all_products, update_product, delete_product
from utils.pdf_generator import generate_pdf
import csv

class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Inventory Management")
        self.window.geometry("1000x600")

        self.create_widgets()
        self.refresh_products()

        self.window.mainloop()

    def create_widgets(self):
        # Labels and Entry Fields
        tk.Label(self.window, text="Product Name").grid(row=0, column=0, padx=5, pady=5)
        self.product_name_entry = tk.Entry(self.window)
        self.product_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Quantity").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry = tk.Entry(self.window)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Price").grid(row=2, column=0, padx=5, pady=5)
        self.price_entry = tk.Entry(self.window)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Low Stock Threshold").grid(row=3, column=0, padx=5, pady=5)
        self.low_stock_entry = tk.Entry(self.window)
        self.low_stock_entry.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        self.add_btn = tk.Button(self.window, text="Add Product", command=self.handle_add_or_update, bg="#2ecc71", fg="white")
        self.add_btn.grid(row=4, column=1, padx=5, pady=5)

        self.delete_button = tk.Button(self.window, text="Delete Product", command=self.delete_product, bg="#e74c3c", fg="white")
        self.delete_button.grid(row=4, column=0, padx=5, pady=5)

        self.export_csv_btn = tk.Button(self.window, text="Export to CSV", command=self.export_csv)
        self.export_csv_btn.grid(row=5, column=0, padx=5, pady=5)

        self.export_pdf_btn = tk.Button(self.window, text="Export to PDF", command=self.export_pdf)
        self.export_pdf_btn.grid(row=5, column=1, padx=5, pady=5)

        # Search
        tk.Label(self.window, text="Search").grid(row=0, column=2, padx=5, pady=5)
        self.search_entry = tk.Entry(self.window)
        self.search_entry.grid(row=0, column=3, padx=5, pady=5)
        self.search_button = tk.Button(self.window, text="Search", command=self.search_products)
        self.search_button.grid(row=0, column=4, padx=5, pady=5)

        # Treeview
        self.tree = ttk.Treeview(self.window, columns=("ID", "Name", "Quantity", "Price"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.grid(row=6, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

        # Scrollbar
        scrollbar = tk.Scrollbar(self.window, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=6, column=5, sticky='ns')

        # Right-click menu
        self.tree.bind("<Button-3>", self.on_right_click)

    def handle_add_or_update(self):
        name = self.product_name_entry.get().strip()
        qty = self.quantity_entry.get().strip()
        price = self.price_entry.get().strip()
        low_stock = self.low_stock_entry.get().strip()

        if not name or not qty.isdigit() or not price.replace('.', '', 1).isdigit() or not low_stock.isdigit():
            messagebox.showerror("Invalid input", "Please fill all fields correctly.")
            return

        add_product(name, int(qty), float(price), int(low_stock))
        self.clear_entries()
        self.refresh_products()

    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a product to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected product?")
        if not confirm:
            return

        item_id = self.tree.item(selected_item)["values"][0]
        delete_product(item_id)
        self.refresh_products()

    def refresh_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        products = get_all_products()
        for p in products:
            is_low = p[2] <= p[4]
            self.tree.insert("", "end", values=(p[0], p[1], p[2], f"₹{p[3]:.2f}"),
                             tags=("low_stock",) if is_low else ())

        self.tree.tag_configure("low_stock", background="#f9e79f", font=('Segoe UI', 10, 'bold'))

    def on_right_click(self, event):
        selected_item = self.tree.identify_row(event.y)
        if not selected_item:
            return

        self.tree.selection_set(selected_item)

        def load_selected_to_form():
            item = self.tree.item(selected_item)
            values = item["values"]

            self.product_name_entry.delete(0, 'end')
            self.product_name_entry.insert(0, values[1])
            self.quantity_entry.delete(0, 'end')
            self.quantity_entry.insert(0, values[2])
            self.price_entry.delete(0, 'end')
            self.price_entry.insert(0, values[3].replace("₹", ""))

        menu = tk.Menu(self.window, tearoff=0)
        menu.add_command(label="Edit Product", command=load_selected_to_form)
        menu.post(event.x_root, event.y_root)

    def search_products(self):
        search_term = self.search_entry.get().strip().lower()
        all_products = get_all_products()

        self.tree.delete(*self.tree.get_children())

        for p in all_products:
            if search_term in p[1].lower():
                self.tree.insert("", "end", values=(p[0], p[1], p[2], f"₹{p[3]:.2f}"))

    def export_csv(self):
        file_path = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Quantity", "Price"])
            for row_id in self.tree.get_children():
                row = self.tree.item(row_id)['values']
                writer.writerow(row)

        messagebox.showinfo("Exported", "CSV file exported successfully.")

    def export_pdf(self):
        products = get_all_products()
        generate_pdf(products)
        messagebox.showinfo("Exported", "PDF file generated successfully.")

    def clear_entries(self):
        self.product_name_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.low_stock_entry.delete(0, 'end')
