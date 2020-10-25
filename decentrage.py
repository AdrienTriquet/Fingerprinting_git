import ravif
import correlation

# ajouter un décompte du nombre de fingerprint calculer / restantes
def decentrage(path_base, path):
    resolution = 100
    f_base = ravif.ravif(path_base, 128, 128)
    meilleure_valeur = -1

    x, y = 0, 0
    while y < 255 :
        while x < 255 :
            f_comparaison = ravif.ravif(path, x, y)

            x += resolution
            valeur = correlation.correlation(f_base, f_comparaison)[0]

            if valeur > meilleure_valeur :
                meilleure_valeur = valeur

        y += resolution
        x = 0

    return meilleure_valeur


# Ouverture du chemin de base
path_base = "input_base.txt"

path_comparaison = "input_comparaison.txt"

print(decentrage(path_base, path_comparaison))