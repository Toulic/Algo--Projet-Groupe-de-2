import csv
import tkinter as tk
from tkinter import messagebox, simpledialog
import hashlib
import os
import requests
from gestion_suggest import *


def mdp_pwned(mdp):

    test_mdp = hashlib.sha1(mdp.encode('utf-8')).hexdigest().upper()
    debut_mdp = test_mdp[:5] 
    reste_mdp = test_mdp[5:]       

    url = f"https://api.pwnedpasswords.com/range/{debut_mdp}"

    try:
        reponse_been_pwned = requests.get(url)
        if reponse_been_pwned.status_code == 200:
            hashes = reponse_been_pwned.text.splitlines()
            for i in hashes:
                hash_part = i.split(':')[0]
                if hash_part == reste_mdp:
                    return True 
            return False  
        else:
            messagebox.showerror("Erreur", f"Erreur API: {reponse_been_pwned.status_code}")
            return False
    except requests.RequestException as e:
        messagebox.showerror("Erreur", f"Erreur réseau: {e}")
        return False


def ajout_user():
    try:
        with open('Data/users.csv', 'r', newline='') as csvfile:
            texte = list(csv.reader(csvfile))

        with open('Data/users.csv', 'a', newline='') as csvfile:
            fieldname = ['Username', 'mdp', 'salt', 'Name'] 
            writer = csv.DictWriter(csvfile, fieldnames=fieldname)

            username = simpledialog.askstring("Username", "Quel est votre pseudonyme ?").strip()
            valide = False
            while not valide:
                valide = True
                for ligne in texte:
                    if ligne[0].strip() == username:
                        valide = False
                        username = simpledialog.askstring("Username", "Pseudonyme déjà utilisé, veuillez en choisir un autre.").strip()
                        break

            mdp = simpledialog.askstring("Password", "Quel mot de passe voulez-vous ?").strip()
            while mdp_pwned(mdp):
                mdp = simpledialog.askstring("Mot de passe compromis", "Ce mot de passe a été trouvé dans des bases de données compromises.\nVeuillez en choisir un autre.").strip()

            salt = os.urandom(16).hex()
            hash_mdp = hashlib.sha256((mdp + salt).encode('utf-8')).hexdigest().strip()
            name = simpledialog.askstring("Name", "Quel est votre Nom ?")

            writer.writerow({'Username': username, 'mdp': hash_mdp, 'salt': salt, 'Name': name})
            messagebox.showinfo("Info", "Utilisateur créé avec succès.")

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

# Fonction qui permet de changer le mot de passe d'un utilisateur
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
