import sqlite3


db = sqlite3.connect("shop.db")
db.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL);
""")

db.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE);
""")

db.execute("""CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                order_date DATE NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id));
""")


def add_product():
    name = input("Product Name: ")
    category = input("Category: ")
    price = float(input("Price: "))
    db.execute("""
        INSERT INTO products (name, category, price)
        VALUES (?, ?, ?);
    """, (name, category, price))
    db.commit()


def add_customer():
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")
    db.execute("""
        INSERT INTO customers (first_name, last_name, email)
        VALUES (?, ?, ?);
    """, (first_name, last_name, email))
    db.commit()


def add_order():
    customer_id = int(input("Customer id: "))
    product_id = int(input("Product id: "))
    quantity = int(input("Quantity: "))
    db.execute("""
        INSERT INTO orders (customer_id, product_id, quantity, order_date)
        VALUES (?, ?, ?, CURRENT_DATE)
    """, (customer_id, product_id, quantity))
    db.commit()


def get_sum():
    info = db.execute("""
        SELECT SUM(orders.quantity * products.price)
        FROM orders
        INNER JOIN products ON orders.product_id == products.id
    """)
    print("Sum:", *info.fetchone())


def get_users_orders():
    info = db.execute("""
        SELECT c.first_name, COUNT(o.id)
        FROM orders o
        INNER JOIN customers c ON o.customer_id == c.id
        GROUP BY c.first_name
    """)
    print(*info.fetchall())


def get_avg_price():
    info = db.execute("""
        SELECT AVG(p.price * o.quantity)
        FROM products p
        INNER JOIN orders o ON p.id == o.product_id
    """)
    print(*info.fetchone())


def get_popular_category():
    info = db.execute("""
        SELECT p.category, COUNT(o.id) AS count
        FROM orders o
        INNER JOIN products p ON o.product_id == p.id
        GROUP BY p.category
        ORDER BY count DESC
    """)
    print(*info.fetchone())


def get_prices_in_category():
    info = db.execute("""
        SELECT category, COUNT(id) AS count
        FROM products
        GROUP BY category
        ORDER BY count
    """)
    print(*info.fetchall())


def update_price():
    category = input("Category: ")
    db.execute("""
        UPDATE products SET
            price = price * 1.1
        WHERE category = ?
    """, (category,))
    db.commit()


while True:
    print('''
            Select an option:
            1 - Add a product
            2 - Add a client
            3 - Order an item
            4 - View total income
            5 - View the number of orders for each client
            6 - View average order price
            7 - View the most popular category
            8 - View total quantity of products for each category
            9 - Update prices by 10%
            0 - Exit''')

    cmd = int(input("Choose an option: "))
    match cmd:
        case 0:
            db.close()
            break
        case 1:
            add_product()
        case 2:
            add_customer()
        case 3:
            add_order()
        case 4:
            get_sum()
        case 5:
            get_users_orders()
        case 6:
            get_avg_price()
        case 7:
            get_popular_category()
        case 8:
            get_prices_in_category()
        case 9:
            update_price()
