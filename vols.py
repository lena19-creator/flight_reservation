import tkinter as tk
from tkinter import ttk
import pymysql

class FlightApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Information")

        # Connect to MySQL
        self.db = pymysql.connect(host='localhost', user='root', password='root', database='air_reservation',port=8889)
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

        # Fetch flight information and populate the inner frame
        self.populate_frame()

    def buy_flight(self, flight_id):
        # Add your code to handle buying the flight
        print(f"Bought flight with ID {flight_id}")

    def populate_frame(self):
        # Execute the SQL query to fetch flight information
        self.cursor.execute("SELECT * FROM flight")
        flights = self.cursor.fetchall()

        # Insert flight information into the inner frame
        for flight in flights:
            flight_frame = ttk.Frame(self.inner_frame, relief=tk.RAISED, borderwidth=2)
            flight_frame.pack(fill=tk.X, padx=10, pady=5)

            # Display flight information
            attributes = ["Departure City", "Arrival City", "Departure Time", "Arrival Time", "Ticket Price", "Class"]
            for i, attribute in enumerate(attributes):
                attribute_label = ttk.Label(flight_frame, text=f"{attribute}:", font=('Arial', 10, 'bold'), justify=tk.CENTER)
                attribute_label.grid(row=0, column=i * 2, padx=5, pady=5)

                flight_info_label = ttk.Label(flight_frame, text=f"{flight[attributes.index(attribute) + 1]}", justify=tk.CENTER)
                flight_info_label.grid(row=0, column=i * 2 + 1, padx=5, pady=5)

            # Create a "Buy" button for each flight and bind the buy_flight method
            buy_button = ttk.Button(flight_frame, text="Buy", command=lambda id=flight[0]: self.buy_flight(id))
            buy_button.grid(row=1, columnspan=len(attributes) * 2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FlightApp(root)
    root.geometry("800x400")  # Set a larger size for the window
    root.mainloop()

