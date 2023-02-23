"Code Graphique"

#---------- IMPORTATION DES MODULES ----------
from random import sample, randrange, random
from tkinter import Tk, Canvas, Scale, Button, Label, N, ALL

#---------- PARTIE CODE ----------

#Génère une forêt carré aléatoire de densité p contenant n² arbres
def forêt_aléatoire(p, n):
    carré=[(ligne,colonne) for colonne in range(n) for ligne in range(n)]
    nombre_arbres=int(n**2*p)
    arbres=sample(carré,nombre_arbres)
    états=[[0]*n for _ in range(n)]
    for (i,j) in arbres:
        états[i][j]=1
    return états

#Donne les arbres voisins d'un arbre dans les 4 directions G,D,B,H
def voisins(n, i, j):
    return [(a,b) for (a, b) in
            [(i, j+1),(i, j-1), (i-1, j), (i+1,j)]
            if a in range(n) and b in range(n)]

#Permet d'utiliser la probabilité de propagation
def probabilité (prob):
    if random() <= prob:
        return True
    return False

#Remplit la cellule de sa couleur correspondante
def remplir_cellule(états, ligne, colonne):
        A=(unité*colonne, unité*ligne)
        B=(unité*(colonne+1), unité*(ligne+1))
        état=états[ligne][colonne]
        couleur=COULEURS[état]
        cnv.create_rectangle(A, B, fill=couleur, outline='')

#Remplit la grille à l'aide de la fonction précédente
def remplir(états):
    n=len(états)
    for ligne in range(n):
        for colonne in range(n):
            remplir_cellule(états, ligne, colonne)

#Met à jour la grille de la forêt 1=>2=>3
def mise_à_jour_grille(états):
    n=len(états)
    prendre_feu=[]
    for ligne in range(n):
        for colonne in range(n):
            if états[ligne][colonne]==2:
                états[ligne][colonne]=3
                for (i, j) in voisins(n, ligne, colonne):
                    if états[i][j]==1 and probabilité(prob) == True:
                        prendre_feu.append((i, j))
    for (ligne,colonne) in prendre_feu:
        états[ligne][colonne]=2
        
#Remet la forêt à 0
def initialisation():
    global états, compteur, nombre_arbres, en_cours

    p=int(curseur1.get())/100
    en_cours=False
    compteur=0
    label1["text"]="%3s %%" %0
    curseur1["state"]='normal'
    curseur2["state"]='normal'
    états=forêt_aléatoire(p, n)
    nombre_arbres=int(n*n*p)
    cnv.delete(ALL)
    remplir(états)

#Permet de créer la nouvelle forêt de nouvelle densité
def réglage_densité(états, p):
    n=len(états)
    arbres= [(i,j) for i in range(n) for j in range(n) if états[i][j]==1]
    pas_arbre=[(i,j) for i in range(n) for j in range(n) if états[i][j]!=1]
    nouveaux_arbres=int(n*n*p)
    avant=len(arbres)
    delta=abs(nouveaux_arbres-avant)
    if nouveaux_arbres>=avant:
        for (i, j) in sample(pas_arbre, delta):
            états[i][j]=1
    else:
        for (i, j) in sample(arbres, delta):
            états[i][j]=0

#Construit la forêt
def construire_forêt(pourcentage):
    global nombre_arbres

    cnv.delete("all")
    p=float(pourcentage)/100
    nombre_arbres=int(n*n*p)
    réglage_densité(états,p)
    remplir(états)

#Suit la propagation du feu
def propager():
    global compteur, en_cours

    mise_à_jour_grille(états)
    nombre_feux=sum(états[i][j]==2 for i in range(n) for j in range(n))
    compteur+=nombre_feux
    pourcentage = int(compteur/nombre_arbres*100)
    cnv.delete("all")
    remplir(états)
    label1["text"]="%3s %%" %pourcentage
    if nombre_feux==0:
        en_cours=False
        return
    cnv.after(150, propager)

#Met en feu
def feu(événement):
    global en_cours, compteur

    i, j=événement.y//unité, événement.x//unité
    if états[i][j]==1:
        états[i][j]=2
        remplir_cellule(états, i, j)

        compteur+=1
        if not en_cours:
            en_cours=True
            curseur1["state"]='disabled'
            curseur2["state"]='disabled'
            propager()

#Met en feu une partie de la gauche de la forêt
def allumer_feu():
    global en_cours, compteur
    i=n//4
    for a in range(n//2):
        états[i+a][1]=2

    compteur+=1
    if not en_cours:
        en_cours=True
        curseur1["state"]='disabled'
        curseur2["state"]='disabled'
        propager()

#Met à jour la probabilité de transmission
def probabilité_curseur(prob_curseur):
    global prob
    prob=float(prob_curseur)


#---------- PARTIE REGLAGE ----------
n=75 #Taille de la forêt (un côté)
unité=10 #Dimension graphique d'un carré sur l'écran
COULEURS=["ivory", "lime green", "red", "gray75"] #Couleurs de la modélisation


#---------- PARTIE GRAPHIQUE ----------

# Fenêtre et canevas
root = Tk()
cnv = Canvas(root, width=unité*n-2, height=unité*n-2, background="ivory")
cnv.grid(row=0, column=0, rowspan=4)

#Boutons
btn1=Button(root,text="Nouveau",  font='Arial 15 bold',\
            command=initialisation, width=8)
btn1.grid(row=0, column=2, sticky=N)

bouton2=Button(root,text="Mettre en feu",  font='Arial 15 bold',\
               command=allumer_feu, width=12)
bouton2.grid(row=0, column=1, sticky=N)

#Labels
label1=Label(root,text="%3s %%" %0,  font='Arial 15 bold', bg='red', width=5)
label1.grid(row=2, column=1, sticky=N)

label2=Label(root,text="% de Forêt brulée",  font='Arial 15 bold', width=15)
label2.grid(row=1, column=1, sticky=N)

# Mettre le feu avec un clic
cnv.bind("<Button-1>", feu)

#Curseurs
curseur1 = Scale(root, orient = "vertical", command=construire_forêt, from_=100,
      to=0, length=200, tickinterval= 25,  label='Densité (%)')
curseur1.set(50)
curseur1.grid(row=3, column=1)

curseur2 = Scale(root, orient='vertical', command=probabilité_curseur,\
                 from_=1, to=0,
      resolution=0.01, length=200, tickinterval= 0.25,
      label='Probabilité de Transmission')
curseur2.set(0.5)
curseur2.grid(row=3, column=2)

initialisation()

root.mainloop()