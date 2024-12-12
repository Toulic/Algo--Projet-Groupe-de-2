import csv
import operation_sur_fichier

def ajout_user():
    with open('users.csv', 'a', newline='') as csvfile:
        fieldname = ['Username', 'mdp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldname)

        username, mdp = input("Votre nom d'utilisateur"), input("Votre mot de passe")
        writer.writerow({'Username': username, 'mdp': mdp})


import csv

def delete_user():
    with open("users.csv", 'r', newline='') as csvfile:
        texte = list(csv.reader(csvfile)) 

    ligne_delete = input("Quel utilisateur voulez-vous supprimer (nom) : ").strip()

    new_texte = [ligne for ligne in texte if ligne[0].strip() != ligne_delete]


    with open("users.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(new_texte) 

    print(f"L'utilisateur '{ligne_delete}' a été supprimé.")

def modif_mdp():
    with open("users.csv", 'r', newline='') as csvfile:
        texte = list(csv.reader(csvfile)) 

    user = input("Qui êtes-vous ?").strip()
    new_mdp = input("Quel est votre nouveau mot de passe ?")

    new_texte = []
    for ligne in texte:
        if ligne[0].strip() != user:
            new_texte.append(ligne)
        else:
            new_texte.append([f"{user}, {new_mdp}"])
    
    print(new_texte)
    
    with open("users.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(new_texte) 

    print(f"Le mot de passe de l'utilisateur '{user}' a été modifié.")




def choix_user(choix):
    if choix == 1:
        ajout_user()
    elif choix == 2:
        delete_user()
    elif choix == 3:
        modif_mdp()
    else:
        print("Erreur, le choix entré ne correspond à rien")
