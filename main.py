
#Parsing du fichier pour isoler les stations et les liens et obtenir deux listes propres
def file_parser(file,arg):
    with open(file, "r") as fd:
        lecture = fd.readlines()
        stations = []
        liens = []
        for ligne in lecture:
            premiere_lettre = ligne[0]
            if premiere_lettre == 'V':
                stations.append(ligne.strip("\n",).split(" ",2))
            elif premiere_lettre == 'E':
                liens.append(ligne.strip("\n").split(" "))
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
        matrice[sommet_depart][sommet_arrive] = 1
        matrice[sommet_arrive][sommet_depart] = 1


#Affichage de la matrice  (utile pour matrice petite sinon illisible)
def affiche_matrice(matrice):
    for liste in matrice:
        print(" ".join([str(nombre) for nombre in liste]))

#Vérification si la matrice est connexe
def est_connexe(matrice):
    """Pars du sommet 0 et lance un parcours en prof pour donner l'ensemble des
    sommets connctés à 0 dans la liste composante_connexe_global"""
    composante_connexe_global = []
    parcours_profondeur(matrice, 0, [], [], composante_connexe_global)
    composante_connexe_global = composante_connexe_global[-1]
    if len(composante_connexe_global) == nb_sommet:
        print("Votre graphe est connexe")
    else:
        print("Votre graphe n'est pas connexe")


def parcours_profondeur(matrice, sommet_depart, sommet_traite, 
                        compo_local_connexe, compo_global_connexe):
    """Parcours en profondeur sur la matrice d'adjacence pour déterminer
    la plus grande composante connexe"""
    sommet_traite.append(sommet_depart)
    compo_local_connexe.append(sommet_depart)
    depart = matrice[sommet_depart]
    les_destinations = [j for j in range(len(depart)) if (depart[j] == 1)]
    if existe_sommet_non_traite(les_destinations, sommet_traite):
        for destination in les_destinations:
            if destination not in sommet_traite:
                parcours_profondeur(matrice, destination, sommet_traite,
                                    compo_local_connexe, compo_global_connexe)
    else:
        compo_global_connexe.append(compo_local_connexe)

def existe_sommet_non_traite(liste, liste_traite):
    """Renvoie vraie s'il exite au moins un sommet non traite"""
    if len(liste) >= 1 :
        for elem in liste:
            if elem not in liste_traite:
                return True
        return False
    else:
        return False


#Main pour tester les fonctions
if __name__ == "__main__":
    path = "metro.txt"
    V = file_parser(path,"stations")
    E = file_parser(path,"liens")
    nb_sommet = len(V)
    matrice = generer_matrice(nb_sommet)
    fill_matrice(matrice,E)
    est_connexe(matrice)
