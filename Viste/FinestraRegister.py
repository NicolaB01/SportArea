import tkinter as tk
from Attività.Cliente import *

def register_gui():

    window = tk.Tk()
    window.title("Register")
    window.geometry("600x700+450+200")
    window.resizable(False, False)

    nome_label = tk.Label(window, text="Nome")
    nome_label.pack(padx=5, pady=5)

    nome = tk.StringVar()
    nome_entry = tk.Entry(window, textvariable=nome)
    nome_entry.pack(padx=5, pady=5)
    nome_entry.focus()

    cognome_label = tk.Label(window, text="Cognome")
    cognome_label.pack(padx=5, pady=5)

    cognome = tk.StringVar()
    cognome_entry = tk.Entry(window, textvariable=cognome)
    cognome_entry.pack(padx=5, pady=5)


    cf_label = tk.Label(window, text="Codice fiscale")
    cf_label.pack(padx=5, pady=5)

    cf = tk.StringVar()
    cf_entry = tk.Entry(window, textvariable=cf)
    cf_entry.pack(padx=5, pady=5)


    email_label = tk.Label(window, text="Email")
    email_label.pack(padx=5, pady=5)

    email = tk.StringVar()
    email_entry = tk.Entry(window, textvariable=email)
    email_entry.pack(padx=5, pady=5)


    dn_label = tk.Label(window, text="Data di nascita")
    dn_label.pack(padx=5, pady=5)

    dn = tk.StringVar()
    dn_entry = tk.Entry(window, textvariable=dn)
    dn_entry.pack(padx=5, pady=5)


    nt_label = tk.Label(window, text="Numero di telefono")
    nt_label.pack(padx=5, pady=5)

    nt = tk.StringVar()
    nt_entry = tk.Entry(window, textvariable=nt)
    nt_entry.pack(padx=5, pady=5)


    pwd_label = tk.Label(window, text="Password")
    pwd_label.pack(padx=5, pady=5)

    pwd = tk.StringVar()
    pwd_entry = tk.Entry(window, textvariable=pwd, show="*")
    pwd_entry.pack(padx=5, pady=5)

    register = tk.Button(window, text="Rwgister", command=lambda : Cliente.registra_account(nome_entry.get(),cognome_entry.get(),cf_entry.get(),email_entry.get(),dn_entry.get(),nt_entry.get(),pwd_entry.get()))
    register.pack()

    window.mainloop()