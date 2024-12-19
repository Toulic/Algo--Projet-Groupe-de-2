import csv
import os
import tkinter as tk
#from gestion_users import *
#from gestion_produits import *
#from gestion_suggest import *
from gestion_fenetres import *

if not os.path.exists('Data/users.csv'):

    os.makedirs('Data', exist_ok=True)
    
    with open('Data/users.csv', 'w', newline='') as csvfile:
        fieldname = ['Username', 'mdp', 'Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldname)
        writer.writeheader()

if not os.path.exists('Data/admin.csv'):

    os.makedirs('Data', exist_ok=True)
    
    with open('Data/admin.csv', 'w', newline='') as csvfile:
        fieldname = ['Username', 'mdp', 'Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldname)
        writer.writeheader()
        writer.writerow({'Username': 'admin', 'mdp': hashlib.sha256('admin'.encode('utf-8')).hexdigest().strip(), 'Name': 'admin'})

if not os.path.exists('Data/mdp_suggest.csv'):

    os.makedirs('Data', exist_ok=True)
    
    with open('Data/mdp_suggest.csv', 'w', newline='') as csvfile:
        fieldname = ['lettres', 'chiffres', 'speciaux']
        writer = csv.DictWriter(csvfile, fieldnames=fieldname)
        writer.writeheader()
        writer.writerow({'lettres': 'abcdefghijklmnopqrstuvwxyz', 'chiffres': '0123456789', 'speciaux': '&()-_~[]|`^%*!?<>'})

while True:
    # Caractéristiques de la fenêtre
    root = tk.Tk()
    root.title("Fenêtre initiale")
    root.geometry("600x300")

    tk.Label(root, text="### MENU DE CONNEXION ###", font=("Arial", 14), pady=10).pack()
    tk.Button(root, text="1. Connexion", bg='lightgrey', command=connexion, width=80).pack(pady=10)
    tk.Button(root, text="2. Inscription", bg='darkgrey', command=inscription, width=80).pack(pady=10)
    tk.Button(root, text="3. Admin", bg='darkgrey', command=connexion_admin, width=80).pack(pady=10)
    tk.Button(root, text="Test", bg='darkgrey', command=mdp_suggest, width=80).pack(pady=10)
    tk.Button(root, text="0. Quitter", bg='red', command=exit, width=60).pack(pady=40)

    root.mainloop()



