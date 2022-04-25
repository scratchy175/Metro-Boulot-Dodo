import tkinter as tk
liste_arret = ["Daumesnil", "Denfert Rochereau", "Faidherbe-Chaligny", "Esplanade de la Défense"]
police = ('Bahnschrift Light SemiCondensed', 17)


def interface(information, colonne):
    """Gère l'interface utilisateur"""
    indication = tk.Label(racine,
                          font=police,
                          text="Veuillez saisair " + information)
    entree = tk.Entry(racine, font=police)
    valider = tk.Button(racine, text="Valider",
                        font=police,
                        command=lambda: bloque_entree(entree))
    indication.grid(column=colonne, row=0)
    entree.grid(column=colonne, row=1)
    valider.grid(column=colonne, row=2)


def bloque_entree(entree):
    """Bloque l'entrée correspondante"""
    entree.config(state="disabled")

racine = tk.Tk()
canvas = tk.Canvas(height=400, width=500)
canvas.grid(column=0, row=0, columnspan=2, rowspan=4)
for indice, info in enumerate(["départ", "arrivée"]):
    interface(info, indice)
racine.mainloop()