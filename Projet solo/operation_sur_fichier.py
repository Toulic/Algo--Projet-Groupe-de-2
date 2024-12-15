import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import os

FILENAME = "produits.csv"

# Fonction qui crée le fichier CSV
def craft_fichier():
    df = pd.DataFrame(columns=["Nom", "Prix", "Quantité"])
    df.to_csv(FILENAME, index=False)
    messagebox.showinfo("Info", "Le fichier CSV a été créé/réinitialisé.")

# Fonction qui ajoute du texte au fichier CSV
def ajout():
    try:
        nom = simpledialog.askstring("Nom", "Quel est le nom du produit ?")
        prix = simpledialog.askfloat("Prix", "Quel est le prix du produit (en €) ?")
        quantite = simpledialog.askinteger("Quantité", "Quelle est la quantité reçue ?")

        if os.path.exists(FILENAME):
            df = pd.read_csv(FILENAME)
        else:
            df = pd.DataFrame(columns=["Nom", "Prix", "Quantité"])

        new_row = pd.DataFrame([{"Nom": nom, "Prix": prix, "Quantité": quantite}])

        # Fusion des données
        df = pd.concat([df, new_row], ignore_index=True)

        # Sauvegarde dans le fichier CSV
        df.to_csv(FILENAME, index=False)
        messagebox.showinfo("Info", "Produit ajouté avec succès.")
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")


# Fonction qui supprime une ligne dans le fichier CSV
def delete():
    try:
        df = pd.read_csv(FILENAME)
        produit_a_supprimer = simpledialog.askstring("Supprimer", "Nom du produit à supprimer :")
        
        if produit_a_supprimer not in df["Nom"].values:
            messagebox.showwarning("Info", "Produit introuvable. Aucune ligne supprimée.")
        else:
            df = df[df["Nom"] != produit_a_supprimer]
            df.to_csv(FILENAME, index=False)
            messagebox.showinfo("Info", "Produit supprimé avec succès.")
            
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

# Fonction qui affiche toutes les lignes du fichier CSV
def affiche():
    try:
        df = pd.read_csv(FILENAME)
        if df.empty:
            contenu = "Aucun produit disponible."
        else:
            contenu = df.to_string(index=False)
        messagebox.showinfo("Liste des Produits", contenu)
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

# Fonction qui recherche un produit donné
def recherche():
    produit = simpledialog.askstring("Recherche", "Nom du produit à chercher :")
    type_recherche = simpledialog.askinteger("Type de recherche", "Quel type de recherche voulez-vous effectuer ?\n1. Séquentielle\n2. Dichotomique")

    try:
        df = pd.read_csv(FILENAME)

        # Recherche Séquentielle
        if type_recherche == 1:
            resultats = df[df["Nom"] == produit]
            if not resultats.empty:
                messagebox.showinfo("Résultat", resultats.to_string(index=False))
            else:
                messagebox.showinfo("Résultat", "Aucun produit trouvé avec ce nom.")

        # Recherche Dichotomique
        elif type_recherche == 2:
            df = df.sort_values(by="Nom").reset_index(drop=True)
            left, right = 0, len(df) - 1
            
            trouve = False
            while left <= right:
                pivot = (left + right) // 2
                nom_pivot = df.iloc[pivot]["Nom"]
                if produit < nom_pivot:
                    right = pivot - 1
                elif produit > nom_pivot:
                    left = pivot + 1
                else:
                    messagebox.showinfo("Résultat", df.iloc[[pivot]].to_string(index=False))
                    trouve = True
                    break
            if not trouve:
                messagebox.showinfo("Résultat", "Aucun produit trouvé avec ce nom.")
                
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

# Fonction de tri des produits
def tri_produits():
    try:           
        df = pd.read_csv(FILENAME)

        # Choix du critère de tri
        choix = simpledialog.askinteger("Critère de tri", "Choisissez un critère de tri :\n1 - Par nom\n2 - Par prix\n3 - Par quantité")
        if choix not in [1, 2, 3]:
            messagebox.showerror("Erreur", "Choix invalide.")
            return

        colonnes = {1: "Nom", 2: "Prix", 3: "Quantité"}
        critere = colonnes[choix]

        # Conversion des données en tableau pour les tris manuels
        produits = df.values.tolist()

        # Choix du type de tri
        type_tri = simpledialog.askinteger("Type de tri", "Quel type de tri voulez-vous effectuer ?\n1 - À bulles\n2 - Rapide\n3 - Par sélection")
        
        if type_tri not in [1, 2, 3]:
            messagebox.showerror("Erreur", "Choix invalide.")
            return

        # Tri à bulles
        if type_tri == 1:
            n = len(produits)
            for i in range(n - 1):
                for j in range(n - 1 - i):
                    if produits[j][choix - 1] > produits[j + 1][choix - 1]:
                        produits[j], produits[j + 1] = produits[j + 1], produits[j]

        # Tri rapide
        elif type_tri == 2:
            def quicksort(tableau):
                if len(tableau) <= 1:
                    return tableau
                pivot = tableau[len(tableau) // 2][choix - 1]  
                left = [i for i in tableau if i[choix - 1] < pivot]
                right = [i for i in tableau if i[choix - 1] > pivot]
                centre = [i for i in tableau if i[choix - 1] == pivot]
                return quicksort(left) + centre + quicksort(right)

            produits = quicksort(produits)

        # Tri par sélection
        elif type_tri == 3:
            n = len(produits)
            for i in range(n):
                min_index = i
                for j in range(i + 1, n):
                    if produits[j][choix - 1] < produits[min_index][choix - 1]:
                        min_index = j
                produits[i], produits[min_index] = produits[min_index], produits[i]

        df = pd.DataFrame(produits, columns=["Nom", "Prix", "Quantité"])

        df.to_csv(FILENAME, index=False)

        algorithmes = {1: "tri à bulles", 2: "tri rapide", 3: "tri par sélection"}
        messagebox.showinfo("Info", f"Les produits ont été triés par {critere} avec l'algorithme de {algorithmes[type_tri]}.")

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")


