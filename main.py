"""
On décompose le fichier metro.txt de manière à ce que dans trajet.txt, il n'y ait que les
aretes du graphe
"""

nb_ligne = 473 # nombre de ligne du fichier trajet.txt

def dicMetro():
    """
    Cette fonction a pour but de créer un dictionnaire de la forme suivante:
    {station de départ:[[station d'arrivé],[temps de trajet]]}
    exemple : {0: [[238, 159], [41, 46]]}
    Comment lire ce dico : depuis la station 1, on peut aller à la station 238 en 41 secondes
    """
    listeArete = [] # Liste de tuple qui contiendra ex: (E, 299, 304, 48)
    with open('trajet.txt', 'r') as fd:
        file = fd.read().splitlines()
        for elt in file:
            listeArete.append(tuple(elt.split(' ')))
    
    dico = {} # clé : station de départ

    for i in range(376): # Nombre de stations repertoriées dans le fichier metro.txt (compte les doublons)
        for elt in listeArete:
            if i == int(elt[1]):
                dico[i] = [[],[]]
    for elt in listeArete: 
            dico[int(elt[1])][0].append(int(elt[2]))
            dico[int(elt[1])][1].append(int(elt[3]))
    return dico

def connexite(dico,listeConnexe,):
    for i in range(376):
        pass

def nombreArret(): # Y'a 296 arrets différents. Je suis pas sûr que ça serve mais c'est la oklm
    """
    Pour determiner le nombre d'arret distinct dans le fichier arret.txt 
    """
    with open('arret.txt','r') as fd:
        hess = []
        file = fd.read().splitlines()
        for elt in file:
            tup = elt[7:]
            if tup not in hess:
                hess.append(tup)
    return len(hess)

#J'ai voulu tester de faire une matrice mais elle est beaucoup trop grosse et donc trop complexe de travailler avec
#En plus en terme de complexité ça pue de fou donc on va éviter !
"""def matriceAdjacence(liste_aretes): 
    maMatrice = [[0 for _ in range(376)] for _ in range(376)]

    for elt in liste_aretes:
        print(int(elt[1]),int(elt[2]))
        maMatrice[int(elt[1])][int(elt[2])] = 1
    return maMatrice"""

if __name__ == "__main__":

    nbArret = nombreArret()
    liste_arete = dicMetro() 
    print(liste_arete)