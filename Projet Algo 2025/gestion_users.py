import csv
import tkinter as tk
from tkinter import messagebox, simpledialog
import hashlib
import os
import requests
import pandas as pd
import datetime as dt
from email_validator import validate_email, EmailNotValidError

# Fonction qui utilise l'API Have I Been Pwned pour vérifier les mots de passes compromis
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
                hash_part, nb_compromis = i.split(':') 
                if hash_part == reste_mdp:
                    return True, nb_compromis
            return False, 0 
        else:
            messagebox.showerror("Erreur", f"Erreur API: {reponse_been_pwned.status_code}")
            return False, 0
    except requests.RequestException as e:
        messagebox.showerror("Erreur", f"Erreur réseau: {e}")
        return False, 0

# Fonction qui hash un mot de passe
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Fonction qui genere le rockyou.csv
def generate_hashed_passwords(rockyou_file='rockyou.txt', output_file='Data/rockyou.csv', max_passwords=1000000):
    with open(rockyou_file, 'r', encoding='utf-8', errors='ignore') as file, \
            open(output_file, 'w', newline='', encoding='utf-8') as csvfile:

        writer = csv.writer(csvfile)
        writer.writerow(['Password', 'Hashed Password'])

        count = 0
        for line in file:
            if count >= max_passwords:
                break
            password = line.strip()
            hashed_password = hash_password(password)
            writer.writerow([password, hashed_password])
            count += 1

    messagebox.showinfo("Succès", f'Fichier CSV créé avec succès : {output_file}')

# Fonction qui vérifie le mot de passe compromis avec rockyou.csv
def is_weak_password(password, rockyou_file='Data/rockyou.csv'):
    try:
        df = pd.read_csv(rockyou_file)
        
        if 'Password' not in df.columns:
            raise ValueError("Le fichier CSV doit contenir la colonne 'Password'.")

        if password in df['Password'].values:
            return True 
        
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Le fichier de mots de passe est manquant.")
    except ValueError as ve:
        messagebox.showerror("Erreur", str(ve))
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
    
    return False  

def ajout_user():
    try:
        with open('Data/users.csv', 'r', newline='') as csvfile:
            texte = list(csv.reader(csvfile))

        with open('Data/users.csv', 'a', newline='') as csvfile:
            fieldname = ['Username', 'mdp', 'sel', 'Name', 'mail']
            writer = csv.DictWriter(csvfile, fieldnames=fieldname)
            df = pd.read_csv('Data/users.csv')

            username = simpledialog.askstring("Username", "Quel est votre pseudonyme ?").strip()            
            valide = False
            if df.empty:
                valide = True
            while not valide:
                valide = True
                for ligne in texte:
                    if ligne and ligne[0].strip() == username:
                        valide = False
                        username = simpledialog.askstring("Username", "Pseudonyme déjà utilisé, veuillez en choisir un autre.").strip()
                        break

            mdp = simpledialog.askstring("Password", "Quel mot de passe voulez-vous ?").strip()

            # Vérification si le mot de passe est faible (en comparant avec le fichier CSV des mots de passe hachés)
            while is_weak_password(mdp):  
                messagebox.showwarning("Mot de passe faible", "Le mot de passe que vous avez choisi a été trouvé dans une base de données de mots de passe compromis (rockyou.txt).\nVeuillez choisir un autre mot de passe.")
                mdp = simpledialog.askstring("Mot de passe", "Veuillez entrer un mot de passe plus sécurisé :").strip()
            sel = os.urandom(16).hex()
            hash_mdp = hashlib.sha256((mdp + sel).encode('utf-8')).hexdigest().strip()

            name = simpledialog.askstring("Name", "Quel est votre Nom ?")

            mail = simpledialog.askstring("Email", "Quelle est votre adresse e-mail ?").strip()
            email_valide = False
            while not email_valide:
                try:
                    # Valider l'adresse e-mail avec email-validator
                    validation = validate_email(mail)
                    mail = validation.email  # Normaliser l'e-mail (enlever espaces, etc.)
                    email_valide = True
                except EmailNotValidError as e:
                    messagebox.showwarning("E-mail invalide", f"L'adresse e-mail est invalide : {str(e)}")
                    mail = simpledialog.askstring("Email", "Veuillez entrer une adresse e-mail valide :").strip()

            writer.writerow({'Username': username, 'mdp': hash_mdp,'sel': sel, 'Name': name, 'mail':  mail})
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
def modif_mdp(user):
    try:
        df = pd.read_csv('Data/users.csv')
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Le fichier des utilisateurs est introuvable.")
        return

    old_mdp = simpledialog.askstring("Password", "Quel est votre mot de passe actuel ?").strip()
    utilisateur = df[df['Username'] == user]

    if utilisateur.empty:
        messagebox.showwarning("Erreur", f"L'utilisateur '{user}' n'a pas été trouvé.")
        return

    sel = utilisateur.iloc[0]['sel']
    hash_stocke = utilisateur.iloc[0]['mdp']
    hash_teste = hashlib.sha256((old_mdp + sel).encode('utf-8')).hexdigest()

    if hash_teste != hash_stocke:
        messagebox.showwarning("Erreur", "Mot de passe actuel incorrect.")
        return
    new_mdp = simpledialog.askstring("Password", "Quel est votre nouveau mot de passe ?").strip()

    while True:
        if mdp_pwned(new_mdp):
           new_mdp = simpledialog.askstring("Password compromis", "Ce mot de passe aussi est compromis, quitte à changer autant le faire bien").strip()
        else:
            break

    new_sel = os.urandom(16).hex()
    new_hash = hashlib.sha256((new_mdp + new_sel).encode('utf-8')).hexdigest()

    df.loc[df['Username'] == user, 'mdp'] = new_hash
    df.loc[df['Username'] == user, 'sel'] = new_sel

    try:
        df.to_csv('Data/users.csv', index=False)
        messagebox.showinfo("Info", f"Le mot de passe de l'utilisateur '{user}' a été modifié avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde des modifications : {str(e)}")