

#Parsing du fichier pour isoler les stations et les liens et obtenir deux listes propres
def file_parser(file,arg):
    with open(file, "r") as fd:
        maliste = fd.readlines()
        stations = []
        liens = []
        for val in maliste:
            if val[0] == 'V':
                stations.append(val.strip("\n",).split(" ",2))
            elif val[0] == 'E':
                liens.append(val.strip("\n").split(" "))
    if arg == "stations":
        return stations
    elif arg == "liens":
        return liens

###############################################################################
#Vérification de la connexité
###############################################################################

#Génèration une matrice de taille n*n
def generer_matrice(n):
    matrice = []
    for i in range(n):
        matrice.append([])
        for j in range(n):
            matrice[i].append(0)
    return matrice


#Remplissage de la matrice
def fill_matrice(matrice,liens):
    for val in liens:
        matrice[int(val[1])][int(val[2])] = 1
        matrice[int(val[2])][int(val[1])] = 1


#Vérification si la matrice est connexe
def est_connexe(matrice):
    n = len(matrice)
    liste = [None]*n
    for i in range(n):
        for j in range(n):
            if matrice[i][j] == 1 or matrice[j][i] == 1:
                liste[i] = True
                break
            else :
                liste[i] = False 
    if all(liste):
        print("Le graphe est connexe.")
    else:
        print("Le graphe n'est pas connexe.")


#Main pour tester les fonctions
if __name__ == "__main__":
    path = "metro.txt"
    V = file_parser(path,"stations")
    E = file_parser(path,"liens")
    matrice = generer_matrice(len(V))
    fill_matrice(matrice,E)
    est_connexe(matrice)
