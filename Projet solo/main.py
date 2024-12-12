import csv
from operation_sur_fichier import *

while True:
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

