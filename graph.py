import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import pymysql

def display_flight_orders():
    # Connection to the data base
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="air_reservation",
        port=8889
    )
    cursor = conn.cursor()

    # Request to pour have the number of order of the flight
    query = "SELECT f.departure_city, f.arrival_city, COUNT(o.flight_id) as num_orders " \
            "FROM flight f LEFT JOIN orders o ON f.flight_id = o.flight_id GROUP BY f.flight_id"
    cursor.execute(query)
    result = cursor.fetchall()

    destinations = []
    num_orders = []

    for row in result:
        departure = row[0]
        arrival = row[1]
        num_orders.append(row[2])
        destinations.append(f"{departure} - {arrival}")

    # Creation of the graphics
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(destinations, num_orders, color='blue')
    ax.set_xlabel('Destination (Departure - Arrival)')
    ax.set_ylabel('Number of order')
    ax.set_title('Number of order by flight')

    # Rotation
    plt.xticks(rotation=45, ha='right')


    conn.close()

    # display
    root = tk.Tk()
    root.title('Graphique des commandes par vol')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    tk.mainloop()


display_flight_orders()

