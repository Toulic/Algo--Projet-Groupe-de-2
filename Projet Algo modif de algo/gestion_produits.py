import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
import hashlib

# Fonction qui génère le nom de fichier basé sur l'utilisateur
def get_user_filename(user):
    return f"Data/produits_{user}.csv"


# Fonction qui crée ou réinitialise le fichier CSV pour un utilisateur
def craft_fichier(user):
    try:
        filename = get_user_filename(user)
        df = pd.DataFrame(columns=["Nom", "Prix", "Quantité"])
        df.to_csv(filename, index=False)
        messagebox.showinfo("Info", f"Le fichier CSV pour {user} a été créé/réinitialisé.")
    except Exception as er:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {er}")


# Fonction qui ajoute un produit au fichier CSV spécifique à l'utilisateur
def ajout(user):
    try:
        filename = get_user_filename(user)
        nom = simpledialog.askstring("Nom", "Quel est le nom du produit ?")
        prix = simpledialog.askfloat("Prix", "Quel est le prix du produit (en €) ?")
        Quantité = simpledialog.askinteger("Quantité", "Quelle est la quantité reçue ?")

        # Charger ou créer un DataFrame
        if os.path.exists(filename):
            df = pd.read_csv(filename)
        else:
            df = pd.DataFrame(columns=["Nom", "Prix", "Quantité"])

        # Ajouter le nouveau produit
        new_row = pd.DataFrame([{"Nom": nom, "Prix": prix, "Quantité": Quantité}])
        df = pd.concat([df, new_row], ignore_index=True)

        # Sauvegarder dans le fichier CSV
        df.to_csv(filename, index=False)
        messagebox.showinfo("Info", f"Produit ajouté avec succès dans le fichier de {user}.")
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")


# Fonction qui supprime un produit dans le fichier CSV spécifique à l'utilisateur
def delete(user):
    try:
        filename = get_user_filename(user)
        if not os.path.exists(filename):
            messagebox.showwarning("Erreur", "Le fichier n'existe pas.")
            return

        df = pd.read_csv(filename)
        produit_a_supprimer = simpledialog.askstring("Supprimer", "Nom du produit à supprimer :")

        if produit_a_supprimer not in df["Nom"].values:
            messagebox.showwarning("Info", "Produit introuvable. Aucune ligne supprimée.")
        else:
            df = df[df["Nom"] != produit_a_supprimer]
            df.to_csv(filename, index=False)
            messagebox.showinfo("Info", f"Produit supprimé avec succès du fichier de {user}.")
            
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")


# Fonction qui affiche les produits d'un utilisateur
def affiche(user):
    try:
        filename = get_user_filename(user)
        if not os.path.exists(filename):
            messagebox.showinfo("Liste des Produits", "Aucun produit disponible.")
            return

        df = pd.read_csv(filename)
        if df.empty:
            contenu = "Aucun produit disponible."
        else:
            contenu = df.to_string(index=False)
        messagebox.showinfo("Liste des Produits", contenu)
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")


# Fonction qui recherche un produit dans le fichier CSV d'un utilisateur
def recherche(user):
    try:
        filename = get_user_filename(user)
        if not os.path.exists(filename):
            messagebox.showinfo("Recherche", "Le fichier est vide ou n'existe pas.")
            return

        produit = simpledialog.askstring("Recherche", "Nom du produit à chercher :")
        if not produit:
            messagebox.showinfo("Recherche", "Vous devez entrer un nom de produit.")
            return

        df = pd.read_csv(filename)
        resultats = df[df["Nom"] == produit]

        if not resultats.empty:
            messagebox.showinfo("Résultat", resultats.to_string(index=False))
        else:
            messagebox.showinfo("Résultat", "Aucun produit trouvé avec ce nom.")

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")


# Fonction de tri des produits
def tri_produits(user):
    try:
        filename = get_user_filename(user)
        if not os.path.exists(filename):
            messagebox.showinfo("Erreur", "Le fichier n'existe pas ou est vide.")
            return
        df = pd.read_csv(filename)

        choix = simpledialog.askinteger("Critère de tri", "Choisissez un critère de tri :\n1 - Par nom\n2 - Par prix\n3 - Par quantité")

        if choix not in [1, 2, 3]:
            messagebox.showerror("Erreur", "Choix invalide.")
            return

        colonnes = {1: "Nom", 2: "Prix", 3: "Quantité"}
        critere = colonnes[choix]
        df = df.sort_values(by=critere, ascending=True)
        df.to_csv(filename, index=False)
        messagebox.showinfo("Info", f"Les produits ont été triés par '{critere}' en ordre croissant.")
    
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")


# Fonction qui affiche un graphique des produits avec matplotlib
def graphic(user):
    try:
        filename = get_user_filename(user)
        if not os.path.exists(filename):
            messagebox.showinfo("Erreur", "Le fichier n'existe pas ou est vide.")
            return
        
        plt.clf() #Lorsqu'une fenêtre plt est déjà ouverte, permet de ne pas superposer l'ancien et le nouveau graphe
        df = pd.read_csv(filename)   
        
        choix = simpledialog.askinteger("Critère de schémas", "Choisissez un critère de schéma :\n1 - Par Quantité\n2 - Par prix")
        if choix not in [1, 2]:
            messagebox.showerror("Erreur", "Choix invalide.")
            return
        
        colonnes = {1: "Quantité", 2: "Prix"}
        critere = colonnes[choix]
        plt.pie(df[critere], labels=df['Nom'], autopct="%1.1f%%") 
        plt.title(f"Test de {user}")

        plt.show()    

        
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")


# Fonction qui prépare la connexion, et la rejette si les conditions ne sont pas remplies
def connexion():
    with open('Data/users.csv', 'r', newline='') as csvfile:
        texte = list(csv.reader(csvfile))

    login = simpledialog.askstring("Login", "Quel est votre identifiant ?")
    mdp = simpledialog.askstring("Mot de passe", "Quel est votre mot de passe ?")

    for ligne in texte:
        if ligne[0].strip() == login:
            if ligne[1].strip() != hashlib.sha256(mdp.encode('utf-8')).hexdigest().strip():
                messagebox.showwarning("Erreur", "L'identifiant ou le mot de passe sont incorrects. \nÊtes-vous bien inscrit ?")
                return
            else:
                gestion(login)
                return

    messagebox.showwarning("Erreur", "L'identifiant ou le mot de passe sont incorrects. \nÊtes-vous bien inscrit ?")

# Fonction de gestion des produits pour un utilisateur donné
def gestion(user):
    fenetre_utilisateur = tk.Toplevel()
    fenetre_utilisateur.title("Fenêtre de gestion")
    fenetre_utilisateur.geometry("800x600")
    tk.Label(fenetre_utilisateur, text=f"Bonjour {user}", font=("Arial", 20)).pack(pady=20)
    tk.Button(fenetre_utilisateur, text="1. Créer/Réinitialiser le fichier des produits", bg='lightgrey', command=lambda: craft_fichier(user), width=80).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="2. Ajouter un produit", bg='grey', command=lambda: ajout(user), width=80).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="3. Supprimer un produit", bg='grey', command=lambda: delete(user), width=80).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="4. Afficher la liste des produits", bg='grey', command=lambda: affiche(user), width=80).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="5. Rechercher un produit", bg='grey', command=lambda: recherche(user), width=80).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="6. Trier les produits", bg='grey', command=lambda: tri_produits(user), width=80).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="7. Afficher un graphe des produits", bg='grey', command=lambda: graphic(user), width=80).pack(pady=10)    
    tk.Button(fenetre_utilisateur, text="Fermer", bg='yellow', command=fenetre_utilisateur.destroy).pack(pady=10)
