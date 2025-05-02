import sqlite3

DB_NAME = 'inventory.db'

# Function to create the database and products table
def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        quantity INTEGER,
        price REAL,
        low_stock_threshold INTEGER
    )
    """)
    
    conn.commit()
    conn.close()

# Function to get all products
def get_all_products():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def delete_product(product_id):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()


# Function to add a product
def add_product(name, qty, price, low_stock_threshold):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, quantity, price, low_stock_threshold) VALUES (?, ?, ?, ?)",
                   (name, qty, price, low_stock_threshold))
    conn.commit()
    conn.close()

# Function to update a product
def update_product(id, name, qty, price, low_stock_threshold):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name = ?, quantity = ?, price = ?, low_stock_threshold = ? WHERE id = ?",
                   (name, qty, price, low_stock_threshold, id))
    conn.commit()
    conn.close()
