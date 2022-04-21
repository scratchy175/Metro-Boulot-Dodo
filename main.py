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

def generer_matrice(n):
    """Renvoie une matrice de taille n*n"""
    return [[0]*n for _ in range(n)]


def fill_matrice(matrice, liens):
    """Remplis la matrice à partir des relations entre deux
    arrets, ces relations ne forment pas tous le temps des
    aretes mais peuvent etre des arcs! (Ligne 10 et 7bis)."""
    arc_ligne_7b = [34, 248, 280, 92]
    arc_ligne_10 = [36, 198, 52, 201, 145, 373, 196, 259]
    for ligne in liens:
        sommet_depart = int(ligne[1])
        sommet_arrive = int(ligne[2])
        temps = int(ligne[3])
        matrice[sommet_depart][sommet_arrive] = temps
        if ((sommet_depart in arc_ligne_7b and sommet_arrive in arc_ligne_7b)
            or (sommet_depart in arc_ligne_10 and sommet_arrive in arc_ligne_10)
            ):
            pass
            #print(sommet_depart, sommet_arrive)
        else:
            matrice[sommet_arrive][sommet_depart] = temps


def affiche_matrice(matrice):
    """Affiche la matrice"""
    for liste in matrice:
        print(" ".join([str(nombre) for nombre in liste]))


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


###############################################################################
# Il est temps de faire un peu de djiskra
###############################################################################

def mini_temps( temps, sommet_traite):
    """Cherche dans la liste temps l'indice du sommet
    non traité qui corresponds au minimum de temps."""
    min = 1e7
    min_index = 0
    for v in range(nb_sommet):
        if temps[v] < min and sommet_traite[v] == False:
            min = temps[v]
            min_index = v
    return min_index


def dijkstra(matrice, sommet_depart, sommet_arrive):
    """Renvoie l'itinéraire le plus court entre le sommet de départ
    et le somme d'arrive. """
    sommet_traite = [False] * nb_sommet
    temps = [1e7] * nb_sommet
    temps[sommet_depart] = 0
    pere = {sommet_depart:None}  #Racine
    for _ in range(nb_sommet):  # Sommet duquel je pars
        index_mini_tps = mini_temps(temps, sommet_traite)
        sommet_traite[index_mini_tps] = True
        for v in range(nb_sommet):
            tps_depart_arrive = matrice[index_mini_tps][v]
            tps_minimum = temps[index_mini_tps]
            tps_itineraire = tps_minimum + tps_depart_arrive
            if (tps_depart_arrive > 0) and (sommet_traite[v] == False) and (temps[v] > tps_itineraire):
                temps[v] = tps_itineraire
                pere[v] = index_mini_tps
    plus_court_chemin = mes_itineraire(pere, sommet_depart, sommet_arrive)
    temps_plus_court_chemin = temps[sommet_arrive]
    return plus_court_chemin, temps_plus_court_chemin


def mes_itineraire(dico, sommet_depart, sommet_arrive):
    """Pars de l'arrive pour remontrer progressivement au sommet de départ"""
    itineraire = []
    while dico[sommet_arrive] != None: # Je m'arrete lorsque Racine
        itineraire.append(sommet_arrive)
        sommet_arrive = dico[sommet_arrive]
    itineraire.append(sommet_depart)  # Je rajoute la racine
    return itineraire[::-1] # Je suis parti de l'arrivé donc forcément...


#Main pour tester les fonctions
if __name__ == "__main__":
    file = "metro.txt"
    V = file_parser(file,"stations")
    E = file_parser(file,"liens")
    nb_sommet = len(V)
    matrice = generer_matrice(nb_sommet)
    fill_matrice(matrice,E)
    #est_connexe(matrice)
    #print(destinations_possibles(92))
    print(dijkstra(matrice, 52, 198))