import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry


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

# Create a frame for the input fields
input_frame = tk.Frame(root)
input_frame.pack(pady=20)

# Create widgets for the input fields
field_names = ["Departure airport", "Arrival airport", "Departing - Returning", "Passengers", "Class"]

widgets = []
for i, field_name in enumerate(field_names):
    label = tk.Label(input_frame, text=field_name, pady=10)
    widget = None

    if i < 3:
        label.grid(row=0, column=i, sticky="w")
        if field_name == "Departure airport":
            capital_cities = ["London", "Paris", "New York", "Tokyo"]
            widget = ttk.Combobox(input_frame, values=capital_cities)
            widget.set("Select Departure Airport")
        elif field_name == "Arrival airport":
            arrival_cities = ["Los Angeles", "Sydney", "Berlin", "Dubai"]
            widget = ttk.Combobox(input_frame, values=arrival_cities)
            widget.set("Select Arrival Airport")
        elif field_name == "Departing - Returning":
            widget = DateEntry(input_frame, width=12)
    else:
        label.grid(row=2, column=i - 3, sticky="w")
        widget = ttk.Entry(input_frame)

    if widget is not None:
        widget.grid(row=1 if i < 3 else 3, column=i if i < 3 else i - 3)
        widgets.append(widget)

# Create a frame for the "Search Flights" button
search_button = tk.Button(input_frame, text="Search Flight", command=search_flights, bg="red")
search_button.grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()
