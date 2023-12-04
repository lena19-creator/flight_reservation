import tkinter as tk
from tkinter import Label, Frame, Button, ttk , Entry
from PIL import Image, ImageTk
import pymysql
import subprocess


class EmployeePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to your Employee Page")
        self.flight_window = None

        self.bg_image = Image.open("image3.png")
        self.bg_image = self.bg_image.resize((1200, 800))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.logo_image = Image.open("logo3.png")
        self.logo_image = self.logo_image.resize((100, 100))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        self.logo_label = Label(self.root, image=self.logo_photo, bg="#000000")
        self.logo_label.place(x=1320, y=60)

        self.flight_tree = None

        self.modify_flight_button = Button(self.root, text="Modify Flight", command=self.load_all_flights)
        self.modify_flight_button.pack(pady=10)

        self.add_flight_button = Button(self.root, text="Add Flight", command=self.add_flight)
        self.add_flight_button.pack()


        self.discount_button = Button(self.root, text="Discount", command=self.apply_discount)
        self.discount_button.pack()

        self.sales_analysis_button = Button(self.root, text="Sales Analysis", command=self.sales_analysis)
        self.sales_analysis_button.pack()

    def load_all_flights(self):
        if self.flight_window:
            self.flight_window.destroy()

        self.flight_window = tk.Toplevel(self.root)
        self.flight_tree = ttk.Treeview(self.flight_window)
        self.flight_tree.pack(expand=True, fill='both')

        conn = pymysql.connect(host='localhost', user='root', password='root', db='air_reservation', port=8889)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM flight")
        flight_data = cursor.fetchall()
        conn.close()

        # Insert column names as headings
        headings = [ "Departure City", "Arrival City", "Departure Time", "Arrival Time", "Ticket Price",
                    "Class"]
        self.flight_tree['columns'] = headings
        self.flight_tree.heading("#0", text="ID")

        for i, header in enumerate(headings):
            self.flight_tree.heading(f"#{i + 1}", text=header)
            self.flight_tree.column(f"#{i + 1}", width=100)  # You can adjust the width as needed

        # Insert flight data into Treeview
        for flight in flight_data:
            self.flight_tree.insert("", "end", text=flight[0], values=flight[1:])

        delete_flight_button = tk.Button(self.flight_window, text="Delete Flight", command=self.delete_flight)
        delete_flight_button.pack()

    def modify_flight(self):
        if not self.flight_tree:
            self.load_all_flights()

        selected_item = self.flight_tree.focus()
        flight_values = self.flight_tree.item(selected_item, 'values')

        if flight_values:
            flight_id_to_delete = flight_values[0]
            print("Flight Details:")
            print(f"Flight ID: {flight_values[0]}")
            print(f"Departure City: {flight_values[1]}")
            print(f"Arrival City: {flight_values[2]}")
            # ... (other flight details)

            self.configure_delete_button(flight_id_to_delete)
        else:
            print("No flight selected.")
            # Close the Toplevel window displaying flights
        if self.flight_window:
            self.flight_window.destroy()

    def add_flight(self):
        # Creation of a window to add a flight
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Add a flight ")


        tk.Label(self.add_window, text="ID of the flight: ").pack()
        entry_flight_id = tk.Entry(self.add_window)
        entry_flight_id.pack()

        tk.Label(self.add_window, text="City of departure: ").pack()
        entry_departure_city = tk.Entry(self.add_window)
        entry_departure_city.pack()

        tk.Label(self.add_window, text="City of arrival: ").pack()
        entry_arrival_city = tk.Entry(self.add_window)
        entry_arrival_city.pack()

        tk.Label(self.add_window, text="Hour of departure: ").pack()
        entry_departure_time = tk.Entry(self.add_window)
        entry_departure_time.pack()

        tk.Label(self.add_window, text="Hour of arrival: ").pack()
        entry_arrival_time = tk.Entry(self.add_window)
        entry_arrival_time.pack()

        tk.Label(self.add_window, text="Price of the ticket: ").pack()
        entry_ticket_price = tk.Entry(self.add_window)
        entry_ticket_price.pack()

        tk.Label(self.add_window, text="Class: ").pack()
        entry_class = tk.Entry(self.add_window)
        entry_class.pack()

        # button register to add the flight
        save_button = tk.Button(self.add_window, text="register",
                                command=lambda: self.save_flight(entry_flight_id.get(),
                                                                 entry_departure_city.get(),
                                                                 entry_arrival_city.get(),
                                                                 entry_departure_time.get(),
                                                                 entry_arrival_time.get(),
                                                                 entry_ticket_price.get(),
                                                                 entry_class.get()))
        save_button.pack()

    def save_flight(self, flight_id, departure_city, arrival_city, departure_time, arrival_time, ticket_price,
                    flight_class):
        # Insertion of the data
        conn = pymysql.connect(host='localhost', user='root', password='root', db='air_reservation', port=8889)
        cursor = conn.cursor()


        insert_query = "INSERT INTO flight (flight_id, departure_city, arrival_city, departure_time, arrival_time, ticket_price, classe) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (
        flight_id, departure_city, arrival_city, departure_time, arrival_time, ticket_price, flight_class))

        conn.commit()
        conn.close()


        self.add_window.destroy()

    def delete_flight(self):
        selected_item = self.flight_tree.focus()
        flight_id = self.flight_tree.item(selected_item, 'text')

        if flight_id:
            conn = pymysql.connect(host='localhost', user='root', password='root', db='air_reservation', port=8889)
            cursor = conn.cursor()

            # delete flight
            delete_query = "DELETE FROM flight WHERE flight_id = %s"

            try:
                cursor.execute(delete_query, (flight_id,))
                conn.commit()
                print(f"Flight {flight_id} deleted successfully!")
                self.load_all_flights()
            except pymysql.Error as e:
                conn.rollback()
                print(f"Error deleting flight: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            print("No flight selected.")

    def configure_delete_button(self, flight_id_to_delete):
        delete_flight_button = Button(self.root, text="Delete Flight",
                                      command=lambda: self.delete_flight(flight_id_to_delete))
        delete_flight_button.pack()

    def apply_discount_to_orders(self, discount_percentage):
        # Connect to the database
        conn = pymysql.connect(host='localhost', user='root', password='root', db='air_reservation',port=8889)
        cursor = conn.cursor()

        # Retrieve orders from the database
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()

        # Apply discount to each order
        for order in orders:
            customer_id = order[1]  # Assuming the structure of the orders table, adjust if needed

            # Retrieve customer_type from the customers table
            cursor.execute("SELECT customer_type FROM customers WHERE customer_id = %s", (customer_id,))
            customer_type_result = cursor.fetchone()

            if customer_type_result:
                customer_type = customer_type_result[0]

                # Check if the customer_type is senior or children
                if customer_type in ["senior", "children"]:
                    # Apply the discount to the total_price
                    total_price = float(order[4]) * (1 - float(discount_percentage) / 100)

                    # Update the order with the new total_price
                    update_query = "UPDATE orders SET total_price = %s WHERE order_id = %s"
                    cursor.execute(update_query, (total_price, order[0]))

        conn.commit()
        conn.close()

        print(f"Discount applied to orders for special customers.")

    def apply_discount(self):
        discount_window = tk.Toplevel(self.root)
        tk.Label(discount_window, text="Select passenger type:").pack()
        passenger_type_var = tk.StringVar()
        tk.Radiobutton(discount_window, text="Children", variable=passenger_type_var, value="children").pack()
        tk.Radiobutton(discount_window, text="Senior", variable=passenger_type_var, value="senior").pack()

        tk.Label(discount_window, text="Enter discount percentage:").pack()
        discount_percentage_entry = Entry(discount_window)
        discount_percentage_entry.pack()

        apply_discount_button = tk.Button(discount_window, text="Apply Discount",
                                          command=lambda: self.apply_discount_to_orders(
                                              discount_percentage_entry.get()))
        apply_discount_button.pack()



    def sales_analysis(self):
        subprocess.Popen(["python", "graph.py"])



if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeePage(root)
    root.mainloop()

