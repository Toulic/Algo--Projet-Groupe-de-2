import tkinter as tk
from tkinter import messagebox, simpledialog
from gestion_produits import * 
from gestion_users import *
import datetime as dt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import matplotlib.pyplot as plt

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

# Fonction qui envoie un mail à l'utilisateur quand son mot de passe est compromis
def send_email(email_address, username):
    sender_email = "algooprojet@gmail.com"  
    sender_password = "d d k j c b n f y g c h b y k v"  
    subject = "Alerte : Mot de passe compromis"

    message = f"""
    Bonjour {username},

    Nous avons détecté que votre mot de passe a été compromis dans une violation de données. 
    Nous vous recommandons vivement de le changer immédiatement.

    Merci de votre attention,
    Équipe de Sécurité
    """

    try:
        # Créer le message email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email_address
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Connexion au serveur SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email_address, msg.as_string())
        messagebox.showinfo("Email envoyé",f"Email envoyé à {email_address} avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur",f"Erreur lors de l'envoi de l'email : {e}")

# Fonction qui prépare la connexion, et la rejette si les conditions ne sont pas remplies
def connexion():
    try:
        with open('Data/users.csv', 'r', newline='', encoding='utf-8') as csvfile:
            texte = list(csv.reader(csvfile))
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Le fichier users.csv est introuvable.")
        return

    try:
        historique_fichier = 'Data/historique.csv'
        fieldnames = ['date', 'user', 'mdp', 'success', 'compromis']
        with open(historique_fichier, 'a', newline='', encoding='utf-8') as histofile:
            writer = csv.DictWriter(histofile, fieldnames=fieldnames)

            login = simpledialog.askstring("Login", "Quel est votre identifiant ?")
            mdp = simpledialog.askstring("Mot de passe", "Quel est votre mot de passe ?")

            for ligne in texte:
                compromis = 0
                if ligne[0].strip() == login: 
                    hash_mdp = hashlib.sha256((mdp + ligne[2]).encode('utf-8')).hexdigest().strip()
                    if ligne[1].strip() != hash_mdp:  
                        messagebox.showwarning("Erreur", "L'identifiant ou le mot de passe sont incorrects. \nÊtes-vous bien inscrit ?")
                        writer.writerow({'date': dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'user': login, 'mdp': hash_mdp, 'success': "False", 'compromis': compromis})
                        return
                    else:
                        pwned_bool, compromis =  mdp_pwned(mdp) 
                        if pwned_bool:  
                            messagebox.showinfo("Mot de passe compromis", "Votre mot de passe est compromis de façon internationale, vous devriez le changer")
                            email_address = ligne[4].strip()  
                            send_email(email_address, login) 
                        writer.writerow({'date': dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'user': login, 'mdp': hash_mdp, 'success': "True", 'compromis': compromis})
                        gestion(login) 
                        return
    
            messagebox.showwarning("Erreur", "L'identifiant ou le mot de passe sont incorrects. \nÊtes-vous bien inscrit ?")
            writer.writerow({'date': dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'user': login, 'mdp': hashlib.sha256((mdp).encode('utf-8')).hexdigest().strip(), 'success': "False", 'compromis': compromis})
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

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
