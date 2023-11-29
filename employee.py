import tkinter as tk
from tkinter import Label, Frame, Button, ttk
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
        # Créer une nouvelle fenêtre pour ajouter un vol
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Ajouter un Vol")

        # Champs de saisie pour les détails du vol
        tk.Label(self.add_window, text="ID du Vol: ").pack()
        entry_flight_id = tk.Entry(self.add_window)
        entry_flight_id.pack()

        tk.Label(self.add_window, text="Ville de Départ: ").pack()
        entry_departure_city = tk.Entry(self.add_window)
        entry_departure_city.pack()

        tk.Label(self.add_window, text="Ville d'Arrivée: ").pack()
        entry_arrival_city = tk.Entry(self.add_window)
        entry_arrival_city.pack()

        tk.Label(self.add_window, text="Heure de Départ: ").pack()
        entry_departure_time = tk.Entry(self.add_window)
        entry_departure_time.pack()

        tk.Label(self.add_window, text="Heure d'Arrivée: ").pack()
        entry_arrival_time = tk.Entry(self.add_window)
        entry_arrival_time.pack()

        tk.Label(self.add_window, text="Prix du Billet: ").pack()
        entry_ticket_price = tk.Entry(self.add_window)
        entry_ticket_price.pack()

        tk.Label(self.add_window, text="Classe: ").pack()
        entry_class = tk.Entry(self.add_window)
        entry_class.pack()

        # Bouton "Enregistrer" pour ajouter le vol
        save_button = tk.Button(self.add_window, text="Enregistrer",
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
        # Insérer ces valeurs dans la base de données (INSERT INTO...)
        conn = pymysql.connect(host='localhost', user='root', password='root', db='air_reservation', port=8889)
        cursor = conn.cursor()

        # Exemple d'insertion dans la table flight (veuillez ajuster la requête en fonction de votre base de données)
        insert_query = "INSERT INTO flight (flight_id, departure_city, arrival_city, departure_time, arrival_time, ticket_price, classe) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (
        flight_id, departure_city, arrival_city, departure_time, arrival_time, ticket_price, flight_class))

        conn.commit()
        conn.close()

        # Fermer la fenêtre après avoir ajouté le vol
        self.add_window.destroy()

    def delete_flight(self):
        selected_item = self.flight_tree.focus()
        flight_id = self.flight_tree.item(selected_item, 'text')

        if flight_id:
            conn = pymysql.connect(host='localhost', user='root', password='root', db='air_reservation', port=8889)
            cursor = conn.cursor()

            # Requête SQL pour supprimer un vol en fonction de son ID
            delete_query = "DELETE FROM flight WHERE flight_id = %s"

            try:
                cursor.execute(delete_query, (flight_id,))
                conn.commit()
                print(f"Flight {flight_id} deleted successfully!")
                self.load_all_flights()  # Recharge les vols après suppression
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
    def apply_discount(self):
        pass

    def sales_analysis(self):
        subprocess.Popen(["python", "graph.py"])



if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeePage(root)
    root.mainloop()

