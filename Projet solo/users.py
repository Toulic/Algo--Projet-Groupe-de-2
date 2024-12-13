import csv
import operation_sur_fichier
import tkinter as tk
from tkinter import messagebox, simpledialog

# Fonction qui ajoute un utilisateur au fichier csv associé
def ajout_user():
    try:
        with open('users.csv', 'a', newline='') as csvfile:
            fieldname = ['Username', 'mdp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldname)

            username = simpledialog.askstring("Username", "Quel est votre pseudonyme ?").strip()
            mdp = simpledialog.askstring("Password", "Quel mot de passe voulez-vous ?")
            writer.writerow({'Username': username, 'mdp': mdp})
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Fichier inexistant. Veuillez le créer d'abord.")

# Fonction qui supprime un utilisateur au fichier csv associé
def delete_user():
    with open("users.csv", 'r', newline='') as csvfile:
        texte = list(csv.reader(csvfile)) 

    ligne_delete = simpledialog.askstring("Suppression", "Qui voulez-vous supprimer").strip()

    new_texte = [ligne for ligne in texte if ligne[0].strip() != ligne_delete]


    with open("users.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(new_texte) 

    messagebox.showinfo("Info", "Utilisateur supprimé avec succès.")

# Fonction qui permet de changer le mot de passe d'un utilisateur  à faire/adapter car guillemets en trop
def modif_mdp():

    with open("users.csv", 'r', newline='') as csvfile:
        texte = list(csv.reader(csvfile))


    user = simpledialog.askstring("Username", "Quel est votre pseudonyme ?").strip()
    new_mdp = simpledialog.askstring("Password", "Quel est nouveau mot de passe ?").strip()

    new_texte = [] 


    user_found = False  
    for ligne in texte:
        if ligne[0].strip() == user:
            new_texte.append([ligne[0], new_mdp]) 
            user_found = True  
        else:
            new_texte.append(ligne)

    if user_found:
        with open("users.csv", "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(new_texte) 

        messagebox.showinfo("Info", f"Le mot de passe de l'utilisateur '{user}' a été modifié.")
    else:
        messagebox.showwarning("Erreur", f"L'utilisateur '{user}' n'a pas été trouvé.")

# Fonction qui devrait ouvrir une fenetre de gestion utilisateur
def connexion():
    fenetre_utilisateur = tk.Toplevel()
    fenetre_utilisateur.title("Fenêtre de connexion")
    fenetre_utilisateur.geometry("500x300")
    tk.Label(fenetre_utilisateur, text="### MENU DE CONNEXION ###").pack(pady=20)
    tk.Button(fenetre_utilisateur, text="1. Ajouter un utilisateur", bg='#7ACD3D', command=ajout_user, width=60).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="2. Modifier un mot de passe", bg='lightgrey', command=modif_mdp, width=60).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="3. Supprimer un utilisateur", bg='#E36044', command=delete_user, width=60).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="Fermer", bg='yellow', command=fenetre_utilisateur.destroy).pack(pady=10)
