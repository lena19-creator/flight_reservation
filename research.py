import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import pymysql
import subprocess
from tkinter import simpledialog


def get_customer_id(email):
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="air_reservation",
        port=8889
    )
    cursor = conn.cursor()

    # Requête SQL pour récupérer customer_id en fonction de l'email
    query = "SELECT customer_id FROM customers WHERE email = %s"
    cursor.execute(query, (email,))
    customer_id = cursor.fetchone()

    conn.close()
    return customer_id[0] if customer_id else None

def search_flights():
    # Get values from the widgets for search
    departure_city = departure_city_combobox.get()
    arrival_city = arrival_city_combobox.get()
    departure_time = departure_time_cal.get_date()
    arrival_time = arrival_time_cal.get_date()
    classe = class_var.get()

    # Connect to MySQL and perform the search query
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="air_reservation",
        port=8889
    )
    cursor = conn.cursor()

    # Construct the search query based on the selected criteria
    flight_query = ("SELECT * FROM flight WHERE departure_city = %s AND arrival_city = %s AND DATE(departure_time) = DATE(%s) AND "
                    "DATE(arrival_time) = DATE(%s) AND classe = %s")
    cursor.execute(flight_query, (departure_city, arrival_city, departure_time, arrival_time, classe))
    matching_flights = cursor.fetchall()

    print("Matching flights:", matching_flights)  # Print matching flights obtained from the database

    # Close the database connection
    conn.close()

    # Open the FlightApp window and pass the matching flights
    flight_app_window = tk.Toplevel(root)
    app = FlightApp(flight_app_window, matching_flights)




class FlightApp:
    def __init__(self, root, matching_flights):
        self.root = root
        self.root.title("Flight Information")

        # Connect to MySQL
        self.db = pymysql.connect(host='localhost', user='root', password='root', database='air_reservation', port=8889)
        self.cursor = self.db.cursor()

        # Create a frame to hold flight information, Buy buttons, and a vertical scrollbar
        self.frame = ttk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas and add it to the frame
        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar and associate it with the canvas
        v_scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=v_scrollbar.set)

        # Create a frame to contain flight information and Buy buttons inside the canvas
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)

        # Bind the canvas to the scrollbar to enable scrolling
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Populate the inner frame with matching flights
        self.populate_frame(matching_flights)

    def buy_flight(self, flight_id):
        # Ouvre le fichier de paiement en tant que processus distinct
        subprocess.Popen(["python", "payment.py"])

    def save_order(self, flight_id):
        # Demander l'email dans une boîte de dialogue
        email = simpledialog.askstring("Email", "Veuillez entrer votre email : ")

        customer_id = get_customer_id(email)

        if customer_id is not None:
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="root",
                database="air_reservation",
                port=8889
            )
            cursor = conn.cursor()

            # Obtenir le prix du billet à partir de la base de données
            ticket_price_query = "SELECT ticket_price FROM flight WHERE flight_id = %s"
            cursor.execute(ticket_price_query, (flight_id,))
            ticket_price = cursor.fetchone()[0]

            number_of_tickets = 1  # Vous pouvez ajouter cela dans l'interface

            # Insérer la commande dans la table orders
            order_query = "INSERT INTO orders (order_id, customer_id, flight_id, number_of_tickets, total_price) " \
                          "VALUES (NULL, %s, %s, %s, %s)"
            total_price = number_of_tickets * ticket_price
            cursor.execute(order_query, (customer_id, flight_id, number_of_tickets, total_price))
            conn.commit()

            conn.close()
            print("La commande a été enregistrée avec succès.")

    def populate_frame(self, matching_flights):
        # Insert flight information into the inner frame
        for flight in matching_flights:
            flight_frame = ttk.Frame(self.inner_frame, relief=tk.RAISED, borderwidth=2)
            flight_frame.pack(fill=tk.X, padx=10, pady=5)
            button_frame = ttk.Frame(self.inner_frame)
            button_frame.pack(fill=tk.X, padx=10, pady=5)



            # Display flight information
            attributes = ["Departure City", "Arrival City", "Departure Time", "Arrival Time", "Ticket Price", "Class"]
            for i, attribute in enumerate(attributes):
                attribute_label = ttk.Label(flight_frame, text=f"{attribute}:", font=('Arial', 10, 'bold'),
                                            justify=tk.CENTER)
                attribute_label.grid(row=0, column=i * 2, padx=5, pady=5)

                flight_info_label = ttk.Label(flight_frame, text=f"{flight[attributes.index(attribute) + 1]}",
                                              justify=tk.CENTER)
                flight_info_label.grid(row=0, column=i * 2 + 1, padx=5, pady=5)

            # Create a "Buy" button for each flight and bind the buy_flight method
            buy_button = ttk.Button(flight_frame, text="Buy", command=lambda id=flight[0]: self.buy_flight(id))
            buy_button.grid(row=1, columnspan=len(attributes) * 2, pady=10)

            # Create Save button
            save_button = ttk.Button(button_frame, text="Enregistrer commande",
                                     command=lambda id=flight[0]: self.save_order(id))
            save_button.pack(side=tk.LEFT, padx=5)


root = tk.Tk()
root.geometry("600x300")
root.configure(bg="white")
root.title("Flight Search")

input_frame = tk.Frame(root)
input_frame.pack(pady=20)

field_names = ["Departure airport", "Arrival airport", "Departure Time", "Arrival Time", "Passengers", "Class"]

widgets = []
for i, field_name in enumerate(field_names):
    label = tk.Label(input_frame, text=field_name, pady=10)
    widget = None

    if i < 4:
        label.grid(row=0, column=i, sticky="w")
        if field_name in ["Departure airport", "Arrival airport"]:
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="root",
                database="air_reservation",
                port=8889
            )
            cursor = conn.cursor()
            flight_query = "SELECT DISTINCT departure_city FROM flight"  # Update the query accordingly
            cursor.execute(flight_query)
            cities = [row[0] for row in cursor.fetchall()]
            widget = ttk.Combobox(input_frame, values=cities)
            widget.set(f"Select {field_name}")
            if field_name == "Departure airport":
                departure_city_combobox = widget
            elif field_name == "Arrival airport":
                arrival_city_combobox = widget
        elif field_name in ["Departure Time", "Arrival Time"]:
            widget = DateEntry(input_frame, width=12, date_pattern='yyyy-mm-dd')
            if field_name == "Departure Time":
                departure_time_cal = widget
            elif field_name == "Arrival Time":
                arrival_time_cal = widget
    else:
        label.grid(row=2, column=i - 4, sticky="w")
        if field_name == "Class":
            class_var = tk.StringVar()
            class_dropdown = ttk.Combobox(input_frame, textvariable=class_var, values=["First", "Economy", "Business"])
            class_dropdown.grid(row=3, column=1, columnspan=2, sticky="w")
            class_dropdown.set("Select Class")
            widgets.insert(3, class_dropdown)

    if widget is not None:
        widget.grid(row=1 if i < 4 else 3, column=i if i < 4 else i - 4, sticky="w")
        widgets.append(widget)

passengers_var = tk.StringVar()
passengers_dropdown = ttk.Combobox(input_frame, textvariable=passengers_var, values=["Adult", "Children", "Senior"])
passengers_dropdown.grid(row=3, column=0, sticky="w")
passengers_dropdown.set("Type of passenger")
widgets.insert(3, passengers_dropdown)

search_button = tk.Button(input_frame, text="Search Flight", command=search_flights, bg="red")
search_button.grid(row=3, column=2, columnspan=3, pady=10)

root.mainloop()