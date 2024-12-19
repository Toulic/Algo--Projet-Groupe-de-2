import csv
import os
import tkinter as tk
from gestion_users import *
from gestion_produits import *

fichier_utilisateurs = 'Data/users.csv'

if not os.path.exists(fichier_utilisateurs):

    os.makedirs('Data', exist_ok=True)
    
    with open('Data/users.csv', 'w', newline='') as csvfile:
        fieldname = ['Username', 'mdp', 'Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldname)
        writer.writeheader()

while True:
    # Caractéristiques de la fenêtre
    root = tk.Tk()
    root.title("Fenêtre initiale")
    root.geometry("600x250")

    tk.Label(root, text="### MENU DE CONNEXION ###", font=("Arial", 14), pady=10).pack()
    tk.Button(root, text="1. Connexion", bg='lightgrey', command=connexion, width=80).pack(pady=10)
    tk.Button(root, text="2. Inscription", bg='darkgrey', command=inscription, width=80).pack(pady=10)
    tk.Button(root, text="0. Quitter", bg='red', command=exit, width=60).pack(pady=40)

    root.mainloop()



