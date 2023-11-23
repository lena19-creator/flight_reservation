import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import pymysql

def search_flights():
    # Add your code to handle flight search here
    pass

def select_item(event, combobox):
    selected_item = combobox.get()
    print(f"Selected: {selected_item}")

root = tk.Tk()
root.geometry("600x300")
root.configure(bg="white")
root.title("Flight Search")

input_frame = tk.Frame(root)
input_frame.pack(pady=20)

field_names = ["Departure airport", "Arrival airport", "Departing - Returning", "Passengers", "Class"]

widgets = []
for i, field_name in enumerate(field_names):
    label = tk.Label(input_frame, text=field_name, pady=10)
    widget = None

    if i < 3:
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
        elif field_name == "Departing - Returning":
            widget = DateEntry(input_frame, width=12)
        elif field_name == "Passengers":
            passengers_label = tk.Label(input_frame, text="Passengers:")
            passengers_label.grid(row=1, column=1, sticky="w")

            passengers_var = tk.StringVar()
            passengers_dropdown = ttk.Combobox(input_frame, textvariable=passengers_var, values=["Adults", "Children"])
            passengers_dropdown.grid(row=4, column=1, sticky="w")
            passengers_dropdown.set("Adults")
            widget = passengers_dropdown
    else:
        label.grid(row=2, column=i-3, sticky="w")
        if field_name == "Class":
            class_var = tk.StringVar()
            class_dropdown = ttk.Combobox(input_frame, textvariable=class_var, values=["First", "Economy", "Business"])
            class_dropdown.grid(row=3, column=1, columnspan=2, sticky="w")
            class_dropdown.set("Select Class")
            widget = class_dropdown
        else:
            widget = ttk.Entry(input_frame)

    if widget is not None:
        widget.grid(row=1 if i < 3 else 3, column=i if i < 3 else i - 3, sticky="w")
        widgets.append(widget)

passengers_var = tk.StringVar()
passengers_dropdown = ttk.Combobox(input_frame, textvariable=passengers_var, values=["Adult", "Children"])
passengers_dropdown.grid(row=3, column=0, sticky="w")
passengers_dropdown.set("Type of passenger")
widgets.insert(3, passengers_dropdown)

search_button = tk.Button(input_frame, text="Search Flight", command=search_flights, bg="red")
search_button.grid(row=3, column=2, columnspan=3, pady=10)

root.mainloop()


