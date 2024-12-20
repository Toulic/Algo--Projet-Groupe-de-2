import csv
import tkinter as tk
from tkinter import messagebox, simpledialog
import hashlib
import os
from random import randint

# Fonction qui créer un mot de passe sécurisé aléatoire
def mdp_suggest():
    with open('Data/mdp_suggest.csv', 'r', newline='') as csvfile:
        texte = list(csv.reader(csvfile))
    
    #On fournira des mots de passe de 10 caractères
    mdp_potentiel = ""
    for i in range(10):
        index_type_ajout = randint(0,2)
        ajout = texte[1][index_type_ajout][randint(0, len(texte[1][index_type_ajout]) - 1)]
        mdp_potentiel += ajout
    
    return mdp_potentiel


