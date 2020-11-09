import scipy.stats
import base64
from binascii import hexlify

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
