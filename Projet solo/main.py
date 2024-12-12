import csv
from users import *
from operation_sur_fichier import *

with open('users.csv', 'w', newline='') as csvfile:
    fieldname = ['Username', 'mdp']
    writer = csv.DictWriter(csvfile, fieldnames=fieldname)
    writer.writeheader()

while True:
    print("\n-------------------------------------------------")
    print("### MENU DE CONNEXION ###\n")
    print("T qui ?")
    print("1. Ajouter un utilisateur")
    print("2. Supprimer un utilisateur")
    print("3. Modifier un mot de passe")
    choix = int(input("Insèrez le choix (en chiffre) : "))
    choix_user(choix)

    test = True

    if not(test):
        print("\n-------------------------------------------------")
        print("### MENU DES OPTIONS ###\n")
        print("1. Créer/Réinnitialiser le fichier des produits")
        print("2. Ajouter un produit")
        print("3. Supprimer un produit")
        print("4. Afficher la liste des produits")
        print("5. Rechercher un produit")
        print("6. Trier les produits")
        print("\n0. === QUITTER ===")
        print("-------------------------------------------------")
        choix = int(input("Insèrez le choix (en chiffre) : "))
        choix_action(choix)

