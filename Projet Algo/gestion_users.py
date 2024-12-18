import csv
import tkinter as tk
from tkinter import messagebox, simpledialog
import hashlib
import os

# Fonction qui ajoute un utilisateur au fichier csv associé
def ajout_user():
    try:
        with open('Data/users.csv', 'r', newline='') as csvfile:
            texte = list(csv.reader(csvfile))

        with open('Data/users.csv', 'a', newline='') as csvfile:
            fieldname = ['Username', 'mdp', 'Name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldname)
            

            username = simpledialog.askstring("Username", "Quel est votre pseudonyme ?").strip()
            valide = False
            while not(valide):
                valide = True
                for ligne in texte:
                    if ligne[0].strip() == username:
                        valide = False
                        username = simpledialog.askstring("Username", "Pseudonyme déjà utilisé, veuillez en choisir un autre.").strip()
                        break


            mdp = simpledialog.askstring("Password", "Quel mot de passe voulez-vous ?").strip()
            hash_mdp = hashlib.sha256(mdp.encode('utf-8')).hexdigest().strip()
            name = simpledialog.askstring("Name", "Quel est votre Nom ?")
            writer.writerow({'Username': username, 'mdp': hash_mdp, 'Name': name})
            messagebox.showinfo("Info", "Utilisateur crée avec succès.")

    except FileNotFoundError:
        messagebox.showerror("Erreur", "Fichier inexistant. Veuillez le créer d'abord.")

# Fonction qui supprime un utilisateur au fichier csv associé
def delete_user():
    with open('Data/users.csv', 'r', newline='') as csvfile:
        texte = list(csv.reader(csvfile)) 

    ligne_delete = simpledialog.askstring("Suppression", "Qui voulez-vous supprimer ?").strip()

    new_texte = [ligne for ligne in texte if ligne[0].strip() != ligne_delete]


    with open('Data/users.csv', "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(new_texte) 

    if os.path.exists(f"Data/produits_{ligne_delete}.csv"):
        os.remove(f"Data/produits_{ligne_delete}.csv")


    messagebox.showinfo("Info", "Utilisateur supprimé avec succès.")

# Fonction qui permet de changer le mot de passe d'un utilisateur  à faire/adapter car guillemets en trop
def modif_mdp():

    with open('Data/users.csv', 'r', newline='') as csvfile:
        texte = list(csv.reader(csvfile))


    user = simpledialog.askstring("Username", "Quel est votre pseudonyme ?").strip()
    old_mdp = simpledialog.askstring("Password", "Quel est votre mot de passe actuel?").strip()

    for ligne in texte:
        if ligne[0].strip() == user:
            if ligne[1].strip() != old_mdp:
                messagebox.showwarning("Erreur", "L'identifiant ou le mot de passe sont incorrects, donc pas touche.")
                return
            else:
                new_mdp = simpledialog.askstring("Password", "Quel est votre nouveau mot de passe ?").strip()
                new_texte = [] 
 
                for ligne in texte:
                    if ligne[0].strip() == user:
                        new_texte.append([ligne[0], new_mdp])   
                    else:
                        new_texte.append(ligne)

                with open('Data/users.csv', "w", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(new_texte) 

                messagebox.showinfo("Info", f"Le mot de passe de l'utilisateur '{user}' a été modifié.")
                return

    messagebox.showwarning("Erreur", f"L'utilisateur '{user}' n'a pas été trouvé.")

# Fonction qui devrait ouvrir une fenetre de gestion utilisateur
def inscription():
    fenetre_utilisateur = tk.Toplevel()
    fenetre_utilisateur.title("Fenêtre d'inscription")
    fenetre_utilisateur.geometry("500x300")
    tk.Label(fenetre_utilisateur, text="### MENU D'INSCRIPTION ###").pack(pady=20)
    tk.Button(fenetre_utilisateur, text="1. Ajouter un utilisateur", bg='#7ACD3D', command=ajout_user, width=60).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="2. Modifier un mot de passe", bg='lightgrey', command=modif_mdp, width=60).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="3. Supprimer un utilisateur", bg='#E36044', command=delete_user, width=60).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="Fermer", bg='yellow', command=fenetre_utilisateur.destroy).pack(pady=10)
