import tkinter as tk
from tkinter import messagebox, simpledialog


# Fonction qui crée le fichier
def craft_fichier():
    fichier = open("fichier.txt", 'w')
    fichier.close()
    messagebox.showinfo("Info", "Le fichier a été créé/réinitialisé.")

# Fonction qui ajoute du texte au fichier
def ajout():
    try:
        with open("fichier.txt", 'a') as fichier:
            nom = simpledialog.askstring("Nom", "Quel est le nom du produit ?")
            prix = simpledialog.askfloat("Prix", "Quel est le prix du produit (en €) ?")
            quantite = simpledialog.askinteger("Quantité", "Quelle est la quantité reçue ?")
            fichier.write(f"{nom}, {prix}, {quantite}\n")
        messagebox.showinfo("Info", "Produit ajouté avec succès.")
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Fichier inexistant. Veuillez le créer d'abord.")

#Fonction qui supprime une ligne du fichier 
def delete():
    try:
        with open("fichier.txt", 'r') as fichier:
            texte = fichier.readlines()

        ligne_delete = simpledialog.askstring("Supprimer", "Nom du produit à supprimer :")                                                          
        new_texte = [ligne for ligne in texte if ligne.split(",")[0].strip() != ligne_delete.strip()]

        if len(new_texte) == len(texte):
            messagebox.showwarning("Info", "Produit introuvable. Aucune ligne supprimée.")
        else:
            with open("fichier.txt", 'w') as fichier:
                fichier.writelines(new_texte)
            messagebox.showinfo("Info", "Produit supprimé avec succès.")
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Fichier inexistant. Veuillez le créer d'abord.")


# Fonction qui affiche toutes les lignes
def affiche():
    try:
        with open("fichier.txt", 'r') as fichier:
            contenu = fichier.read()
        if not contenu.strip():
            contenu = "Aucun produit disponible."
        messagebox.showinfo("Liste des Produits", contenu)
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Fichier inexistant. Veuillez le créer d'abord.")

# Fonction qui recherche de deux façons différentes possibles un produit donnée dans le fichier
def recherche():
    produit = simpledialog.askstring("Recherche", "Nom du produit à chercher :")
    type_recherche = simpledialog.askinteger(
        "Type de recherche",
        "Quel type de recherche voulez-vous effectuer ?\n1. Séquentielle\n2. Dichotomique",
    )

    # Validation de l'entrée
    if type_recherche not in [1, 2]:
        messagebox.showerror("Erreur", "Choix invalide. Veuillez choisir 1 ou 2.")
        return

    try:
        with open("fichier.txt", 'r') as fichier:
            produits = fichier.readlines()

        # Recherche Séquentielle
        if type_recherche == 1:
            resultats = [ligne.strip() for ligne in produits if ligne.split(",")[0].strip() == produit.strip()]
            if resultats:
                messagebox.showinfo("Résultat", f"Produit trouvé : {resultats[0]}")
            else:
                messagebox.showinfo("Résultat", "Aucun produit trouvé avec ce nom.")
            return

        # Recherche Dichotomique
        elif type_recherche == 2:
            produits_triees = sorted(produits, key=lambda x: x.split(",")[0].strip())

            left = 0
            right = len(produits_triees) - 1
            trouve = False

            while left <= right:
                pivot = (left + right) // 2
                nom_pivot = produits_triees[pivot].split(",")[0].strip()

                if produit.strip() < nom_pivot:
                    right = pivot - 1
                elif produit.strip() > nom_pivot:
                    left = pivot + 1
                else:
                    messagebox.showinfo("Résultat", f"Produit trouvé : {produits_triees[pivot].strip()}")
                    trouve = True
                    break

            if not trouve:
                messagebox.showinfo("Résultat", "Aucun produit trouvé avec ce nom.")

    except FileNotFoundError:
        messagebox.showerror("Erreur", "Fichier inexistant. Veuillez le créer d'abord.")

# Fonction de tri à bulle des produits
def tri_produits():
    try:
        with open("fichier.txt", "r") as fichier:
            texte = fichier.readlines()

        produits = []
        for ligne in texte:
            nom, prix, quantite = ligne.strip().split(", ")
            produits.append((nom, float(prix), int(quantite)))

        choix = simpledialog.askinteger("Critère de tri","Choisissez un critère de tri :\n1 - Par nom\n2 - Par prix\n3 - Par quantité")
        
        if choix not in [1, 2, 3]:
            messagebox.showerror("Erreur", "Choix invalide.")
            return

        critere = choix - 1
        type_tri = simpledialog.askinteger("Type de tri", "Quel type de tri voulez-vous effectuer ?\n1 - À bulles\n2 - Rapide\n3 - Par sélection")
        if type_tri not in [1, 2, 3]:
            messagebox.showerror("Erreur", "Choix invalide.")
            return

        # Tri à bulles
        if type_tri == 1:
            n = len(produits)
            for i in range(n - 1, 0, -1):
                tableau_trie = True
                for j in range(i):
                    if produits[j][critere] > produits[j + 1][critere]:
                        produits[j], produits[j + 1] = produits[j + 1], produits[j]
                        tableau_trie = False
                if tableau_trie:
                    break

        # Tri rapide
        elif type_tri == 2:
            def quicksort(tableau):
                if len(tableau) <= 1:
                    return tableau
                pivot = tableau[len(tableau) // 2][critere]
                left = [i for i in tableau if i[critere] < pivot]
                right = [i for i in tableau if i[critere] > pivot]
                centre = [i for i in tableau if i[critere] == pivot]
                return quicksort(left) + centre + quicksort(right)

            produits = quicksort(produits)

        # Tri par sélection
        elif type_tri == 3:
            n = len(produits)
            for i in range(n):
                min_index = i
                for j in range(i + 1, n):
                    if produits[j][critere] < produits[min_index][critere]:
                        min_index = j
                produits[i], produits[min_index] = produits[min_index], produits[i]

        # Écrire le fichier trié
        with open("fichier.txt", "w") as fichier:
            for produit in produits:
                fichier.write(f"{produit[0]}, {produit[1]}, {produit[2]}\n")

        criteres = {0: "nom", 1: "prix", 2: "quantité"}
        algorithmes = {1: "tri à bulles", 2: "tri rapide", 3: "tri par sélection"}
        messagebox.showinfo("Info", f"Les produits ont été triés par {criteres[critere]} avec l'algorithme de {algorithmes[type_tri]}.")

    except FileNotFoundError:
        messagebox.showerror("Erreur", "Fichier inexistant. Veuillez le créer d'abord.")
