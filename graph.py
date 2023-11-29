import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import pymysql

def display_flight_orders():
    # Connexion à la base de données MySQL
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="air_reservation",
        port=8889
    )
    cursor = conn.cursor()

    # Requête pour récupérer le nombre de commandes par vol avec les détails de départ et d'arrivée
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

    # Création du graphique en barres
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(destinations, num_orders, color='blue')
    ax.set_xlabel('Destinations (Départ - Arrivée)')
    ax.set_ylabel('Nombre de commandes')
    ax.set_title('Nombre de commandes par vol')

    # Rotation des étiquettes de l'axe des abscisses pour éviter le chevauchement
    plt.xticks(rotation=45, ha='right')

    # Fermeture de la connexion à la base de données
    conn.close()

    # Affichage du graphique dans une fenêtre tkinter
    root = tk.Tk()
    root.title('Graphique des commandes par vol')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    tk.mainloop()

# Appel de la fonction pour afficher le graphique
display_flight_orders()

