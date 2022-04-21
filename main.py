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



###############################################################################
# Il est temps de faire un peu de djiskra
###############################################################################

# Python program for Dijkstra's single
# source shortest path algorithm. The program is
# for adjacency matrix representation of the graph
class PlusCourtChemin():
 
    def __init__(self, matrice, sommet_depart, sommet_arrive):
        self.nb_sommet = len(matrice)
        self.matrice = matrice
        self.sommet_depart = sommet_depart
        self.sommet_arrive = sommet_arrive
        self.dijkstra(sommet_depart, sommet_arrive)
 
    def mini_temps(self, temps, sommet_traite):
        """Cherche dans la liste temps l'indice du sommet
        non traité qui corresponds au minimum de temps."""
        min = 1e7
        min_index = 0
        for v in range(self.nb_sommet):
            if temps[v] < min and sommet_traite[v] == False:
                min = temps[v]
                min_index = v
        return min_index

    def dijkstra(self, sommet_depart, sommet_arrive):
        """Principale djikra"""
        sommet_traite = [False] * self.nb_sommet
        temps = [1e7] * self.nb_sommet
        temps[sommet_depart] = 0
        pere = {sommet_depart:None}  #Racine
        for _ in range(self.nb_sommet):  # Sommet duquel je pars
            index_mini_tps = self.mini_temps(temps, sommet_traite)
            sommet_traite[index_mini_tps] = True
            for v in range(self.nb_sommet):
                tps_depart_arrive = self.matrice[index_mini_tps][v]
                tps_minimum = temps[index_mini_tps]
                tps_itineraire = tps_minimum + tps_depart_arrive
                if (tps_depart_arrive > 0) and (sommet_traite[v] == False) and (temps[v] > tps_itineraire):
                    temps[v] = tps_itineraire
                    pere[v] = index_mini_tps
        self.mes_itineraire(pere, sommet_depart, sommet_arrive)

    def mes_itineraire(self, dico, sommet_depart, sommet_arrive):
        """Pars de l'arrive pour remontrer progressivement au sommet de départ"""
        itineraire = []
        while dico[sommet_arrive] != None: # Racine
            itineraire.append(sommet_arrive)
            sommet_arrive = dico[sommet_arrive]
        itineraire.append(sommet_depart)
        print(itineraire[::-1]) # Je suis parti de l'arrivé donc forcément...

# Driver program
 
# This code is contributed by Divyanshu Mehta

#Main pour tester les fonctions
if __name__ == "__main__":
    file = "test_fichier.txt"
    V = file_parser(file,"stations")
    E = file_parser(file,"liens")
    nb_sommet = len(V)
    matrice = generer_matrice(nb_sommet)
    fill_matrice(matrice,E)
    #est_connexe(matrice)
    #print(destinations_possibles(171))
    PlusCourtChemin(matrice, 0, 3)