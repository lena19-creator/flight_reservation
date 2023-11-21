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
def create_account():
    # Get user input from the entry fields
    email = txtuserid.get()
    password = txtpassword.get()

    # Connect to the MySQL database (replace with your database details)
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="air_reservation"
    )

    # Create a cursor object
    cursor = conn.cursor()

    # Insert the new user into the 'users' table
    insert_query = "INSERT INTO customers (email, password) VALUES (%s, %s)"
    values = (email, password)

    try:
        cursor.execute(insert_query, values)
        conn.commit()
        print("User added successfully to the database")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    # Close the cursor and database connection
    cursor.close()
    conn.close()

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

enter_guest = tk.Button(root, text="Enter as a guest", command=myclick, bg="red")
enter_guest.pack()

root.mainloop()