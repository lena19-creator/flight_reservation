import tkinter as tk

def myclick():
    pass

root = tk.Tk()
root.geometry("1000x600")
root.configure(bg="white")

mylabel = tk.Label(root, text="Welcome to ECEtravel", font=('Helvetica'))
mylabel.pack()

frame = tk.Frame(root)
frame.pack(pady=20)  # Add some padding to center the frame

email_label = tk.Label(frame, text="Email", pady=10)
email_label.grid(row=0, column=0)

txtuserid = tk.Entry(frame, text="Email")
txtuserid.grid(row=0, column=1)


password_label = tk.Label(frame, text="Password", pady=10)
password_label.grid(row=1, column=0)

txtpassword = tk.Entry(frame, show="*")  # Password entry field
txtpassword.grid(row=1, column=1)

logme = tk.Button(root, text="Log in", command=myclick, bg="red")
logme.pack()

create_account = tk.Button(root, text="Create an account", command=myclick, bg="red")
create_account.pack()

enter_guest = tk.Button(root, text="Enter as a guest", command=myclick, bg="red")
enter_guest.pack()

root.mainloop()


