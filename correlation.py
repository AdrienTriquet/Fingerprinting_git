import scipy.stats
import base64
from binascii import hexlify
import numpy as np
import math


def f_correlation(fingerprint_base, fingerprint_compar):
    ### passage de la base 64 à de l'hexadecimale
    decod1 = hexlify(base64.b64decode(fingerprint_base))
    decod2 = hexlify(base64.b64decode(fingerprint_compar))

    ### Mise sous forme de string utilisable par la suite
    decod1_str = str(decod1)
    decod2_str = str(decod2)

    ### Les 2 fingerprint doivent avoir la même taille, toutes les variables utilisées sont donc de même taille n ici
    n = len(decod1)

    ### On enleve les indicateurs au début à la fin pour n'utiliser que le contenu
    decod1_str_crop = decod1_str[2:n - 1]
    decod2_str_crop = decod2_str[2:n - 1]

    ### Creation des listes finales à comparer
    list1 = []
    list2 = []

    ### On remplie les liste de n-3 caractères car on a enlevé précedement les indicateurs
    for i in range(n - 3):
        ### On rempli les 2 listes de valeur décimales utilisables par la fonction scipy
        list1.append((int(decod1_str_crop[i], 16)))
        list2.append((int(decod2_str_crop[i], 16)))

    ### on vient enfin comparer nos deux array
    return scipy.stats.pearsonr(list1, list2)


def correlation_3(f_1, f_2):
    #  Passage de base 64 à une chaine de caractère des binaires
    bin_1 = "".join(["{:08b}".format(x) for x in f_1])
    bin_2 = "".join(["{:08b}".format(x) for x in f_2])

    # Mise sous la forme d'une liste avec tous les décimaux
    dec_1 = []
    dec_2 = []
    for i in range(0, len(bin_1), 8):
        dec_1.append(int(bin_1[i:i + 8], 2))
        dec_2.append(int(bin_2[i:i + 8], 2))

    # Calcul des valeurs : Rho = correlation, t = test statistique
    mean1 = np.mean(dec_1)
    mean2 = np.mean(dec_2)
    num = 0
    denom1, denom2 = 0, 0
    for i in range(len(dec_1) - 1):
        num += (dec_1[i] - mean1) * (dec_2[i] - mean2)
        denom1 += (dec_1[i] - mean1) ** 2
        denom2 += (dec_2[i] - mean2) ** 2
    rho = num / math.sqrt(denom1 * denom2)
    t = rho * math.sqrt((len(dec_1) - 2) / (1 - rho ** 2))
    return rho, t

f1 = b'DAwMDAwMDAwNDA0NDQ0NDQ0NDA0NDQ0NDQ0NDQ0NDA0NDAwzNDQzMzMzMjIyMDAuKSkoJSUiICAeGRgXExERDg4ODAwMDAwMCwsLCwsLCw0NDQwMDQwMDAwMDQwMDB8fHBcXFxgYIC4uPkpKUlRUWVpaW1tbWFBQUVNTWFxcUUsHBwcHBwcHBwcHBwcHCAgHCAgHCAgICAgICAgICAgICAgICAgICAgICAgHBwgHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcICQkLDQ0QEhIUFhYYGxsdHx8fLi4sKSkqKysxPDxIU1NeYGBlaWlqampnX19gYmJmampcVgoKCgoKCgoKCgoKCgoLCwoLCwoLCwsLCwsLCwsLCwsLCwsLHB4eICEhIyYmKi4uLi4uLy4uLy8vLy4wLy8wMC8wMC8wMDAvLy4tLSwrKyoqKikoKCcmJiQiIiEfHx4qKiUfHx4cHCQ0NEhXV19fX2FhYWJhYV5WVldaWl5hYVhU'
f2 = b'k5OTkpKSkpKTk5OTkpKTkpKRkJCQj5CQj5CPj4+Ojo6Oj4+QkJCQkJCQj4+Pj5CQkZGRkJGQkJGQkJCRkZGRkZGSkpKSkpGSkpOUk5SVlZWWlpaVlJWVlZeXl5iYmJeXlpWWl5eZmpqamZiZmZmZmpmam5qbm5ubm5qam5qbnJtxcXFxcXFxcXFxcXFxcXBwb29ubm5ub29vb25ubm5ubm9vb29vb29vb29vb29vb3BwcHBwcG9vcHBvb3BwcHBwcHBxcXFxcXFxcnJxcnJyc3N0c3Nyc3NzdHR0dXV1dHRzc3N0dHV2dnZ1dXV1dXV1dXZ2dnd3d3d3dnd3d3d4eGNjY2JjY2JjY2NjY2JjY2JiYWBgYGBhYWFhYWFhYGFgYGFhYWFhYmJiYmFhYWFiYWJiYmJiYmFiYmFiYmJjYmJhY2NjY2NiY2NkY2NkZGRlZWVlZGRkZWRlZWVmZmZmZmVkZWZmZ2dnZ2ZlZmVlZmZlZmZmZ2dnZ2dnZ2dnZ2ho'