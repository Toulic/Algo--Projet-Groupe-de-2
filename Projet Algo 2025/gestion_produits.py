import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import os
import csv
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
        resultats = df[df["Nom"].str.lower() == produit.lower()]

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


