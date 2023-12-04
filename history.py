import tkinter as tk
from tkinter import ttk
import pymysql


def get_customer_orders():
    def search_orders():
        # Retrieve the email or customer ID depending on the filled field
        search_value = search_entry.get()
        if search_by.get() == "Email":
            query = "SELECT * FROM customers WHERE email = %s"
        else:
            query = "SELECT * FROM customers WHERE customer_id = %s"


        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="air_reservation",
            port=8889
        )
        cursor = conn.cursor()

        cursor.execute(query, (search_value,))
        customer_info = cursor.fetchone()

        if customer_info:
            customer_id = customer_info[0]

            # Query to retrieve customer order history
            order_query = "SELECT * FROM orders WHERE customer_id = %s"
            cursor.execute(order_query, (customer_id,))
            orders = cursor.fetchall()

            #Displaying commands in the window
            orders_text.delete(1.0, tk.END)
            for order in orders:
                orders_text.insert(tk.END, f"Order ID: {order[0]}\n"
                                            f"Flight ID: {order[2]}\n"
                                            f"Number of Tickets: {order[3]}\n"
                                            f"Total Price: {order[4]}\n\n")


        else:
            orders_text.delete(1.0, tk.END)
            orders_text.insert(tk.END, "Customer not found!")

        conn.close()

    # Configuring the main
    root = tk.Tk()
    root.title("Customer Orders History")

    # Création des widgets
    search_label = ttk.Label(root, text="Search by:")
    search_label.grid(row=0, column=0)

    search_by = ttk.Combobox(root, values=["Email", "Customer ID"])
    search_by.grid(row=0, column=1)

    search_entry = ttk.Entry(root)
    search_entry.grid(row=0, column=2)

    search_button = ttk.Button(root, text="Search", command=search_orders)
    search_button.grid(row=0, column=3)

    orders_text = tk.Text(root, height=15, width=50)
    orders_text.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

    root.mainloop()


get_customer_orders()
