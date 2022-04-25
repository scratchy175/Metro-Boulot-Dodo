
#Parsing du fichier pour isoler les stations et les liens et obtenir deux listes propres
from xml.sax.saxutils import prepare_input_source


from re import I


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

###############################################################################
# Consigne de voyages
###############################################################################

def direction(sommet_dep=252, sommet_arr=166):
    """Détermine la direction dans laquelle il faut aller"""
    terminus_1 = int(V[sommet_dep][3]) # On a besoin que d'un terminus_1
    terminus_2 = int(V[sommet_dep][4])
    delta_T1 = dijkstra(matrice, sommet_dep, terminus_1)[1]
    delta_T2 = dijkstra(matrice, sommet_arr, terminus_1)[1]
    ligne = V[sommet_dep][2]
    if delta_T1 > delta_T2:
        return print("direction {}".format(terminus_1))
    else:
        return print("direction {}".format(terminus_2))


def consigne(dep, arrive):
    """Prend en paramètre l'itineraire et le simplifie
    pour donner les consignes sous le formet demande"""
    itineraire, tps = dijkstra(matrice, dep, arrive)
    depart = itineraire[0]
    destination = itineraire[-1]
    ligne_traite = []
    tps = tps/60
    print("Vous etes à", depart)
    for i in range(len(itineraire)-1):
        ligne_de_arret1 = V[itineraire[i]][2]
        ligne_de_arret2 = V[itineraire[i+1]][2]
        if ligne_de_arret1 != ligne_de_arret2:
            print("A {}, changez et prenez la ligne {} ".format(itineraire[i], ligne_de_arret2), end="")
        else:
            if ligne_de_arret1 not in ligne_traite:
                direction(itineraire[i], itineraire[i+1])
                ligne_traite.append(ligne_de_arret1)
    print("Vous devriez arriver à {} dans {} minutes".format(destination, tps))



###############################################################################
#Partie que j'ai fait
###############################################################################


#fonction qui renvoie un dico contenant les terminus et leurs poids d'un sommet (mini dijktra)
def poids(matrice,stations,start):
    terminus_ligne = [int(stations[start][3]),int(stations[start][4])]
    ligne_metro = stations[start][2]
    nontraiter = [val for val in range(len(stations)) if stations[val][2] == ligne_metro and val != start]
    traiter = [start]
    dico={start:0}
    n = 0
    while len(nontraiter)+1 != len(traiter):
        for j in nontraiter:
            poid = matrice[traiter[n]][j]
            if poid != 0 and j not in traiter:
                dico[j] = dico[traiter[n]] + poid
                traiter.append(j)
        if traiter[n] not in terminus_ligne:
            dico.pop(traiter[n])
        n += 1
    #print(dico)
    return dico

def affichage(stations,trajet,temps):
    #affichage du depart
    print("Vous êtes à {}.".format(stations[trajet[0]][5]))

    #création de la liste contenant le premier sommet, le dernier et les sommet ou il y a un changement
    sommet = trajet[0]
    liste_changements = [trajet[0]]
    for j in range(len(trajet)):
        if stations[sommet][2] != stations[trajet[j]][2]:
            liste_changements.append(trajet[j-1])
            liste_changements.append(trajet[j])
        sommet = trajet[j]
    liste_changements.append(trajet[j])
    ##print(liste_changements)


    #affichage entre le premier sommet et le premier changement ou le dernier sommet si il n'y a pas de changement
    p1=poids(matrice,stations,liste_changements[0]) #poids du premier sommet et ses terminus
    p2=poids(matrice,stations,liste_changements[1]) #poids du dernier sommet ou du premier changement et ses terminus
    #on obtiens un dico avec les terminus et leur poids
    ##print(p1,p2)
    key1 = list(p1.keys()) #pour recuperer les cles du dico
    if stations[liste_changements[0]][2] == '13' or stations[liste_changements[0]][2] == '07': #petit check si ligne 13 ou 7
        if p1[key1[0]] < p2[key1[0]]:  #comparaison des poids
            print('Prenez la ligne {} direction {}'.format(stations[liste_changements[0]][2],stations[key1[1]][6]))
        else:
            print('Prenez la ligne {} direction {}'.format(stations[liste_changements[0]][2],stations[key1[0]][6]))
    else:
        if p1[key1[0]] < p2[key1[0]]:
            print('Prenez la ligne {} direction {}'.format(stations[liste_changements[0]][2],stations[key1[1]][5]))
        else:
            print('Prenez la ligne {} direction {}'.format(stations[liste_changements[0]][2],stations[key1[0]][5]))

    #affichage entre les changements intermediaires et la fin du trajet
    if len(liste_changements) > 2: # si il y a plus de 2 changements
        for i in range(2,len(liste_changements),2):
            p1=poids(matrice,stations,liste_changements[i])
            p2=poids(matrice,stations,liste_changements[i+1])
            ##print(p1,p2)
            key1 = list(p1.keys())
            if stations[liste_changements[i]][2] == '13' or stations[liste_changements[i]][2] == '07':
                if p1[key1[0]] < p2[key1[0]]:
                    print('A {}, changez et prenez la ligne {} direction {}'.format(stations[liste_changements[i]][6],stations[liste_changements[i]][2],stations[key1[1]][6]))
                else:
                    print('A {}, changez et prenez la ligne {} direction {}'.format(stations[liste_changements[i]][6],stations[liste_changements[i]][2],stations[key1[0]][6]))
            else:
                if p1[key1[0]] < p2[key1[0]]:
                    print('A {}, changez et prenez la ligne {} direction {}'.format(stations[liste_changements[i]][5],stations[liste_changements[i]][2],stations[key1[1]][5]))
                else:
                    print('A {}, changez et prenez la ligne {} direction {}'.format(stations[liste_changements[i]][5],stations[liste_changements[i]][2],stations[key1[0]][5]))

    #affichage de l'arrivee
    print("Vous devriez arriver a {} dans {} minutes.".format(stations[trajet[j]][5],temps//60))



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
    #print(dijkstra(matrice, 0, 5)) 

    print("matrice",matrice[7].index(39))
    #trajet,temps = dijkstra(matrice, 0, 150)
    #trajet,temps = dijkstra(matrice, 150, 0)
    #trajet,temps = dijkstra(matrice, 1, 5)
    #trajet,temps = dijkstra(matrice, 5, 1)
    trajet,temps = dijkstra(matrice, 0, 39)
    print(trajet)
    print(temps)
    
    affichage(V,trajet,temps)


    
    
