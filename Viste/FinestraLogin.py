import tkinter as tk



#window.iconbitmap("immagine") per mettere un icona alla pagina


#per importare un massimo e un minimo per il ridimensionamento della finestra
#window.minsize(400, 100)
#window.maxsize(1000,1000)

#window.attributes("-alpha", 0.5) per rendere la finestra trasparente

#per importare lo stack delle pagine presenti sulla finestra principale di home
#window.attributes("-topmost", 1)

#window.lift() per farla comparire sopra la finestra
#window.lower() per farla comparire sotto una finestra

#label = tk.Label(text="ciao", background="red", pady = 50, padx = 50, foreground ="white", font=("Helvetica", 48), cursor ="pirate")
#label.pack()


"""
frame_immagine = tk.Frame(window_login, bg="red")
frame_immagine.pack(ipadx=100, ipady=100, fill="both", side="left")

frame_login_titolo = tk.Frame(window_login, bg="blue")
frame_login_titolo.pack(ipadx=50, ipady=50, fill="x", side="top")

frame_login_entry = tk.Frame(window_login, bg="green")
frame_login_entry.pack(ipadx=50, ipady=50, fill="x", side="top")

frame_login_button = tk.Frame(window_login, bg="yellow")
frame_login_button.pack(ipadx=50, ipady=50, fill="x", side="top")
"""

def login_gui():
    window_login = tk.Tk()
    window_login.title("Login")
    window_login.geometry("600x400+450+200")
    window_login.resizable(True, True)

    testo_lable = tk.Label(window_login, text="Login", fg="sky blue", font=("Helvetica", 36), justify="center")
    testo_lable.pack()

    email_label = tk.Label(window_login, text="Email")
    email_label.pack(padx=5, pady=5)

    email = tk.StringVar()
    email_entry = tk.Entry(window_login, textvariable=email)
    email_entry.pack(padx=5, pady=5)

    pwd_label = tk.Label(window_login, text="Password")
    pwd_label.pack(padx=5, pady=5)

    pwd = tk.StringVar()
    pwd_entry = tk.Entry(window_login, textvariable=pwd, show="*")
    pwd_entry.pack(padx=5, pady=5)

    login = tk.Button(window_login, text="Login", command=lambda: Cliente.login_account(email_entry.get(), pwd_entry.get()), font=("Helvetica"))
    login.pack()

    register = tk.Button(window_login, text="Register",command=registrati, font=("Helvetica"))
    register.pack()

    window_login.mainloop()

