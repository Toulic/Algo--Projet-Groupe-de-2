# Fonction qui crée le fichier
def craft_fichier():
    fichier = open("fichier.txt", 'w')
    fichier.close()

# Fonction qui ajoute du texte au fichier
def ajout():
    with open("fichier.txt", 'a') as fichier:
        nom = input("Quel est le nom du produit ? : ")
        prix = float(input("Quel est le prix du produit (en €)? : "))
        quantite = int(input("Quel est la quantité reçue de ce produit ? (en unité arbitraire) : "))
        fichier.write(f"{nom}, {prix}, {quantite}")
        fichier.write("\n")

#Fonction qui supprime une ligne du fichier à faire / adapter
def delete():
    with open("fichier.txt", 'r') as fichier:
        texte = fichier.readlines()
        ligne_delete = input("Ce que vous voulez supprimer : ")
        new_texte = [ligne for ligne in texte if ligne.strip() != ligne_delete.strip().split(", ")[0]]

    with open("fichier.txt", "w") as fichier:
        fichier.writelines(new_texte)


# Fonction qui affiche toutes les lignes
def affiche():
    print("### Menu des Produits ###\n")

    with open("fichier.txt", 'r') as fichier:
        texte = fichier.read()
        print(texte)

# Fonction qui recherche de deux façons différentes possibles un produit donnée dans le fichier
def recherche(produit):
    type_recherche = int(input("Quel type de recherche voulez-vous effectuer ? \n1. Séquentielle\n2. Dichotomique\n"))

    #Pour obliger à mettre 1 ou 2 :
    while (type_recherche < 1) or (type_recherche > 2):
        type_recherche = int(input("Les autres chiffres ne sont pas attribués.\nQuel type de recherche voulez-vous effectuer ? \n1. Séquentielle\n2. Dichotomique\n"))

    #La recherche séquentielle
    if type_recherche == 1:
        with open("fichier.txt", 'r') as fichier:
            texte = fichier.readlines()
        affiche = [ligne.strip() for ligne in texte if ligne.strip().split(", ")[0] == produit]

        if affiche:
            print(f"Produit trouvé : {affiche[0]}")
        else:
            print("Aucun produit trouvé avec ce nom.")

    # La recherche Dichotomique
    elif type_recherche == 2:
        with open("fichier.txt", 'r') as fichier:
            sauvegarde = fichier.readlines()

        tri_pour_dicho()

        with open("fichier.txt", 'r') as fichier:
            produits = fichier.readlines()
        left = 0
        right = len(produits)-1
        while left <= right:
            pivot = (left+right)//2
            if produit < produits[pivot].split(",")[0]:
                right = pivot -1
            elif produit > produits[pivot].split(",")[0]:
                left = pivot +1
            else:
                print("Produit trouvé : ", produits[pivot])
                break
        with open("fichier.txt", 'w') as fichier:
            fichier.writelines(sauvegarde)
    else:
        print("Cela ne correspond à rien de proposer\n")

# Fonction de tri à bulle des produits mais pour la recherche dichotomique (i.e. sans affichage que ça a été trié) car elle a été faite avant
def tri_pour_dicho():
    with open("fichier.txt", "r") as fichier:
        produits = fichier.readlines()

    produits = []
    for ligne in produits:
        nom, prix, quantite = ligne.strip().split(", ")
        produits.append((nom, float(prix), int(quantite)))

    n = len(produits)
    for i in range(n - 1, 0, -1):
        tableau_trie = True
        for j in range(i):
            if produits[j][0] > produits[j + 1][0]: 
                produits[j], produits[j + 1] = produits[j + 1], produits[j]
                tableau_trie = False
        if tableau_trie:
            break

    with open("fichier.txt", "w") as fichier:
        for produit in produits:
            fichier.write(f"{produit[0]}, {produit[1]}, {produit[2]}\n")




# Fonction de tri à bulle des produits
def tri_produits():
    with open("fichier.txt", "r") as fichier:
        texte = fichier.readlines()

    produits = []
    for ligne in texte:
        nom, prix, quantite = ligne.strip().split(", ")
        produits.append((nom, float(prix), int(quantite)))

    print("Choisissez un critère de tri :")
    print("1 - Par nom")
    print("2 - Par prix")
    print("3 - Par quantité")
    choix = input("Votre choix (1, 2 ou 3) : ")

    if choix == "1":
        critere = 0  
    elif choix == "2":
        critere = 1 
    elif choix == "3":
        critere = 2  
    else:
        print("Choix invalide. Tri par défaut (nom).")
        critere = 0

    type_tri = int(input("Quel type de tri voulez-vous effectuer ? \n1. À bulles\n2. Rapide\n"))
    
    #Pour obliger à mettre 1 ou 2 :
    while (type_tri < 1) or (type_tri > 2):
        type_tri = int(input("Les autres chiffres ne sont pas attribués.\nQuel type de tri voulez-vous effectuer ? \n1. À bulles\n2. Rapide\n"))

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

        with open("fichier.txt", "w") as fichier:
            for produit in produits:
                fichier.write(f"{produit[0]}, {produit[1]}, {produit[2]}\n")

        criteres = {0: "nom", 1: "prix", 2: "quantité"}
        print(f"Les produits ont été triés par {criteres[critere]} avec l'algorithme de tri à bulles.")

    #Tri rapide
    elif type_tri == 2:
        # Fonction du tri rapide qui sera appelé en récursif
        def quicksort(tableau):
            if len(tableau) <= 1:
                return tableau
            pivot = tableau[len(tableau) // 2][critere] 
            left = [i for i in tableau if i[critere] < pivot]
            right = [i for i in tableau if i[critere] > pivot]
            centre = [i for i in tableau if i[critere] == pivot]
            return quicksort(left) + centre + quicksort(right)

        produits_triees = quicksort(produits)

        with open("fichier.txt", "w") as fichier:
            for produit in produits_triees:
                fichier.write(f"{produit[0]}, {produit[1]}, {produit[2]}\n")

        criteres = {0: "nom", 1: "prix", 2: "quantité"}
        print(f"\nLes produits ont été triés par {criteres[critere]} avec l'algorithme de tri rapide.")


# Fonction qui appelle les autres fonctions
def choix_action(choix):
    if choix == 0:
        exit()
    elif choix == 1:
        craft_fichier()
    elif choix == 2:
        ajout()
    elif choix == 3:
        delete()
    elif choix == 4:
        affiche()
    elif choix == 5:
        produit = input("Quel produit voulez-vous chercher (son nom) ? ")
        recherche(produit)
    elif choix == 6:
        tri_produits()
    else:
        print("Erreur, le choix entré ne correspond à rien")

