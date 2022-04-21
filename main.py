#Parsing du fichier pour isoler les stations et les liens et obtenir deux listes propres

def lecture_fichier(file):
    """Lis le fichier dont le chemin a été mis en paramètre"""
    with open(file, "r") as fic:
        lecture = fic.read().split("\n")
    return lecture


def file_parser(file, arg):
    lecture = lecture_fichier(file)
    stations = []
    liens = []
    for ligne in lecture:
        premiere_lettre = ligne[0]
        if premiere_lettre == 'V':
            ligne_metro = ligne[7:9]
            if ligne_metro == '13' or ligne_metro == '07':
                stations.append(ligne.split(" ",6))
            else:
                stations.append(ligne.split(" ",5))
        elif premiere_lettre == 'E':
            liens.append(ligne.split(" "))
    if arg == "stations":
        return stations
    elif arg == "liens":
        return liens

###############################################################################
#Vérification de la connexité
###############################################################################

#Génèration une matrice de taille n*n

def generer_matrice(n):
    return [[0]*n for _ in range(n)]


#Remplissage de la matrice
def fill_matrice(matrice,liens):
    for ligne in liens:
        sommet_depart = int(ligne[1])
        sommet_arrive = int(ligne[2])
        temps = int(ligne[-1])
        matrice[sommet_depart][sommet_arrive] = temps
        matrice[sommet_arrive][sommet_depart] = temps


#Affichage de la matrice  (utile pour matrice petite sinon illisible)
def affiche_matrice(matrice):
    for liste in matrice:
        print(" ".join([str(nombre) for nombre in liste]))

#Vérification si la matrice est connexe
def est_connexe(matrice):
    """Pars du sommet 0 et lance un parcours en prof pour donner l'ensemble des
    sommets connectés à 0, et affirme ou réfute la connexité du graphe"""
    compo_connexe = parcours_profondeur(matrice, 0, [])
    if len(compo_connexe) == nb_sommet:
        print("Votre graphe est connexe")
    else:
        print("Votre graphe n'est pas connexe")


def parcours_profondeur(matrice, sommet_depart, sommet_traite):
    """Parcours en profondeur sur la matrice d'adjacence pour déterminer
    la plus grande composante connexe"""
    sommet_traite.append(sommet_depart)
    for destination in destinations_possibles(sommet_depart):
        if destination not in sommet_traite:
            parcours_profondeur(matrice, destination, sommet_traite)
    else:
        return sommet_traite # Tous les sommets traites à partir de 0, sont liés à 0


def destinations_possibles(sommet_depart):
    """Renvoie une liste de sommet directement accessible à
    partir du sommet de départ"""
    depart = matrice[sommet_depart]
    return [j for j in range(len(depart)) if (depart[j] != 0)]



#Main pour tester les fonctions
if __name__ == "__main__":
    file = "metro.txt"
    V = file_parser(file,"stations")
    E = file_parser(file,"liens")
    nb_sommet = len(V)
    matrice = generer_matrice(nb_sommet)
    #fill_matrice(matrice,E)
    #est_connexe(matrice)
    #est_connexe(matrice)
    #g = PlusCourtChemin(matrice, 0, 3)