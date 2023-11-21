import tkinter as tk
import pymysql

# Function to perform login verification
def myclick():
    # Get user input from the entry fields
    email = txtuserid.get()
    password = txtpassword.get()

    # Connect to the MySQL database (replace with your database details)
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='air_reservation',
        port=8889
    )

    # Create a cursor object
    cursor = conn.cursor()

    # Check if the entered email and password exist in the 'users' table
    select_query = "SELECT * FROM users WHERE email = %s AND password = %s"
    values = (email, password)

    cursor.execute(select_query, values)
    user_data = cursor.fetchone()

    if user_data:
        print("Login successful!")
        # You can add code here to navigate to another window or perform other actions upon successful login
    else:
        print("Invalid login credentials")

    # Close the cursor and database connection
    cursor.close()
    conn.close()

# Function to handle creating an account and adding the user to the database
def save_to_database(username, password, name, email, phone):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='air_reservation',
        port=8889
    )

    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO customers (customer_type, username, password, name, email, phone) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, ('regular', username, password, name, email, phone))
            conn.commit()

            messagebox.showinfo("Success", "Account created successfully!")
    except pymysql.Error as e:
        messagebox.showerror("Error", f"Error in database: {e}")
    finally:
        conn.close()
def save_guest_to_database(guest_name):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='air_reservation',
        port=8889
    )

    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO guest (username) VALUES (%s)"
            cursor.execute(sql, (guest_name,))
            conn.commit()
            print("Guest added successfully!")
    except pymysql.Error as e:
        print(f"Error in database: {e}")
    finally:
        conn.close()



def create_account():
    def save_to_database_from_input():
        username = username_entry.get()
        password = password_entry.get()
        name = name_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        save_to_database(username, password, name, email, phone)

    create_account_window = tk.Toplevel(root)
    create_account_window.title("Create an Account")

    tk.Label(create_account_window, text="Username:").pack()
    username_entry = tk.Entry(create_account_window)
    username_entry.pack()

    tk.Label(create_account_window, text="Password:").pack()
    password_entry = tk.Entry(create_account_window, show="*")
    password_entry.pack()

    tk.Label(create_account_window, text="Name:").pack()
    name_entry = tk.Entry(create_account_window)
    name_entry.pack()

    tk.Label(create_account_window, text="Email:").pack()
    email_entry = tk.Entry(create_account_window)
    email_entry.pack()

    tk.Label(create_account_window, text="Phone:").pack()
    phone_entry = tk.Entry(create_account_window)
    phone_entry.pack()

    tk.Button(create_account_window, text="Create Account", command=save_to_database_from_input).pack()

# GUI setup
root = tk.Tk()
root.geometry("1200x600")
root.configure(bg="white")

mylabel = tk.Label(root, text="Welcome to ECEtravel", font=('Helvetica'))
mylabel.pack()

frame = tk.Frame(root, bg="gray90", padx=50, pady=20)  # Increase padx for wider frame
frame.pack()

email_label = tk.Label(frame, text="Email", pady=20, bg="gray90", fg="black")  # Set background and text colour
email_label.grid(row=0, column=0)

txtuserid = tk.Entry(frame, text="Email", width=30)  # Increase width for wider Entry
txtuserid.grid(row=0, column=1)

password_label = tk.Label(frame, text="Password", pady=10, bg="gray90", fg="black")  # Set background and text colour
password_label.grid(row=1, column=0)

txtpassword = tk.Entry(frame, show="*", width=30)  # Increase width for wider Entry
txtpassword.grid(row=1, column=1)

logme = tk.Button(root, text="Log in", command=myclick, bg="red")
logme.pack()

# Link the "Create an account" button to the new function
create_account_button = tk.Button(root, text="Create an account", command=create_account, bg="red")
create_account_button.pack()

def enter_as_guest():
    def save_guest_to_database():
        guest_name = guest_name_entry.get()
        save_guest_to_database(guest_name)

    guest_window = tk.Toplevel(root)
    guest_window.title("Enter as a Guest")

    tk.Label(guest_window, text="Guest Name:").pack()
    guest_name_entry = tk.Entry(guest_window)
    guest_name_entry.pack()

    tk.Button(guest_window, text="Enter as a Guest", command=save_guest_to_database).pack()

def save_guest_to_database(guest_name):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='air_reservation',
        port=8889
    )

    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO guest (username) VALUES (%s)"
            cursor.execute(sql, (guest_name,))
            conn.commit()
            print("Guest added successfully!")
    except pymysql.Error as e:
        print(f"Error in database: {e}")
    finally:
        conn.close()

enter_guest = tk.Button(root, text="Enter as a guest", command=enter_as_guest, bg="red")
enter_guest.pack()

root.mainloop()