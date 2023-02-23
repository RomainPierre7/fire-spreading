"Code Statistique"

#---------- IMPORTATION DES MODULES ----------
from random import sample, random
import matplotlib.pyplot as plt
import time

#---------- PARTIE CODE ----------

#Génère une forêt carré aléatoire de densité p contenant n² arbres
def forêt_aléatoire(p, n):
    carré=[(ligne,colonne) for colonne in range(n) for ligne in range(n)]
    nombre_arbres=int(n**2*p)
    arbres=sample(carré,nombre_arbres)
    forêt=[[0]*n for _ in range(n)]
    for (i,j) in arbres:
        forêt[i][j]=1
    return forêt

#Donne les arbres voisins d'un arbre dans les 4 directions G,D,B,H
def voisins(n, i, j):
    return [(a,b) for (a, b) in
            [(i, j+1),(i, j-1), (i-1, j), (i+1,j)]
            if a in range(n) and b in range(n)]

#Permet d'utiliser la probabilité de transmission
def probabilité (prob):
    if random() <= prob:
        return True
    return False

#Met à jour la grille de la forêt 1=>2=>3
def mise_à_jour_grille(forêt, probabilité_propagation):
    prendre_feu=[]
    for ligne in range(n):
        for colonne in range(n):
            if forêt[ligne][colonne]==2:
                forêt[ligne][colonne]=3
                for (i, j) in voisins(n, ligne, colonne):
                    if forêt[i][j]==1 and probabilité(probabilité_propagation)\
                        == True:
                        prendre_feu.append((i, j))
    for (ligne,colonne) in prendre_feu:
        forêt[ligne][colonne]=2
    return forêt


#Met en feu lune partie de la gauche de la forêt
def allumer_feu(forêt):
    i=n//4
    for a in range(n//2):
        forêt[i+a][1]=2
    return forêt
        
#Indique si il y a percolation i.e. amas infini
def percolation (forêt):
    for i in range (n):
        if forêt[i][n-1]==3:
            return True
    return False

#Simule un feu jusqu'à extinction
def simulation(densité, probabilité_propagation):
    forêt = forêt_aléatoire(densité, n)
    forêt = allumer_feu(forêt)
    nombre_feux=sum(forêt[i][j]==2 for i in range(n) for j in range(n))
    while nombre_feux !=0 :
        forêt = mise_à_jour_grille(forêt,probabilité_propagation)
        nombre_feux=sum(forêt[i][j]==2 for i in range(n) for j in range(n))
    if percolation(forêt)==True:
        return 1
    return 0

#---------- PARTIE ACQUISITION ----------
def acquisition_probabilité_propagation(densité):
    début=time.time()
    L=[]
    P=[]
    probabilité_propagation=0
    while probabilité_propagation<=1:
        P.append(probabilité_propagation)
        s=0
        for _ in range(100):
            s+=simulation(densité, probabilité_propagation)
        print((int(probabilité_propagation*100)),"/100")
        L.append(s)
        probabilité_propagation+=0.01
    fin=time.time()
    print("Temps de calcul =",fin-début)
    plt.figure(figsize=(16,9))
    plt.plot(P,L, color = 'red', linestyle = '--' , linewidth = 2)
    plt.xlabel("Probabilité de propagation")
    plt.ylabel("% de percolation")
    plt.grid()
    plt.title("Etude sur le paramètre de probabilité de transmission du feu")
    
def acquisition_probabilité_propagation_centrée():
    début=time.time()
    L=[]
    P=[]
    probabilité_propagation=0.4
    while probabilité_propagation<=0.6:
        P.append(probabilité_propagation)
        s=0
        for _ in range(100):
            s+=simulation(1, probabilité_propagation)
        print((int(probabilité_propagation*100)-40),"/20")
        L.append(s)
        probabilité_propagation+=0.01
    fin=time.time()
    print("Temps de calcul =",fin-début)
    plt.figure(figsize=(16,9))
    plt.plot(P,L, color = 'red', linestyle = '--' , linewidth = 2)
    plt.xlabel("Probabilité de propagation")
    plt.ylabel("% de percolation")
    plt.grid()
    plt.title("Etude sur le paramètre de probabilité de transmission du feu")

        
def acquisition_densité(probabilité):
    début=time.time()
    L=[]
    D=[]
    densité=0
    while densité<=1:
        D.append(densité)
        s=0
        for _ in range(100):
            s+=simulation(densité, probabilité)
        print((int(densité*100)),"/100")
        L.append(s)
        densité+=0.01
    fin=time.time()
    print("Temps de calcul =",fin-début)
    plt.figure(figsize=(16,9))
    plt.plot(D,L, color = 'red', linestyle = '--' , linewidth = 2)
    plt.xlabel("Densité", fontsize = 15)
    plt.ylabel("% de percolation", fontsize = 15)
    plt.grid()
    plt.title("Etude sur le paramètre de densité de la forêt", fontsize = 25)
    
def acquisition_densité_centrée():
    début=time.time()
    L=[]
    D=[]
    densité=0.5
    while densité<=0.7:
        D.append(densité)
        s=0
        for _ in range(100):
            s+=simulation(densité, 1)
        print((int(densité*100)-50),"/20")
        L.append(s)
        densité+=0.01
    fin=time.time()
    print("Temps de calcul =",fin-début)
    plt.figure(figsize=(16,9))
    plt.plot(D,L, color = 'red', linestyle = '--' , linewidth = 2)
    plt.xlabel("Densité", fontsize = 15)
    plt.ylabel("% de percolation", fontsize = 15)
    plt.grid()
    plt.title("Etude sur le paramètre de densité de la forêt", fontsize = 25)


def acquisition_densité_précision(epsilon):
    début=time.time()
    densité_min=0.59
    densité_max=0.60
    densité_pivot=(densité_max+densité_min)/2
    while densité_max-densité_min > epsilon:
        densité_pivot=(densité_max+densité_min)/2
        print(densité_pivot)
        s=0
        for _ in range(100):
            s+=simulation(densité_pivot, 1)
        if s>50:
            densité_max=densité_pivot
        elif s==50:
            fin=time.time()
            print("Temps de calcul =",fin-début)
            return densité_pivot
        else:
            densité_min=densité_pivot
    fin=time.time()
    print("Temps de calcul =",fin-début)
    return densité_pivot
 
#---------- PARTIE REGLAGE ----------
n=100 #Taille de la forêt (un côté)
COULEURS=["ivory", "lime green", "red", "gray75"] #Couleurs de la modélisation

#---------- PARTIE EXECUTION ----------

acquisition_probabilité_propagation(1)