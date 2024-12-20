import tkinter as tk
from tkinter import messagebox, simpledialog
from gestion_produits import * 
from gestion_users import *

# Fonction qui prépare la connexion de l'admin très sécurisé n'est-ce pas
def connexion_admin():
    with open('Data/admin.csv', 'r', newline='') as csvfile:
        texte = list(csv.reader(csvfile))

    login = simpledialog.askstring("Login", "Donne le login admin ?")
    mdp = simpledialog.askstring("Mot de passe", "Donne le mot de passe admin ?")

    for ligne in texte:
        if ligne[0].strip() == login:
            if ligne[1].strip() != hashlib.sha256(mdp.encode('utf-8')).hexdigest().strip():
                messagebox.showwarning("Erreur", "L'identifiant ou le mot de passe sont incorrects. \nSors de là")
                return
            else:
                admin()
                return

    messagebox.showwarning("Erreur", "L'identifiant ou le mot de passe sont incorrects. \nSors de là")

# Fonction qui ouvre une fenetre de gestion utilisateur pour l'admin
def admin():
    fenetre_utilisateur = tk.Toplevel()
    fenetre_utilisateur.title("Fenêtre de l'admin")
    fenetre_utilisateur.geometry("500x250")
    tk.Label(fenetre_utilisateur, text="### MENU ADMINISTRATEUR ###").pack(pady=20)
    tk.Button(fenetre_utilisateur, text="1. Ajouter un utilisateur", bg='#7ACD3D', command=ajout_user, width=60).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="2. Supprimer un utilisateur", bg='#E36044', command=delete_user, width=60).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="Fermer", bg='yellow', command=fenetre_utilisateur.destroy).pack(pady=30)


# Fonction qui fait la fenêtre utilisateur d'inscription
def inscription():
    fenetre_utilisateur = tk.Toplevel()
    fenetre_utilisateur.title("Fenêtre d'inscription")
    fenetre_utilisateur.geometry("500x250")
    tk.Label(fenetre_utilisateur, text="### MENU D'INSCRIPTION ###").pack(pady=20)
    tk.Label(fenetre_utilisateur, text="Voici le menu d'inscription.\nNous considérons que vous acceptez les conditions d'utilisations fictives\ncar je voulais écrire un bloc de texte ici mais j'ai pas d'idées.").pack(pady=5)
    tk.Button(fenetre_utilisateur, text="1. Ajouter un utilisateur", bg='#7ACD3D', command=ajout_user, width=60).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="Fermer", bg='yellow', command=fenetre_utilisateur.destroy).pack(pady=30)


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
        plt.title(f"Les produits de {user} par {critere}")

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
            if ligne[1].strip() != hashlib.sha256((mdp + ligne[2]).encode('utf-8')).hexdigest().strip():
                messagebox.showwarning("Erreur", "L'identifiant ou le mot de passe sont incorrects. \nÊtes-vous bien inscrit ?")
                return
            else:
                if mdp_pwned(mdp):
                   mdp = messagebox.showinfo("Mot de passe compromis", "Votre mot de passe est compromis de façon internationale, vous devriez le changer")
                gestion(login)
                return

    messagebox.showwarning("Erreur", "L'identifiant ou le mot de passe sont incorrects. \nÊtes-vous bien inscrit ?")

# Fonction de gestion des produits pour un utilisateur donné
def gestion(user):
    if not os.path.exists(f"Data/produits_{user}.csv"):
        craft_fichier(user)
    fenetre_utilisateur = tk.Toplevel()
    fenetre_utilisateur.title("Fenêtre de gestion")
    fenetre_utilisateur.geometry("800x600")
    tk.Label(fenetre_utilisateur, text=f"Bonjour {user}", font=("Arial", 20)).pack(pady=20)
    tk.Button(fenetre_utilisateur, text="1. Réinitialiser le fichier des produits", bg='lightgrey', command=lambda: craft_fichier(user), width=80).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="2. Ajouter un produit", bg='grey', command=lambda: ajout(user), width=80).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="3. Supprimer un produit", bg='grey', command=lambda: delete(user), width=80).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="4. Afficher la liste des produits", bg='grey', command=lambda: affiche(user), width=80).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="5. Rechercher un produit", bg='grey', command=lambda: recherche(user), width=80).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="6. Trier les produits", bg='grey', command=lambda: tri_produits(user), width=80).pack(pady=10)
    tk.Button(fenetre_utilisateur, text="7. Afficher un graphe des produits", bg='grey', command=lambda: graphic(user), width=80).pack(pady=10)    
    tk.Button(fenetre_utilisateur, text="8. Modifier votre mot de passe", bg='darkgrey', command=lambda: modif_mdp(user), width=80).pack(pady=10)        
    tk.Button(fenetre_utilisateur, text="Fermer", bg='yellow', command=fenetre_utilisateur.destroy).pack(pady=10)
