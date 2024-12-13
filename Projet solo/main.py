import csv
import tkinter as tk
from users import *
from operation_sur_fichier import *

with open('users.csv', 'w', newline='') as csvfile:
    fieldname = ['Username', 'mdp']
    writer = csv.DictWriter(csvfile, fieldnames=fieldname)
    writer.writeheader()

while True:
    # Caractéristiques de la fenêtre
    root = tk.Tk()
    root.title("Gestion des Produits")
    root.geometry("900x500")

    tk.Label(root, text="### MENU DES OPTIONS ###", font=("Arial", 14), pady=10).pack()
    tk.Button(root, text="1. Créer/Réinitialiser le fichier des produits", bg='lightgrey', command=craft_fichier, width=80).pack(pady=10)
    tk.Button(root, text="2. Ajouter un produit", bg='grey', command=ajout, width=80).pack(pady=10)
    tk.Button(root, text="3. Supprimer un produit", bg='grey', command=delete, width=80).pack(pady=10)
    tk.Button(root, text="4. Afficher la liste des produits", bg='grey', command=affiche, width=80).pack(pady=10)
    tk.Button(root, text="5. Rechercher un produit", bg='grey', command=recherche, width=80).pack(pady=10)
    tk.Button(root, text="6. Trier les produits", bg='grey', command=tri_produits, width=80).pack(pady=10)
    tk.Button(root, text="7. Ouvrir la gestion de connexion", bg='yellow', command=connexion, width=100).pack(pady=20)
    tk.Button(root, text="0. Quitter", bg='red', command=exit, width=60).pack(pady=20)

    root.mainloop()



